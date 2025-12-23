from sqlalchemy import Column, Integer, Double, String, DateTime, ForeignKey
from observa.database.database import Base
from sqlalchemy.dialects.postgresql import JSONB 
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class SourceModel(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    json_data = Column(JSONB, nullable=True)  # conteúdo do arquivo JSON
    api_url = Column(String, nullable=True)     # se for remoto
    
    history_items = relationship(
        "HistoryModel",
        back_populates="source",
        passive_deletes=True
    )

class DetectorModel(Base):
    __tablename__ = "detectors"

    id = Column(Integer, primary_key=True, index=True)
    name_ap = Column(String, nullable=False)
    name = Column(String, unique=True, nullable=False)
    class_path = Column(String, nullable=True)  # ex: "observa.detectors.excessive_alerts.ExcessiveAlertsDetector"
    api_url = Column(String, nullable=True)     # se for remoto
    
    history_items = relationship(
        "HistoryModel",
        back_populates="detector",
        passive_deletes=True
    )

class HistoryModel(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("sources.id", ondelete="CASCADE"), nullable=False)
    detector_id = Column(Integer, ForeignKey("detectors.id", ondelete="CASCADE"), nullable=False)
    detected = Column(Integer, nullable=False)  
    total = Column(Integer, nullable=False)  
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    execution_time = Column(Double, nullable=False)  
    result = Column(JSONB, nullable=True)     
    
    source = relationship("SourceModel", back_populates="history_items")
    detector = relationship("DetectorModel", back_populates="history_items")