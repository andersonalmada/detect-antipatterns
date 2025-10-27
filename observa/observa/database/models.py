from sqlalchemy import Column, Integer, String, Text
from observa.database.database import Base
from sqlalchemy.dialects.postgresql import JSONB 

class SourceModel(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    json_data = Column(JSONB, nullable=False)  # conteúdo do arquivo JSON

class DetectorModel(Base):
    __tablename__ = "detectors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    class_path = Column(String, nullable=True)  # ex: "observa.detectors.excessive_alerts.ExcessiveAlertsDetector"
    api_url = Column(String, nullable=True)     # se for remoto
