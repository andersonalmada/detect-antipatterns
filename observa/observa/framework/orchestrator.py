import time
from typing import Dict, Any
from observa.framework.manager import Manager
from observa.framework.base import Detector
import importlib
import requests

class Orchestrator:
    def __init__(self, manager: Manager):
        self.manager = manager

    def run(self, detector_name: str, source_name: str) -> Dict[str, Any]:
        detector = self.manager.get_detector(detector_name)
        if detector is None:
            raise ValueError(f"Detector '{detector_name}' not found")
        source = self.manager.get_source(source_name)
        if source is None:
            raise ValueError(f"Source '{source_name}' not found")    
        
        data = source.json_data
        start = time.time()
        
        if detector.api_url: # Remoto
            response = requests.post(detector.api_url, json=data)
            response.raise_for_status()
            result = response.json()
            result.setdefault('detector', detector.name)
        else: # Local
            module_name, class_name = detector.class_path.rsplit('.', 1)
            module = importlib.import_module(module_name)
            cls = getattr(module, class_name)
            detector = cls()
            result = detector.detect(data)
            result.setdefault('detector', detector.name())
        
        end = time.time()
        result.setdefault('source', source.name)        
        result.setdefault('execution_time_ms', round((end - start) * 1000, 3))
        return result