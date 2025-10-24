import time
from typing import Dict, Any
from observa.framework.manager import Manager

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

        data = source.load()
        start = time.time()
        result = detector.detect(data)
        end = time.time()
        result.setdefault('detector', detector.name())
        result.setdefault('execution_time_ms', round((end - start) * 1000, 3))
        return result
