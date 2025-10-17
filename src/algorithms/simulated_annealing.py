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
        import time
        
        start_time = time.time()
        currT = self.initialT 
        currState = state 
        currState.stateValue = currState.countStateValue(*objectives)
        
        initial_stateValue = currState.stateValue
        iterations = 0
        stuck_freq = 0

        # Plotting Hasil
        all_stateValues = [initial_stateValue]
        all_probabilities = [1]
        iterasi = [iterations]
        
        while currT > self.stopT:  # kalo masih di atas suhu berhenti
            successor = currState.generateRandomSuccessor(*objectives) # cari successor (random)
            _deltaE = successor.stateValue - currState.stateValue # hitung delta E = E_successor - E_curr 

            if _deltaE > 0:  # Successor lebih baik
                probabability = 1.0  # Selalu diterima (100%)
                currState = successor # langsung pindah ke successor
            else:  # Successor lebih buruk, terima dengan probabilitas tertentu
                probabability = self._acceptance_probability(_deltaE, currT)
                _accept = random.uniform(0, 1) # random float antara 0 dan 1
                stuck_freq += 1
                if _accept < probabability: # kalo _deltaE nya ada 
                    currState = successor
            
            # Turunkan temperature
            currT *= self.coolingRate
            iterations += 1

            # Update Plotting Hasil
            all_stateValues.append(currState.stateValue)
            all_probabilities.append(probabability)
            iterasi.append(iterations)
            
            # Progress indicator setiap 100 iterasi
            # if iterations % 100 == 0:
            #     print(f"   Iterasi {iterations:,}, Temperature: {currT:.2f}, State Value: {currState.stateValue:.2f}")
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # print(f"Simulated Annealing selesai!")
        # print(f"   Final Temperature: {currT:.4f}")
        # print(f"   Final State Value: {currState.stateValue:.2f}")
        # print(f"   Total Iterasi: {iterations:,}")
        # print(f"   Waktu Eksekusi: {execution_time:.3f} detik")
        
        # Plotting Hasil
        plotting_hasil = {
            'State Value': {
                'x_label': 'Iterasi',
                'y_label': 'State Value',
                'x_data': iterasi,
                'y_data': all_stateValues
            },
            'Acceptance Probability': {
                'x_label': 'Iterasi',
                'y_label': 'Acceptance Probability',
                'x_data': iterasi,
                'y_data': all_probabilities
            }
        }

        # Return state dan statistik
        stats = {
            'algorithm_name': 'Simulated Annealing',
            'initial_temp': self.initialT,
            'cooling_rate': self.coolingRate,
            'stop_temp': self.stopT,
            'execution_time': execution_time,
            'iterations': iterations,
            'stuck_freq': stuck_freq,
            'initial_stateValue': initial_stateValue,
            'final_stateValue': currState.stateValue,
            'plot_graph': plotting_hasil
        }
        
        return currState, stats
    
    def _acceptance_probability(self, _deltaE: float, temperature: float) -> float:
        # CEK INI BROOOO 
        # baru ngecek 
        if temperature <= 0:
            return 0.0 
        
        # Untuk _deltaE < 0, exp(_deltaE/T) memberikan probabilitas 0-1
        # Semakin besar |_deltaE| (semakin buruk), semakin kecil probabilitas
        # Semakin tinggi temperature, semakin besar probabilitas
        return math.exp(_deltaE / temperature)
        
    def setInitialTemperature(self, initialT: float):
        self.initialT = initialT
    
    def setCoolingRate(self, coolingRate: float):
        self.coolingRate = coolingRate
    
    def setStopTemperature(self, stopT: float):
        self.stopT = stopT
    