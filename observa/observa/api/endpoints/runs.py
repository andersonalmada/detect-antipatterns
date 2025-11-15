from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from observa.framework.orchestrator import global_orchestrator as orchestrator
from observa.framework.manager import global_manager as manager
from observa.sources.data_source import DataSource
from observa.sources.remote_source import RemoteSource
from observa.detectors.remote_detector import RemoteDetector
from typing import List
import importlib

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
                source = manager.get_source(src)                
                if source.api_url:
                    sourceObj = RemoteSource(name=source.name, api_url=source.api_url)    
                else:
                    sourceObj = DataSource(name=source.name, json_data=source.json_data)
                
                detector = manager.get_detector(det)                
                if detector.api_url:
                    detectorObj = RemoteDetector(name=detector.name, api_url=detector.api_url)
                else:
                    module_name, class_name = detector.class_path.rsplit('.', 1)
                    module = importlib.import_module(module_name)
                    cls = getattr(module, class_name)
                    detectorObj = cls(name=detector.name)

                resultTemp = orchestrator.run(source=sourceObj, detector=detectorObj)                    
                manager.register_history(source_id=source.id, detector_id=detector.id,result=resultTemp)
                    
                result.append(resultTemp)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return result

@router.get('/history')
def execute_history(source: str, detector: str):
    source = manager.get_source(source)
    detector = manager.get_detector(detector)
    return manager.get_history(source_id=source.id,detector_id=detector.id)
    
    