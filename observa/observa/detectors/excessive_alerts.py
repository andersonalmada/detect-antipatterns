from observa.framework.base import Detector
from typing import Any, Dict

class ExcessiveAlertsDetector(Detector):
    def detect(self, data: Any) -> Dict:
        # Expecting data to be a list of alerts with 'alert_name' and 'count'
        threshold = 100
        excessive = []
        if isinstance(data, list):
            for item in data:
                try:
                    if int(item.get('count', 0)) > threshold:
                        excessive.append(item)
                except Exception:
                    continue
        return {
            'antipattern': 'Excessive Alerts',
            'instances': len(excessive),
            'details': excessive
        }
