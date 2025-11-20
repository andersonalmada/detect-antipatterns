from observa.framework.base import Detector
from typing import Any, Dict

class ExcessiveAlertsDetector(Detector):
    def detect(self, data: Any) -> Dict:
        for item in data:
            if int(item.get('count', 0)) > 100:
                item["exceeded"] = True
            else:
                item["exceeded"] = False
        
        count = sum(1 for x in data if x["exceeded"])       

        response = {
            "analyzed": len(data),
            "detected": count,
            "data": data
        }
    
        return response
