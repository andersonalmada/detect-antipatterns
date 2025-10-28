from fastapi import APIRouter
from sqlalchemy import text
from observa.database.database import engine

router = APIRouter()
    
@router.post("/clear")
def clear_database():
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE sources, detectors RESTART IDENTITY CASCADE;"))
    return {"message": "✅ Database cleared successfully"}