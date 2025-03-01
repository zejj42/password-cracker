from typing import Optional
from .persistence import PersistenceLayer
from app.db.redis_client import redis_client


class RedisPersistence(PersistenceLayer):
    """
    Concrete implementation of PersistenceLayer using Redis as the backend.
    """

    def set_progress(self, hash_value: str, end: int) -> None:
        key = f"hash:{hash_value}"
        redis_client.set(key, end)

    def get_progress(self, hash_value: str) -> Optional[int]:
        key = f"hash:{hash_value}"
        val = redis_client.get(key)
        return int(val) if val else None

    def clear_progress(self, hash_value: str) -> None:
        key = f"hash:{hash_value}"
        redis_client.delete(key)
