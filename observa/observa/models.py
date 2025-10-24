from sqlalchemy import Column, Integer, String, Text
from observa.database import Base

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    json_data = Column(Text, nullable=False)  # conteúdo do arquivo JSON


class Detector(Base):
    __tablename__ = "detectors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    class_path = Column(String, nullable=True)  # ex: "observa.detectors.excessive_alerts.ExcessiveAlertsDetector"
    api_url = Column(String, nullable=True)     # se for remoto
