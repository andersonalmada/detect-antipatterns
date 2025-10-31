from abc import ABC, abstractmethod
from typing import Any, Dict

class Source(ABC):    
    def __init__(self, name: str = "Source", json_data: Any = None):
        self.name = name
        self.json_data = json_data
            
    @abstractmethod
    def load(self) -> Any:
        """Load and return data in a standardized format (e.g., list/dict)."""
        raise NotImplementedError

class Detector(ABC):
    def __init__(self, name: str = "Detector", api_url: str = None, class_path: str = None):
        self.name = name
        self.api_url = api_url
        self.class_path = class_path
    
    @abstractmethod
    def detect(self, data: Any) -> Dict:
        """Return a JSON-serializable dict with detection results."""
        raise NotImplementedError
