from observa.database.models import SourceModel, DetectorModel
from observa.database.database import Base, engine
from observa.sources.json_source import JsonSource
from observa.framework.manager import global_manager as manager
from observa.framework.base import Source, Detector

from dotenv import load_dotenv
import time
from typing import Dict, Any
import os

class Orchestrator:
    def load(self):
        print("\n####### Observa Framework #######\n")
        
        load_dotenv()
        print("Loaded environment variables ...")

        SOURCES_LOCAL_NAME = os.getenv("SOURCES_LOCAL_NAME", "")
        SOURCES_LOCAL_PATH = os.getenv("SOURCES_LOCAL_PATH", "")
        DETECTOR_LOCAL_NAME = os.getenv("DETECTOR_LOCAL_NAME", "")
        DETECTOR_LOCAL_PATH = os.getenv("DETECTOR_LOCAL_PATH", "")

        Base.metadata.create_all(bind=engine)
        print("Database loaded ...")
            
        _names_source = [item.strip() for item in SOURCES_LOCAL_NAME.split(',')]
        _paths_source = [item.strip() for item in SOURCES_LOCAL_PATH.split(',')]

        print("\n####### Available sources #######\n")

        for i, value in enumerate(_names_source):
            if not manager.get_source(value):
                _json = JsonSource(name=value,path=_paths_source[i])        
                manager.register_source(_json)
                print(value + " - New !!")
            else:
                print(value)
            
        for item in set(manager.list_sources()).symmetric_difference(_names_source):
            print(item)

        _names_detectors = [item.strip() for item in DETECTOR_LOCAL_NAME.split(',')]
        _path_detectors = [item.strip() for item in DETECTOR_LOCAL_PATH.split(',')]

        print("\n####### Available detectors #######\n")

        for i, value in enumerate(_names_detectors):
            if not manager.get_detector(value):
                manager.register_detector(value, _path_detectors[i])
                print(value + " - New !!")
            else: 
                print(value)

        for item in set(manager.list_detectors()).symmetric_difference(_names_detectors):
            print(item)
                
        print("\nReady !!!\n")
        
    def run(self, detector: Detector, source: Source) -> Dict[str, Any]: 
        data = source.load()
        start = time.time()        
        result = detector.detect(data)        
        end = time.time()
        result.setdefault('source', source.name)        
        result.setdefault('detector', detector.name)
        result.setdefault('execution_time_ms', round((end - start) * 1000, 3))
        return result
    
global_orchestrator = Orchestrator()    