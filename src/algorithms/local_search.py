from abc import ABC, abstractmethod
from src.model.state import State

class LocalSearch(ABC):
    @abstractmethod
    def search(self, state: State, *objectives):
        pass
    