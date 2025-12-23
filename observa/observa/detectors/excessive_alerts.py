from observa.framework.base import Detector
from typing import Any, Dict

class ExcessiveAlertsDetector(Detector):
    def detect(self, data: Any) -> Dict:
        for item in data:
            if int(item.get('count', 0)) > 10:
                item["detected"] = True
                item["reason"] = "detect_limit"
            else:
                item["detected"] = False
                item["reason"] = ""
        
        count = sum(1 for x in data if x["detected"])       

        response = {
            "analyzed": len(data),
            "detected": count,
            "data": data
        }
    
        return response
