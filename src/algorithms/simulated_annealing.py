from src.model.state import State
from src.algorithms.local_search import LocalSearch
from typing import Tuple, Dict, Any
import random 
import math  # Import math untuk exponential function

class SA(LocalSearch): 
    def __init__(self, initialT: float, coolingRate: float, stopT: float): 
        self.initialT = initialT  # suhu awal
        self.coolingRate = coolingRate  # laju pendinginan
        self.stopT = stopT  # suhu yang menghentikan algoritma
    
    def search(self, state: State, *objectives) -> Tuple[State, Dict[str, Any]]: 
        """Search dengan tracking statistik untuk output"""
        import time
        
        start_time = time.time()
        currT = self.initialT 
        currState = state 
        currState.state_value = currState.count_state_value(*objectives)
        
        initial_state_value = currState.state_value
        iterations = 0
        
        print(f"Memulai Simulated Annealing...")
        print(f"   Initial Temperature: {self.initialT}")
        print(f"   Initial State Value: {initial_state_value:.2f}")
        
        while currT > self.stopT:  # kalo masih di atas suhu berhenti
            successor = currState.generate_random_successor(*objectives) # cari successor (random)
            _deltaE = successor.state_value - currState.state_value # hitung delta E = E_successor - E_curr 

            if _deltaE > 0:  # Successor lebih baik
                currState = successor # langsung pindah ke successor
            else:  # Successor lebih buruk, terima dengan probabilitas tertentu
                _accept = random.uniform(0, 1) # random float antara 0 dan 1
                if _accept < self._acceptance_probability(_deltaE, currT): # kalo _deltaE nya ada 
                    currState = successor
            
            # Turunkan temperature
            currT *= self.coolingRate
            iterations += 1
            
            # Progress indicator setiap 100 iterasi
            if iterations % 100 == 0:
                print(f"   Iterasi {iterations:,}, Temperature: {currT:.2f}, State Value: {currState.state_value:.2f}")
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"Simulated Annealing selesai!")
        print(f"   Final Temperature: {currT:.4f}")
        print(f"   Final State Value: {currState.state_value:.2f}")
        print(f"   Total Iterasi: {iterations:,}")
        print(f"   Waktu Eksekusi: {execution_time:.3f} detik")
        
        # Return state dan statistik
        stats = {
            'algorithm_name': 'Simulated Annealing',
            'initial_temp': self.initialT,
            'cooling_rate': self.coolingRate,
            'stop_temp': self.stopT,
            'execution_time': execution_time,
            'iterations': iterations,
            'initial_state_value': initial_state_value,
            'final_state_value': currState.state_value
        }
        
        return currState, stats
    
    def _acceptance_probability(self, _deltaE: float, temperature: float) -> float:
        # formula Boltzmann, ya kek umumnya lah
        # # Bad move, hitung probabilitas berdasarkan Boltzmann distribution
        return math.exp(_deltaE / temperature)  # e^(_deltaE/T)
        
    def setInitialTemperature(self, initialT: float):
        self.initialT = initialT
    
    def setCoolingRate(self, coolingRate: float):
        self.coolingRate = coolingRate
    
    def setStopTemperature(self, stopT: float):
        self.stopT = stopT
    