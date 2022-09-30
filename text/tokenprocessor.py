from abc import ABC, abstractmethod
from typing import Iterable

class TokenProcessor(ABC):
    """A TokenProcessor applies some rules of normalization to a token from a document,
     and returns a term for that token."""
    @abstractmethod
    def process_token(self, token : str) -> Iterable[str]:
        """Normalizes a token into a term."""
        pass