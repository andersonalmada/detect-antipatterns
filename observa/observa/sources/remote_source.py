from observa.framework.base import Source
from typing import Any
import requests

class RemoteSource(Source):
    def load(self) -> Any:
        response = requests.get(self.api_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro {response.status_code}: {response.text}")