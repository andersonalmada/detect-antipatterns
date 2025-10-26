from observa.database.database import SessionLocal
from observa.database.models import Source, Detector
import json

class SourceRepository:
    @staticmethod
    def add_source(name: str, json_content: dict):
        db = SessionLocal()
        src = Source(name=name, json_data=json_content)
        db.add(src)
        db.commit()
        db.close()

    @staticmethod
    def get_all():
        db = SessionLocal()
        sources = db.query(Source).all()
        db.close()
        return sources

    @staticmethod
    def get_by_name(name: str):
        db = SessionLocal()
        source = db.query(Source).filter(Source.name == name).first()
        db.close()
        return source


class DetectorRepository:
    @staticmethod
    def add_detector(name: str, class_path: str = None, api_url: str = None):
        db = SessionLocal()
        det = Detector(name=name, class_path=class_path, api_url=api_url)
        db.add(det)
        db.commit()
        db.close()

    @staticmethod
    def get_all():
        db = SessionLocal()
        detectors = db.query(Detector).all()
        db.close()
        return detectors

    @staticmethod
    def get_by_name(name: str):
        db = SessionLocal()
        det = db.query(Detector).filter(Detector.name == name).first()
        db.close()
        return det
