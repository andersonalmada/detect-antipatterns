from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from observa.framework.orchestrator import Orchestrator
from observa.framework.manager import global_manager as manager

router = APIRouter()
_orchestrator = Orchestrator(manager)

class RunRequest(BaseModel):
    source: str
    detector: str

@router.post('/execute')
def execute_run(req: RunRequest):
    try:
        result = _orchestrator.run(req.detector, req.source)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return result
