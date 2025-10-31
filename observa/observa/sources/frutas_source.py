from typing import Any
from observa.framework.base import Source

class FrutasLocal(Source):
    def load(self) -> Any:
        frutas = [
            {"fruta": "Maçã", "quantidade": 10},
            {"fruta": "Banana", "quantidade": 8},
            {"fruta": "Laranja", "quantidade": 12},
            {"fruta": "Manga", "quantidade": 5},
            {"fruta": "Abacaxi", "quantidade": 3},
            {"fruta": "Morango", "quantidade": 20}
        ]
        
        return frutas
