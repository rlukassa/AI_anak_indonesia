from src.model.state import State  # import class State untuk representasi jadwal
from src.algorithms.local_search import LocalSearch  # import parent class LocalSearch
from typing import Tuple, Dict, Any  # import type hints untuk return value
import time  # import untuk tracking waktu eksekusi

class HillClimbing(LocalSearch):
    """Implementasi algoritma Hill Climbing dengan berbagai varian"""
    
    def __init__(self, variant: str = "steepest", maxIterations: int = 1000, restarts: int = 10):
        self.variant = variant  # jenis variant HC: steepest, sideways, stochastic, random_restart
        self.maxIterations = maxIterations  # maksimum iterasi per run algoritma
        self.restarts = restarts  # jumlah restart untuk random restart variant
         
    def search(self, state: State, *objectives) -> Tuple[State, Dict[str, Any]]: 
        """Entry point untuk menjalankan Hill Climbing dengan tracking statistik"""
        startTime = time.time()  # catat waktu mulai eksekusi
        
        if self.variant == "steepest":  # pilih steepest ascent hill climbing
            result, stats = self._steepestAscentSearch(state, *objectives)
        elif self.variant == "sideways":  # pilih sideways move hill climbing
            result, stats = self._sidewaysMoveSearch(state, *objectives)
        elif self.variant == "stochastic":  # pilih stochastic hill climbing
            result, stats = self._stochasticSearch(state, *objectives)
        elif self.variant == "random_restart":  # pilih random restart hill climbing
            result, stats = self._randomRestartSearch(state, *objectives)
        else:  # jika variant tidak dikenali, default ke steepest ascent
            result, stats = self._steepestAscentSearch(state, *objectives)
        
        endTime = time.time()  # catat waktu selesai eksekusi
        executionTime = endTime - startTime  # hitung total waktu eksekusi
        
        # tambahkan info waktu eksekusi ke statistik
        stats['execution_time'] = executionTime  # simpan waktu eksekusi dalam detik
        stats['algorithm_name'] = f"Hill Climbing ({self.variant})"  # nama algoritma dengan variant
        
        return result, stats  # return state terbaik dan statistik lengkap
        
    def _steepestAscentSearch(self, state: State, *objectives) -> Tuple[State, Dict[str, Any]]: 
        """Steepest ascent hill climbing - pilih successor dengan nilai terbaik"""
        print(f"Memulai Hill Climbing (Steepest Ascent)...") # Info algoritma dimulai
        
        currentState = state.copy() # Copy state awal untuk manipulasi
        currentState.initialize_random_state(*objectives) # Inisialisasi dengan assignment random
        initialStateValue = currentState.state_value # Simpan nilai state awal
        
        iterations = 0 # Counter untuk jumlah iterasi
        
        print(f"   Initial State Value: {initialStateValue:.2f}") # Tampilkan nilai awal
        
        while iterations < self.maxIterations: # Loop sampai mencapai maksimum iterasi
            successors = currentState.generate_all_successors(*objectives) # Generate semua successor
            
            if not successors: # Jika tidak ada successor yang bisa di-generate
                print("   Tidak ada successor yang valid, algoritma berhenti") # Info tidak ada successor
                break # Keluar dari loop optimasi
            
            bestSuccessor = max(successors, key=lambda s: s.state_value) # Pilih successor terbaik
            
            if bestSuccessor.state_value <= currentState.state_value: # Jika successor tidak lebih baik
                print("   Mencapai local maximum, algoritma berhenti") # Info mencapai local maximum
                break # Keluar karena tidak ada perbaikan
            
            currentState = bestSuccessor # Pindah ke successor terbaik
            iterations += 1 # Increment counter iterasi
            
            # Progress indicator setiap 50 iterasi
            if iterations % 50 == 0: # Tampilkan progress setiap 50 iterasi
                print(f"   Iterasi {iterations}, State Value: {currentState.state_value:.2f}") # Info progress
        
        print(f"Hill Climbing (Steepest Ascent) selesai!") # Info algoritma selesai
        print(f"   Final State Value: {currentState.state_value:.2f}") # Tampilkan nilai akhir
        print(f"   Total Iterasi: {iterations}") # Tampilkan total iterasi
        
        # Buat dictionary statistik untuk output
        stats = {
            'variant': 'steepest', # Jenis variant yang digunakan
            'max_iterations': self.maxIterations, # Maksimum iterasi yang diset
            'iterations': iterations, # Jumlah iterasi yang benar-benar dilakukan
            'initial_state_value': initialStateValue, # Nilai state awal
            'final_state_value': currentState.state_value # Nilai state akhir
        }
        
        return currentState, stats # Return state terbaik dan statistiknya
            
    def _sidewaysMoveSearch(self, state: State, *objectives) -> Tuple[State, Dict[str, Any]]:
        """Sideways move hill climbing - terima move yang sama nilainya"""
        print(f"Memulai Hill Climbing (Sideways Move)...") # Info algoritma dimulai
        
        currentState = state.copy() # Copy state awal untuk manipulasi
        currentState.initialize_random_state(*objectives) # Inisialisasi dengan assignment random
        initialStateValue = currentState.state_value # Simpan nilai state awal
        
        visitedStates = set() # Set untuk menyimpan state yang sudah dikunjungi
        visitedStates.add(frozenset(currentState.assignments.items())) # Tambahkan state awal ke visited
        
        iterations = 0 # Counter untuk jumlah iterasi
        sidewaysMoves = 0 # Counter untuk jumlah sideways move
        
        print(f"   Initial State Value: {initialStateValue:.2f}") # Tampilkan nilai awal
        
        while iterations < self.maxIterations: # Loop sampai mencapai maksimum iterasi
            successors = currentState.generate_all_successors(*objectives) # Generate semua successor
            
            if not successors: # Jika tidak ada successor yang bisa di-generate
                print("   Tidak ada successor yang valid, algoritma berhenti") # Info tidak ada successor
                break # Keluar dari loop optimasi
            
            foundBetterMove = False # Flag untuk cek apakah ada move yang lebih baik
            
            for successor in successors: # Iterasi semua successor
                successorKey = frozenset(successor.assignments.items()) # Buat key untuk cek visited
                
                if successorKey in visitedStates: # Skip jika state sudah pernah dikunjungi
                    continue # Lanjut ke successor berikutnya
                
                if successor.state_value > currentState.state_value: # Jika ada successor yang lebih baik
                    currentState = successor # Pindah ke successor yang lebih baik
                    visitedStates.add(successorKey) # Tambahkan ke visited states
                    foundBetterMove = True # Set flag ada move yang lebih baik
                    break # Keluar dari loop successor
                elif successor.state_value == currentState.state_value: # Jika nilai sama (sideways move)
                    currentState = successor # Terima sideways move
                    visitedStates.add(successorKey) # Tambahkan ke visited states
                    sidewaysMoves += 1 # Increment counter sideways move
                    foundBetterMove = True # Set flag ada move (walaupun sideways)
                    break # Keluar dari loop successor
            
            if not foundBetterMove: # Jika tidak ada move yang bisa dilakukan
                print("   Tidak ada move yang valid, algoritma berhenti") # Info tidak ada move
                break # Keluar dari loop optimasi
            
            iterations += 1 # Increment counter iterasi
            
            # Progress indicator setiap 50 iterasi
            if iterations % 50 == 0: # Tampilkan progress setiap 50 iterasi
                print(f"   Iterasi {iterations}, State Value: {currentState.state_value:.2f}, Sideways: {sidewaysMoves}") # Info progress
        
        print(f"Hill Climbing (Sideways Move) selesai!") # Info algoritma selesai
        print(f"   Final State Value: {currentState.state_value:.2f}") # Tampilkan nilai akhir
        print(f"   Total Iterasi: {iterations}") # Tampilkan total iterasi
        print(f"   Sideways Moves: {sidewaysMoves}") # Tampilkan jumlah sideways move
        
        # Buat dictionary statistik untuk output
        stats = {
            'variant': 'sideways', # Jenis variant yang digunakan
            'max_iterations': self.maxIterations, # Maksimum iterasi yang diset
            'iterations': iterations, # Jumlah iterasi yang benar-benar dilakukan
            'sideways_moves': sidewaysMoves, # Jumlah sideways move yang dilakukan
            'initial_state_value': initialStateValue, # Nilai state awal
            'final_state_value': currentState.state_value # Nilai state akhir
        }
        
        return currentState, stats # Return state terbaik dan statistiknya
        
    def _stochasticSearch(self, state: State, *objectives) -> Tuple[State, Dict[str, Any]]:
        """Stochastic hill climbing - pilih successor secara probabilistik berdasarkan nilai"""
        import random
        
        print(f"Memulai Hill Climbing (Stochastic)...") # Info algoritma dimulai
        
        currentState = state.copy() # Copy state awal untuk manipulasi
        currentState.initialize_random_state(*objectives) # Inisialisasi dengan assignment random
        initialStateValue = currentState.state_value # Simpan nilai state awal
        
        iterations = 0 # Counter untuk jumlah iterasi
        stochasticMoves = 0 # Counter untuk jumlah stochastic move
        
        print(f"   Initial State Value: {initialStateValue:.2f}") # Tampilkan nilai awal
        
        while iterations < self.maxIterations: # Loop sampai mencapai maksimum iterasi
            successors = currentState.generate_all_successors(*objectives) # Generate semua successor
            
            if not successors: # Jika tidak ada successor yang bisa di-generate
                print("   Tidak ada successor yang valid, algoritma berhenti") # Info tidak ada successor
                break # Keluar dari loop optimasi
            
            # Filter successor yang lebih baik atau sama
            betterSuccessors = [s for s in successors if s.state_value >= currentState.state_value]
            
            if not betterSuccessors: # Jika tidak ada successor yang lebih baik
                print("   Tidak ada successor yang lebih baik, algoritma berhenti") # Info tidak ada perbaikan
                break # Keluar karena tidak ada perbaikan
            
            # Pilih successor secara probabilistik berdasarkan nilai
            if len(betterSuccessors) == 1:
                chosenSuccessor = betterSuccessors[0] # Jika hanya ada satu pilihan
            else:
                # Buat probability distribution berdasarkan nilai state
                minValue = min(s.state_value for s in betterSuccessors)
                weights = [s.state_value - minValue + 1 for s in betterSuccessors] # Normalisasi weight
                chosenSuccessor = random.choices(betterSuccessors, weights=weights)[0] # Pilih berdasarkan weight
                stochasticMoves += 1
            
            if chosenSuccessor.state_value <= currentState.state_value: # Jika tidak ada perbaikan
                print("   Mencapai local maximum, algoritma berhenti") # Info mencapai local maximum
                break # Keluar karena tidak ada perbaikan
                
            currentState = chosenSuccessor # Pindah ke successor terpilih
            iterations += 1 # Increment counter iterasi
            
            # Progress indicator setiap 50 iterasi
            if iterations % 50 == 0: # Tampilkan progress setiap 50 iterasi
                print(f"   Iterasi {iterations}, State Value: {currentState.state_value:.2f}, Stochastic Moves: {stochasticMoves}") # Info progress
        
        print(f"Hill Climbing (Stochastic) selesai!") # Info algoritma selesai
        print(f"   Final State Value: {currentState.state_value:.2f}") # Tampilkan nilai akhir
        print(f"   Total Iterasi: {iterations}") # Tampilkan total iterasi
        print(f"   Stochastic Moves: {stochasticMoves}") # Tampilkan jumlah stochastic move
        
        # Buat dictionary statistik untuk output
        stats = {
            'variant': 'stochastic', # Jenis variant yang digunakan
            'max_iterations': self.maxIterations, # Maksimum iterasi yang diset
            'iterations': iterations, # Jumlah iterasi yang benar-benar dilakukan
            'stochastic_moves': stochasticMoves, # Jumlah stochastic move yang dilakukan
            'initial_state_value': initialStateValue, # Nilai state awal
            'final_state_value': currentState.state_value # Nilai state akhir
        }
        
        return currentState, stats # Return state terbaik dan statistiknya
    
    def _randomRestartSearch(self, state: State, *objectives) -> Tuple[State, Dict[str, Any]]:
        """Random restart hill climbing - jalankan multiple steepest ascent dari state awal berbeda"""
        print(f"Memulai Hill Climbing (Random Restart) dengan {self.restarts} restart...") # Info algoritma dimulai
        
        bestState = None # State terbaik yang ditemukan
        bestStateValue = float('-inf') # Nilai terbaik yang ditemukan (awalnya -infinity)
        totalIterations = 0 # Total iterasi semua restart
        allStats = [] # Statistik dari semua restart
        
        for restart in range(self.restarts): # Loop untuk setiap restart
            print(f"\n   Restart {restart + 1}/{self.restarts}:") # Info restart ke-n
            
            # Buat state baru untuk restart ini
            restartState = state.copy() # Copy state awal
            restartState.initialize_random_state(*objectives) # Random initialization baru
            
            # Jalankan steepest ascent hill climbing
            resultState, stats = self._steepestAscentSearch(restartState, *objectives)
            
            totalIterations += stats['iterations'] # Akumulasi total iterasi
            allStats.append(stats) # Simpan statistik restart ini
            
            # Update best state jika ditemukan yang lebih baik
            if resultState.state_value > bestStateValue:
                bestState = resultState # Update state terbaik
                bestStateValue = resultState.state_value # Update nilai terbaik
                print(f"   Restart {restart + 1}: NEW BEST! State Value: {bestStateValue:.2f}") # Info new best
            else:
                print(f"   Restart {restart + 1}: State Value: {resultState.state_value:.2f}") # Info hasil restart
        
        print(f"\nHill Climbing (Random Restart) selesai!") # Info algoritma selesai
        print(f"   Best State Value: {bestStateValue:.2f}") # Tampilkan nilai terbaik
        print(f"   Total Restarts: {self.restarts}") # Tampilkan jumlah restart
        print(f"   Total Iterasi: {totalIterations}") # Tampilkan total iterasi semua restart
        
        # Buat dictionary statistik gabungan
        stats = {
            'variant': 'random_restart', # Jenis variant yang digunakan
            'restarts': self.restarts, # Jumlah restart yang dilakukan
            'max_iterations': self.maxIterations, # Maksimum iterasi per restart
            'total_iterations': totalIterations, # Total iterasi semua restart
            'initial_state_value': allStats[0]['initial_state_value'] if allStats else 0, # Nilai state awal restart pertama
            'final_state_value': bestStateValue, # Nilai state terbaik yang ditemukan
            'all_restart_stats': allStats # Statistik detil dari semua restart
        }
        
        return bestState, stats # Return state terbaik dan statistik lengkap