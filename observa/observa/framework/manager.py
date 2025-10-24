from typing import Dict, Any
from observa.framework.base import Source, Detector

class Manager:
    def __init__(self):
        self._sources: Dict[str, Source] = {}
        self._detectors: Dict[str, Detector] = {}

    # Sources
    def register_source(self, name: str, source: Source):
        self._sources[name] = source

    def get_source(self, name: str) -> Source:
        return self._sources.get(name)

    def list_sources(self):
        return list(self._sources.keys())

    # Detectors
    def register_detector(self, name: str, detector: Detector):
        self._detectors[name] = detector

    def get_detector(self, name: str) -> Detector:
        return self._detectors.get(name)

    def list_detectors(self):
        return list(self._detectors.keys())

global_manager = Manager()