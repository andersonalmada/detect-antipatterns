from fastapi import APIRouter
from pydantic import BaseModel
from observa.framework.manager import global_manager as manager

router = APIRouter()
_manager = manager

class DetectorRegisterRequest(BaseModel):
    name: str
    api_url: str = None

@router.post('/register')
def register_detector(req: DetectorRegisterRequest):
    _manager.register_detector(req.name, api_url=req.api_url)
    return {'message': f"Detector '{req.name}' registered"}

@router.get('/list')
def list_detectors():
    return {'detectors': _manager.list_detectors()}

@router.get('/get')
def get_detector(name: str):
    return {'detector': _manager.get_detector(name)}
