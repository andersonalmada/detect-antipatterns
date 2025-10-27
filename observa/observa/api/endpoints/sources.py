from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
from observa.framework.manager import global_manager as manager
from observa.sources.json_source import JsonSource

router = APIRouter()
_manager = manager

class SourceRegisterRequest(BaseModel):
    name: str
    json_data: dict

@router.post('/register')
def register_source(req: SourceRegisterRequest):
    _manager.register_source(req.name, req.json_data)
    return {'message': f"Source '{req.name}' registered"}

@router.get('/list')
def list_sources():
    return {'sources': _manager.list_sources()}
