from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
from observa.framework.manager import global_manager as manager
from observa.sources.json_source import JsonSource

router = APIRouter()
# using a simple in-memory manager instance for skeleton
_manager = manager

class SourceRegisterRequest(BaseModel):
    name: str
    path: str

@router.post('/register')
def register_source(req: SourceRegisterRequest):
    src = JsonSource(req.path)
    _manager.register_source(req.name, src)
    return {'message': f"Source '{req.name}' registered"}

@router.get('/list')
def list_sources():
    return {'sources': _manager.list_sources()}
