from observa.database.database import SessionLocal
from observa.database.models import SourceModel, DetectorModel

class SourceRepository:
    @staticmethod
    def add_source(name: str, json_content: dict):
        db = SessionLocal()
        src = SourceModel(name=name, json_data=json_content)
        db.add(src)
        db.commit()
        db.close()

    @staticmethod
    def get_all():
        db = SessionLocal()
        sources = db.query(SourceModel).all()
        db.close()
        return sources

    @staticmethod
    def get_by_name(name: str):
        db = SessionLocal()
        source = db.query(SourceModel).filter(SourceModel.name == name).first()
        db.close()
        return source
    
    @staticmethod
    def delete_batch(names: list[str]):
        db = SessionLocal()
        db.query(SourceModel).filter(SourceModel.name.in_(names)).delete(synchronize_session=False)
        db.commit()  
        db.close()

class DetectorRepository:
    @staticmethod
    def add_detector(name: str, class_path: str = None, api_url: str = None):
        db = SessionLocal()
        det = DetectorModel(name=name, class_path=class_path, api_url=api_url)
        db.add(det)
        db.commit()
        db.close()

    @staticmethod
    def get_all():
        db = SessionLocal()
        detectors = db.query(DetectorModel).all()
        db.close()
        return detectors

    @staticmethod
    def get_by_name(name: str):
        db = SessionLocal()
        det = db.query(DetectorModel).filter(DetectorModel.name == name).first()
        db.close()
        return det

    @staticmethod
    def delete_batch(names: list[str]):
        db = SessionLocal()
        db.query(DetectorModel).filter(DetectorModel.name.in_(names)).delete(synchronize_session=False)
        db.commit()  
        db.close()