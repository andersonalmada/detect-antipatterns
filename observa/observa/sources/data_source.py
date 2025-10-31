from typing import Any
from observa.framework.base import Source

class DataSource(Source):
    def load(self) -> Any:
        return self.json_data
