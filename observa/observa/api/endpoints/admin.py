from fastapi import APIRouter
from sqlalchemy import text
from pydantic import BaseModel
from observa.database.database import engine
from observa.database.repositories import SourceRepository, DetectorRepository
from typing import List

router = APIRouter()
class DeleteRequest(BaseModel):
    names: List[str]
        
@router.delete("/clear")
def clear_database():
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE sources, detectors RESTART IDENTITY CASCADE;"))
    return {"message": "✅ Database cleared successfully"}

@router.delete("/sources")
def delete_sources(req: DeleteRequest):
    SourceRepository.delete_batch(req.names)
    return {"message": f"Deleted sources: {', '.join(req.names)}"}

@router.delete("/detectors")
def delete_sources(req: DeleteRequest):
    DetectorRepository.delete_batch(req.names)
    return {"message": f"Deleted detectors: {', '.join(req.names)}"}