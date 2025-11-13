from observa.framework.base import Detector
from typing import Any, Dict
import requests

class RemoteDetector(Detector):
    def detect(self, data: Any) -> Dict:
        response = requests.post(self.api_url, json=data)
        if response.status_code == 200:
            return response.json()
        else:            
            print(f"Erro {response.status_code}: {response.text}")
