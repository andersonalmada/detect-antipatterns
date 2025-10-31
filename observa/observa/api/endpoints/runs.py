from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from observa.framework.orchestrator import global_orchestrator as orchestrator
from typing import List

router = APIRouter()

class RunRequest(BaseModel):
    sources: List[str]
    detectors: List[str]

@router.post('/execute')
def execute_run(req: RunRequest):
    result = []    
    try:
        for src in req.sources:
            for det in req.detectors:
                result.append(orchestrator.runByDatabase(source_name=src, detector_name=det))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return result
