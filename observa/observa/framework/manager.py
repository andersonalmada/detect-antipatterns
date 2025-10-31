from typing import List, Optional
from observa.database.models import SourceModel, DetectorModel
from observa.database.repositories import SourceRepository, DetectorRepository
from observa.framework.base import Source

class Manager:
    def __init__(self):
        pass  # não precisa mais de dicionários internos

    # Sources
    def register_source(self, source: Source) -> SourceModel:
        source = SourceRepository.add_source(source.name, source.load())
        return source

    def get_source(self, name: str) -> Optional[SourceModel]:
        return SourceRepository.get_by_name(name)

    def list_sources(self) -> List[str]:
        return [s.name for s in SourceRepository.get_all()]

    # Detectors
    def register_detector(self, name: str, class_path: str = None, api_url: str = None) -> DetectorModel:
        detector = DetectorRepository.add_detector(name, class_path, api_url)
        return detector

    def get_detector(self, name: str) -> Optional[DetectorModel]:
        return DetectorRepository.get_by_name(name)

    def list_detectors(self) -> List[str]:
        return [d.name for d in DetectorRepository.get_all()]

# Singleton global
global_manager = Manager()
