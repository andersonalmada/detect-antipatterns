from fastapi import APIRouter
from pydantic import BaseModel
from observa.framework.manager import global_manager as manager
from observa.sources.data_source import DataSource
from typing import Any

router = APIRouter()
_manager = manager

class SourceRegisterRequest(BaseModel):
    name: str
    json_data: Any

@router.post('/register')
def register_source(req: SourceRegisterRequest):
    source = DataSource(name=req.name, json_data=req.json_data)    
    _manager.register_source(source)
    return {'message': f"Source '{source.name}' registered"}

@router.get('/list')
def list_sources():
    return {'sources': _manager.list_sources()}

@router.get('/get')
def get_source(name: str):
    return {'source': _manager.get_source(name)}
