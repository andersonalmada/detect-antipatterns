from typing import Any
from observa.framework.base import Source

class DataSource(Source):
    def __init__(self, name: str, json_data: str):
        self.name = name
        self.json_data = json_data
        
    def get_name(self) -> str:
        return self.name

    def load(self) -> Any:
        return self.json_data
