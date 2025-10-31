from observa.framework.base import Detector
from typing import Any, Dict

class FrutasExcessivas(Detector):
    def detect(self, data: Any) -> Dict:
        excessive = []        
        for item in data:
            try:
                if int(item.get('quantidade', 0)) > 5:
                    excessive.append(item)
            except Exception:
                continue
        
        return {
            'antipattern': self.name,
            'instances': len(excessive),
            'details': excessive
        }
