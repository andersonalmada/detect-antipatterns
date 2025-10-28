from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from observa.framework.orchestrator import Orchestrator
from observa.framework.manager import global_manager as manager
from typing import List

router = APIRouter()
_orchestrator = Orchestrator(manager)

class RunRequest(BaseModel):
    sources: List[str]
    detectors: List[str]

@router.post('/execute')
def execute_run(req: RunRequest):
    result = []
    
    try:
        for src in req.sources:
            for det in req.detectors:
                result.append(_orchestrator.run(det, src))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return result
