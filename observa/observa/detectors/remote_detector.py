from observa.framework.base import Detector
from typing import Any, Dict
import requests

class RemoteDetector(Detector):
    def detect(self, data: Any) -> Dict:
        response = requests.post(self.api_url, json=data)
        response.raise_for_status()
        return response.json()
