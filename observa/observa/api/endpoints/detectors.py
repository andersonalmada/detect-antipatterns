from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from observa.framework.manager import global_manager as manager
from observa.detectors.excessive_alerts import ExcessiveAlertsDetector

router = APIRouter()
_manager = manager

class DetectorRegisterRequest(BaseModel):
    name: str
    module: str = None

@router.post('/register')
def register_detector(req: DetectorRegisterRequest):
    # in this skeleton we only support the built-in ExcessiveAlertsDetector
    if req.name == 'ExcessiveAlerts':
        det = ExcessiveAlertsDetector()
    else:
        raise HTTPException(status_code=400, detail='Unknown detector in skeleton')
    _manager.register_detector(req.name, det)
    return {'message': f"Detector '{req.name}' registered"}

@router.get('/list')
def list_detectors():
    return {'detectors': _manager.list_detectors()}
