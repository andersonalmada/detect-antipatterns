from observa.framework.base import Detector
from typing import Any, Dict

class FrutasExcessivas(Detector):
    def detect(self, data: Any) -> Dict:
        for item in data:
            try:
                if int(item.get('quantidade', 0)) > 5:
                    item["exceeded"] = True
                else:
                    item["exceeded"] = False
            except Exception:
                continue
            
        count = sum(1 for x in data if x["exceeded"])      
        
        return {
            'analyzed': len(data),
            'detected': count,
            'data': data
        }
