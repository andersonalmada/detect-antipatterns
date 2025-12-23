from observa.database.models import SourceModel, DetectorModel, HistoryModel
from observa.database.repositories import SourceRepository, DetectorRepository, HistoryRepository
from observa.framework.base import Source
from typing import List, Optional, Dict, Any
from datetime import datetime

class Manager:
    def __init__(self):
        pass  # não precisa mais de dicionários internos

    # Sources
    def register_source(self, source: Source) -> SourceModel:
        if source.api_url:
            source = SourceRepository.add_source(name=source.name, api_url=source.api_url)
        else:
            source = SourceRepository.add_source(name=source.name, json_content=source.load())
        return source

    def get_source(self, name: str) -> Optional[SourceModel]:
        return SourceRepository.get_by_name(name)

    def list_sources(self) -> List[str]:
        return [s.name for s in SourceRepository.get_all()]

    # Detectors
    def register_detector(self, name_ap: str, name: str, class_path: str = None, api_url: str = None) -> DetectorModel:
        detector = DetectorRepository.add_detector(name_ap=name_ap, name=name, class_path=class_path, api_url=api_url)
        return detector

    def get_detector(self, name: str) -> Optional[DetectorModel]:
        return DetectorRepository.get_by_name(name)

    def list_detectors(self) -> List[DetectorModel]:
        return DetectorRepository.get_all()
    
    # History
    def register_history(self, source_id: int, detector_id: int, result: Dict[str, Any]) -> HistoryModel:
        history = HistoryRepository.add_history(source_id=source_id,detector_id=detector_id,detected=result["detected"],total=result["analyzed"],result=result["data"], execution_time=result["execution_time_ms"])
        return history

    def get_history(self, source_id: int, detector_id: int, start: datetime, end: datetime) -> Optional[List[HistoryModel]]:
        return HistoryRepository.get_by_source_and_detector(source_id=source_id,detector_id=detector_id, start=start, end=end)

# Singleton global
global_manager = Manager()
