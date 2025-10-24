import json
from typing import Any
from observa.framework.base import Source

class JsonSource(Source):
    def __init__(self, path: str):
        self.path = path

    def load(self) -> Any:
        with open(self.path, 'r', encoding='utf-8') as f:
            return json.load(f)
