import asyncio
import time
from typing import List, Optional

from app.core.config import settings
from app.db import get_persistence
from app.logic.agent_manager import AgentManager
from app.models.types import CrackResult, ChunkPayload

CHUNK_SIZE: int = 100_000
TOTAL_NUMBERS: int = 100_000_000
BATCH_SIZE: int = 100
FOUND_KEY = "found"


def log_result(found_result: Optional[CrackResult], elapsed_time: float) -> None:
    if found_result and found_result.get(FOUND_KEY):
        print(f"Found result: {found_result}")
    else:
        print("No match found in any chunk.")
    print(f"Total processing time: {elapsed_time:.2f} seconds")


class CoordinatorTaskManager:
    def __init__(self):
        self.found_event: asyncio.Event = asyncio.Event()
        self.found_result: Optional[CrackResult] = None
        self.persistence = get_persistence()
        self.agent_manager = AgentManager(settings.agent_list)

    def get_resume_start(self, hash_value: str) -> int:
        last_processed = self.persistence.get_progress(hash_value)
        return (last_processed + CHUNK_SIZE) if last_processed is not None else 0

    def create_payload(self, hash_value: str, start: int, end: int) -> ChunkPayload:
        return {"hash": hash_value, "range_start": start, "range_end": end}

    async def dispatch_chunk(self, payload: ChunkPayload) -> Optional[CrackResult]:
        self.persistence.set_progress(payload["hash"], payload["range_end"])
        if self.found_event.is_set():
            return None

        result = await self.agent_manager.dispatch_with_retry(payload)

        if result and result.get(FOUND_KEY):
            self.persistence.clear_progress(payload["hash"])
            self.found_event.set()
        return result

    async def check_batch_for_match(self, batch_tasks: List[asyncio.Task]) -> bool:
        results = await asyncio.gather(*batch_tasks, return_exceptions=True)
        for res in results:
            if res and isinstance(res, dict) and res.get(FOUND_KEY):
                self.found_result = res
                return True
        return False

    def cancel_remaining_tasks(self, batch_tasks: List[asyncio.Task]) -> None:
        for task in batch_tasks:
            if not task.done():
                task.cancel()

    async def process_chunks(self, hash_value: str) -> None:
        batch_tasks: List[asyncio.Task] = []
        resume_start = self.get_resume_start(hash_value)

        for start in range(resume_start, TOTAL_NUMBERS, CHUNK_SIZE):
            if self.found_event.is_set():
                break
            end = min(start + CHUNK_SIZE, TOTAL_NUMBERS)

            payload = self.create_payload(hash_value, start, end)
            batch_tasks.append(asyncio.create_task(self.dispatch_chunk(payload)))

            if len(batch_tasks) >= BATCH_SIZE:
                if await self.check_batch_for_match(batch_tasks):
                    break
                batch_tasks = []

        if batch_tasks and not self.found_event.is_set():
            await self.check_batch_for_match(batch_tasks)

        self.cancel_remaining_tasks(batch_tasks)

    async def process_hash(self, hash_value: str) -> Optional[CrackResult]:
        print(f"Starting to process hash: {hash_value}")
        start_time = time.monotonic()

        await self.process_chunks(hash_value)

        elapsed_time = time.monotonic() - start_time
        log_result(self.found_result, elapsed_time)
        self.persistence.clear_progress(hash_value)
        return self.found_result


async def process_hash_task(hash_value: str) -> Optional[CrackResult]:
    manager = CoordinatorTaskManager()
    return await manager.process_hash(hash_value)
