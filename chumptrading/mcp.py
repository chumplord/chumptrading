from typing import Dict

from pydantic import BaseModel


class Strategy(BaseModel):
    name: str
    strategy: str


class StrategyMCP:
    def __init__(self):
        self.strategies: Dict[str, Strategy] = {}

    def add_strategy(self, name: str, strategy: str):
        self.strategies[name.lower()] = Strategy(name=name, strategy=strategy)
        return {'message': f'Added strategy {name}'}

    def update_strategy(self, name, strategy):
        key = name.lower()
        if key in self.strategies:
            self.strategies[key] = Strategy(name=name, strategy=strategy)
        else:
            self.add_strategy(name, strategy)

    def list_strategies(self):
        return self.strategies.values()
