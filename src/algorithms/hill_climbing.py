from dataclasses import dataclass
from typing import Any, Tuple, Dict
from .local_search import LocalSearch
from src.model.state import State
import random
import time

@dataclass
class HillClimbing(LocalSearch):

    def __init__(self, v:str, ms:int, mi:int, mr:int):
        self.variant = v
        self.max_sideways = ms
        self.max_iteration = mi
        self.max_restart = mr
         
    def search(self, state: State, *objectives) -> Tuple[State, Dict[str, Any]]: 
        """ entry point search function """

        final_state:State
        execStats:Dict[str, Any]

        start_time = time.time()
        if self.variant == "steepest":
            final_state, execStats = self._steepest(state, *objectives)
        elif self.variant == "sideways":
            ms = 10 if self.max_sideways is None else self.max_sideways
            final_state, execStats = self._sideways(state, ms, *objectives)
        elif self.variant == "stochastic":
            iters = 10 if self.max_iteration is None else self.max_iteration
            final_state, execStats = self._stochastic(state, iters, *objectives)
        elif self.variant == "random_restart":
            rs = 10 if self.max_restart is None else self.max_restart
            final_state, execStats = self._random_restart(state, rs, *objectives)
        else:
            raise ValueError(f"Unknown algorithm type:{self.variant}")
        end_time = time.time()
        execStats['execution_time'] = end_time - start_time

        return final_state, execStats

        
    def _steepest(self, state: State, *objectives) -> Tuple[State, Dict[str, Any]]: 
        """ steepest ascent hill-climbing  """
        current = state.copy()
        initial_state_value = current.state_value
        
        # Plot Hasil
        state_values = [current.state_value]
        iters = [0]

        while True:
            # generate successors
            successors = current.generate_all_successors(*objectives)
            if not successors: 
                break
            
            # compare value
            best_successor = max(successors, key=lambda s: s.state_value)
            state_values.append(best_successor.state_value)
            iters.append(iters[-1]+1)
            
            if best_successor.state_value <= current.state_value: 
                break
            current = best_successor

        # Plot Hasil
        plotting_hasil = {
            'HC Steepent Ascent': {
                'x_label': 'Iterasi',
                'y_label': 'State Value',
                'x_data': iters,
                'y_data': state_values
            }
        }

        stats = {
            'iterations': iters[-1],
            'initial_state_value': initial_state_value,
            'final_state_value': current.state_value,
            'plot_graph': plotting_hasil
        }

        return current, stats
    
    
    def _sideways(self, state: State, MAX_SIDEWAYS: int, *objectives) -> Tuple[State, Dict[str, Any]]: 
        """ sideways variant hill-climbing """
        def _keys(s: State):
            return frozenset(s.assignments.items())
        
        current = state.copy()
        initial_state_value = current.state_value

        visited = {_keys(current)}
        sideways = 0
        
        # Plot Hasil
        state_values = [current.state_value]
        iters = [0]

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

                state_values.append(current.state_value)
                iters.append(iters[-1]+1)
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

                    state_values.append(current.state_value)
                    iters.append(iters[-1]+1)
                    continue
            break

        # Plot Hasil
        plotting_hasil = {
            'HC Sideways': {
                'x_label': 'Iterasi',
                'y_label': 'State Value',
                'x_data': iters,
                'y_data': state_values
            }
        }

        stats = {
            'iterations': iters[-1],
            'initial_state_value': initial_state_value,
            'final_state_value': current.state_value,
            'plot_graph': plotting_hasil
        }

        return current, stats
    
    def _stochastic(self, state: State, iterations: int, *objectives) -> Tuple[State, Dict[str, Any]]: 
        """ stochastic hill-climbing """
        current = state.copy()
        initial_state_value = current.state_value
        
        # Plot Hasil
        state_values = [current.state_value]
        iters = [0]

        steps = 0
        while steps < iterations:
            # # Ini Logikanya salah, gw koreksi dikit ye
            # successors = current.generate_all_successors(*objectives)
            # if not successors:
            #     break
            
            # better = [s for s in successors if s.state_value > current.state_value]
            # if not better:
            #     break
            
            # # random dari better states
            # current = random.choice(better)

            successor = current.generate_random_successor(*objectives)
            better =  successor.state_value > current.state_value
            if better:
                current = successor

            state_values.append(current.state_value)
            iters.append(iters[-1]+1)

            steps += 1

        # Plot Hasil
        plotting_hasil = {
            'HC Stochastic': {
                'x_label': 'Iterasi',
                'y_label': 'State Value',
                'x_data': iters,
                'y_data': state_values
            }
        }

        stats = {
            'iterations': iters[-1],
            'initial_state_value': initial_state_value,
            'final_state_value': current.state_value,
            'plot_graph': plotting_hasil
        }

        return current, stats

    
    
    def _random_restart(self, state: State, restarts:int, *objectives) -> Tuple[State, Dict[str, Any]]: 
        """ random-restart hill-climbing """
        best = None
        state_values = []
        iters = []
        restart = []
        res_iter = []
        res_val = []
        initial_state_value = 0

        found = False
        for i in range (restarts):

            if found:
                break

            current = state.copy()
            current.initialize_random_state(*objectives)
            
            if i == 0:
                # Plot Hasil
                state_values = [current.state_value]
                iters = [0]
                initial_state_value = current.state_value

            restart.append(i)
            res_iter.append(0)
            res_val.append(0)

            iterasi = 0
            while True:
                # generate successors
                successors = current.generate_all_successors(*objectives)
                if not successors: 
                    break
                
                # compare value
                nxt = max(successors, key=lambda s:s.state_value)
                if nxt.state_value <= current.state_value:
                    res_iter[i] = iterasi
                    res_val[i] = current.state_value
                    iterasi = 0
                    break
                current = nxt

                state_values.append(current.state_value)
                iters.append(iters[-1]+1)

                iterasi += 1

                if current.state_value == 0:
                    res_iter[i] = iterasi
                    res_val[i] = current.state_value
                    found = True
                    break
                
            if best is None or current.state_value > best.state_value:
                best = current
        
        # Plot Hasil
        plotting_hasil = {
            'HC Random Restart (All)': {
                'x_label': 'Iterasi',
                'y_label': 'State Value',
                'x_data': iters,
                'y_data': state_values
            },
            'HC Random Restart (Stuck Value)': {
                'x_label': 'Restart',
                'y_label': 'State Value',
                'x_data': restart,
                'y_data': res_val
            },
            'HC Random Restart (Jumlah Iterasi)': {
                'x_label': 'Restart',
                'y_label': 'Jumlah Iterasi',
                'x_data': restart,
                'y_data': res_iter
            }
        }

        stats = {
            'initial_state_value': initial_state_value,
            'final_state_value': best.state_value,
            'restarts': restart[-1],
            'iter_restart': res_iter,
            'plot_graph': plotting_hasil
        }

        return best.copy(), stats
