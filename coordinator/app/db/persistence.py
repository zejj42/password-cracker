from abc import ABC, abstractmethod
from typing import Optional


class PersistenceLayer(ABC):
    """
    Abstract base class defining how we interact with our persistent store.
    """

    @abstractmethod
    def set_progress(self, hash_value: str, end: int) -> None:
        """
        Persist the last range_end processed for a given hash.
        """
        pass

    @abstractmethod
    def get_progress(self, hash_value: str) -> Optional[int]:
        """
        Retrieve the last range_end processed for a given hash.
        Returns None if no progress is recorded.
        """
        pass

    @abstractmethod
    def clear_progress(self, hash_value: str) -> None:
        """
        Remove the progress key for a given hash, indicating we no longer need it.
        """
        pass
