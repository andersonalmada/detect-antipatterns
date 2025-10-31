from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from observa.framework.orchestrator import global_orchestrator as orchestrator
from observa.framework.manager import global_manager as manager
from observa.sources.data_source import DataSource
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
                source = DataSource(name=source.name, json_data=source.json_data)
                
                detector = manager.get_detector(det)                
                if detector.api_url:
                    detector = RemoteDetector(name=detector.name, api_url=detector.api_url)
                else:
                    module_name, class_name = detector.class_path.rsplit('.', 1)
                    module = importlib.import_module(module_name)
                    cls = getattr(module, class_name)
                    detector = cls(name=detector.name)
                    
                result.append(orchestrator.run(source=source, detector=detector))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return result
