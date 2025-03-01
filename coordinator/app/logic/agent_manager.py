import asyncio
from itertools import cycle
from typing import List, Optional
from app.apis.http_utils import fetch
from app.models.types import ChunkPayload, CrackResult

MAX_RETRIES = 3
RETRY_DELAY = 1


class AgentManager:
    def __init__(self, agent_urls: List[str]) -> None:
        self.agent_urls_cycle = cycle(agent_urls)

    async def dispatch_with_retry(self, payload: ChunkPayload) -> Optional[CrackResult]:
        attempt = 0
        while attempt < MAX_RETRIES:
            agent_url = next(self.agent_urls_cycle)
            dispatch_url = f"{agent_url}/crack/"
            try:
                result = await fetch(
                    dispatch_url,
                    method="POST",
                    json=payload,
                )
                if result is not None:
                    return result
            except Exception as e:
                print(
                    f"Error dispatching to {dispatch_url} on attempt {attempt+1}: {e}"
                )
            attempt += 1
            await asyncio.sleep(RETRY_DELAY * (2**attempt))
        return None
