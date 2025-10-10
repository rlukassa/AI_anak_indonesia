from types import Any
from .local_search import LocalSearch
from src.model.state import State

class HillClimbing(LocalSearch):
    
    def __init__(self, variant: str = "steepest", max_iters: int = 1000, restarts: int = 10):
        self.variant = variant
        self.max_iters = max_iters
        self.restarts = restarts
         
    def search(self, state: State, *objectives) -> Any: 
        """ entry point search function """
        if self.variant == "steepest":
            return self._steepest(state, *objectives)
        if self.variant == "sideways":
            return self._sideways(state, *objectives)
        if self.variant == "stochastic":
            return self._strochastic(state, *objectives)
        if self.variant == "random_restart":
            return self._random_restart(state, *objectives)
        
    def _steepest(self, state: State, *objectives) -> State: 
        """ steepest ascent hill-climbing  """
        current = state.copy()
        current.initialize_random_state(*objectives)
        while True:
            successors = current.generate_all_successors(*objectives)
            
            if not successors: 
                return current
            
            best_successor = max(successors, key=lambda s: s.state_value)
            
            if best_successor.state_value <= current.state_value: 
                return current
            current = best_successor
            
    def _sideways(self, state: State, *objectives) -> State:
        """ sideways hill-climbing """
        current = state.copy()
        current.initialize_random_state(*objectives)
        
        visited = set()
        visited.add(frozenset(current.assignments.items()))
        
        while True: 
            successors = current.generate_all_successors(*objectives)
            if not successors: 
                return current
            
            found = False
            for s in successors:
                skey = frozenset(s.assignments.items())
                if skey in visited or s.state_value < current.state_value:
                    continue
                current = s
                visited.add(skey)
                found = True
                break
            
            if not found: 
                return current
                
        
                
                