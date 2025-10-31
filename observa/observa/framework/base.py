from abc import ABC, abstractmethod
from typing import Any, Dict

class Source(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass
    
    @abstractmethod
    def load(self) -> Any:
        """Load and return data in a standardized format (e.g., list/dict)."""
        raise NotImplementedError

class Detector(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def detect(self, data: Any) -> Dict:
        """Return a JSON-serializable dict with detection results."""
        raise NotImplementedError
