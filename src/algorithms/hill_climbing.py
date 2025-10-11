from dataclasses import dataclass
from typing import Any
from .local_search import LocalSearch
from src.model.state import State
import random

@dataclass
class HillClimbing(LocalSearch):
    variant:str = "steepest"
         
    def search(self, state: State, *objectives, max_sideways=None, restarts=None, iterations=None) -> Any: 
        """ entry point search function """
        if self.variant == "steepest":
            return self._steepest(state, *objectives)
        if self.variant == "sideways":
            ms = 10 if max_sideways is None else max_sideways
            return self._sideways(state, ms, *objectives)
        if self.variant == "stochastic":
            iters = 10 if iterations is None else iterations
            return self._stochastic(state, iters, *objectives)
        if self.variant == "random_restart":
            rs = 10 if restarts is None else restarts
            return self._random_restart(state, rs, *objectives)
        else:
            raise ValueError(f"Unknown algorithm type:{self.variant}")
        
        
    def _steepest(self, state: State, *objectives) -> State: 
        """ steepest ascent hill-climbing  """
        current = state.copy()
        current.initialize_random_state(*objectives)
        
        while True:
            # generate successors
            successors = current.generate_all_successors(*objectives)
            if not successors: 
                break
            
            # compare value
            best_successor = max(successors, key=lambda s: s.state_value)
            if best_successor.state_value <= current.state_value: 
                break
            current = best_successor
        return current
    
    
    def _sideways(self, state: State, MAX_SIDEWAYS: int, *objectives) -> State:
        """ sideways variant hill-climbing """
        def _keys(s: State):
            return frozenset(s.assignments.items())
        
        current = state.copy()
        current.initialize_random_state(*objectives)

        visited = {_keys(current)}
        sideways = 0

        while True:
            # generate successors
            successors = current.generate_all_successors(*objectives)
            if not successors:
                break

            current_value = current.state_value
            best_value = max(s.state_value for s in successors)

            # better value
            if best_value > current_value:
                better_states = [s for s in successors if s.state_value == best_value]
                current = random.choice(better_states)
                visited.add(_keys(current))
                sideways = 0
                continue

            # same value
            if best_value == current_value and sideways < MAX_SIDEWAYS:
                equal_unvisited = [
                    s for s in successors
                    if s.state_value == current_value and _keys(s) not in visited
                ]
                if equal_unvisited:
                    current = random.choice(equal_unvisited)
                    visited.add(_keys(current))
                    sideways += 1
                    continue
            break
        return current
    
    
    def _stochastic(self, state: State, iterations:int, *objectives) -> State:
        """ stochastic hill-climbing """
        current = state.copy()
        current.initialize_random_state(*objectives)
        
        for _ in range(iterations):
            # generate random successor
            successor = current.generate_random_successor(*objectives)
            
            # move if better
            if successor.state_value > current.state_value:
                current = successor 
        return current
    
    
    def _random_restart(self, state: State, restarts:int, *objectives) -> State:
        """ random-restart hill-climbing """
        best = None
        
        for _ in range (restarts):
            current = state.copy()
            current.initialize_random_state(*objectives)
            
            while True:
                # generate successors
                successors = current.generate_all_successors(*objectives)
                if not successors: 
                    break
                
                # compare value
                nxt = max(successors, key=lambda s:s.state_value)
                if nxt.state_value <= current.state_value:
                    break
                current = nxt
                
            if best is None or current.state_value > best.state_value:
                best = current
                
        return best.copy()
