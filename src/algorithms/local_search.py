from abc import ABC, abstractmethod
from src.model.state import State

class LocalSearch(ABC):
      
    @abstractmethod
    def search(self, state: State, *objectives):
        pass

'''
# 1) Steepest-ascent
algo: LocalSearch = HillClimbing(variant="steepest")
final_state: State = algo.search(initial_state, objective)

# 2) Sideways 
algo = HillClimbing(variant="sideways")
final_state: State = algo.search(initial_state, objective, max_sideways=50)

# 3) Stochastic
algo = HillClimbing(variant="stochastic")
final_state: State = algo.search(initial_state, objective, iterations=20)

# 4) Random-restart
algo = HillClimbing(variant="random_restart")
final_state: State = algo.search(initial_state, objective, restarts=30)
'''