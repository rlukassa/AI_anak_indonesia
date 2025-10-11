from src.model.state import State  # import class State untuk representasi jadwal
from src.algorithms.local_search import LocalSearch  # import parent class LocalSearch
from typing import Tuple, Dict, Any, List  # import type hints untuk return value dan populasi
import random  # import untuk operasi random dalam GA
import time  # import untuk tracking waktu eksekusi

class GeneticAlgorithm(LocalSearch):
    """Implementasi algoritma Genetic Algorithm untuk optimasi penjadwalan"""
    
    def __init__(self, populationSize: int = 50, maxGenerations: int = 100, 
                 crossoverRate: float = 0.8, mutationRate: float = 0.1,
                 selectionMethod: str = "tournament", tournamentSize: int = 3):
        self.populationSize = populationSize  # ukuran populasi individu
        self.maxGenerations = maxGenerations  # maksimum generasi yang akan dijalankan
        self.crossoverRate = crossoverRate  # probabilitas crossover (0.0 - 1.0)
        self.mutationRate = mutationRate  # probabilitas mutasi (0.0 - 1.0)
        self.selectionMethod = selectionMethod  # metode seleksi: tournament, roulette
        self.tournamentSize = tournamentSize  # ukuran tournament untuk tournament selection
    
    def search(self, state: State, *objectives) -> Tuple[State, Dict[str, Any]]:
        """Entry point untuk menjalankan Genetic Algorithm dengan tracking statistik"""
        print(f"Memulai Genetic Algorithm...") # Info algoritma dimulai
        startTime = time.time() # Catat waktu mulai eksekusi
        
        # Inisialisasi populasi awal
        population = self._initializePopulation(state, *objectives) # Buat populasi random
        
        bestIndividual = max(population, key=lambda ind: ind.state_value) # Cari individu terbaik
        initialBestValue = bestIndividual.state_value # Simpan nilai terbaik awal
        
        print(f"   Population Size: {self.populationSize}") # Tampilkan ukuran populasi
        print(f"   Initial Best Value: {initialBestValue:.2f}") # Tampilkan nilai terbaik awal
        
        generationsWithoutImprovement = 0 # Counter generasi tanpa perbaikan
        maxGenerationsWithoutImprovement = 20 # Maksimum generasi tanpa perbaikan sebelum stop
        
        # Evolusi populasi selama beberapa generasi
        for generation in range(self.maxGenerations): # Loop untuk setiap generasi
            
            # Evaluasi fitness seluruh populasi
            for individual in population: # Hitung ulang fitness setiap individu
                individual.state_value = individual.count_state_value(*objectives) # Update fitness value
            
            # Cari individu terbaik di generasi ini
            currentBest = max(population, key=lambda ind: ind.state_value) # Individu dengan fitness tertinggi
            
            # Cek apakah ada perbaikan dari generasi sebelumnya
            if currentBest.state_value > bestIndividual.state_value: # Jika ada perbaikan
                bestIndividual = currentBest.copy() # Simpan individu terbaik baru
                generationsWithoutImprovement = 0 # Reset counter tanpa perbaikan
            else: # Jika tidak ada perbaikan
                generationsWithoutImprovement += 1 # Increment counter tanpa perbaikan
            
            # Progress indicator setiap 10 generasi
            if generation % 10 == 0: # Tampilkan progress setiap 10 generasi
                avgFitness = sum(ind.state_value for ind in population) / len(population) # Rata-rata fitness
                print(f"   Generation {generation}, Best: {currentBest.state_value:.2f}, Avg: {avgFitness:.2f}") # Info progress
            
            # Early stopping jika tidak ada perbaikan dalam waktu lama
            if generationsWithoutImprovement >= maxGenerationsWithoutImprovement: # Jika terlalu lama tanpa perbaikan
                print(f"   Early stopping: {generationsWithoutImprovement} generasi tanpa perbaikan") # Info early stopping
                break # Keluar dari loop evolusi
            
            # Buat populasi baru untuk generasi berikutnya
            newPopulation = [] # List untuk populasi generasi berikutnya
            
            # Elitism: simpan beberapa individu terbaik
            eliteCount = max(1, self.populationSize // 10) # Jumlah elite (10% populasi)
            sortedPopulation = sorted(population, key=lambda ind: ind.state_value, reverse=True) # Sort populasi
            newPopulation.extend(sortedPopulation[:eliteCount]) # Tambahkan elite ke populasi baru
            
            # Generate sisa populasi melalui crossover dan mutasi
            while len(newPopulation) < self.populationSize: # Sampai populasi penuh
                
                # Seleksi dua parent untuk crossover
                parent1 = self._selection(population) # Pilih parent pertama
                parent2 = self._selection(population) # Pilih parent kedua
                
                # Crossover jika memenuhi probabilitas
                if random.random() < self.crossoverRate: # Cek probabilitas crossover
                    child1, child2 = self._crossover(parent1, parent2, *objectives) # Lakukan crossover
                else: # Jika tidak crossover
                    child1, child2 = parent1.copy(), parent2.copy() # Copy parent langsung
                
                # Mutasi pada offspring
                if random.random() < self.mutationRate: # Cek probabilitas mutasi untuk child1
                    child1 = self._mutation(child1, *objectives) # Lakukan mutasi pada child1
                
                if random.random() < self.mutationRate: # Cek probabilitas mutasi untuk child2
                    child2 = self._mutation(child2, *objectives) # Lakukan mutasi pada child2
                
                # Tambahkan offspring ke populasi baru
                newPopulation.append(child1) # Tambahkan child1 ke populasi
                if len(newPopulation) < self.populationSize: # Jika masih ada slot
                    newPopulation.append(child2) # Tambahkan child2 ke populasi
            
            population = newPopulation[:self.populationSize] # Set populasi baru (potong jika lebih)
        
        endTime = time.time() # Catat waktu selesai eksekusi
        executionTime = endTime - startTime # Hitung total waktu eksekusi
        
        print(f"Genetic Algorithm selesai!") # Info algoritma selesai
        print(f"   Final Best Value: {bestIndividual.state_value:.2f}") # Tampilkan nilai terbaik akhir
        print(f"   Total Generations: {generation + 1}") # Tampilkan total generasi
        print(f"   Waktu Eksekusi: {executionTime:.3f} detik") # Tampilkan waktu eksekusi
        
        # Buat dictionary statistik untuk output
        stats = {
            'algorithm_name': 'Genetic Algorithm', # Nama algoritma
            'population_size': self.populationSize, # Ukuran populasi
            'max_generations': self.maxGenerations, # Maksimum generasi
            'crossover_rate': self.crossoverRate, # Rate crossover
            'mutation_rate': self.mutationRate, # Rate mutasi
            'selection_method': self.selectionMethod, # Metode seleksi
            'execution_time': executionTime, # Waktu eksekusi dalam detik
            'generations': generation + 1, # Jumlah generasi yang dijalankan
            'initial_state_value': initialBestValue, # Nilai terbaik awal
            'final_state_value': bestIndividual.state_value # Nilai terbaik akhir
        }
        
        return bestIndividual, stats # Return individu terbaik dan statistik lengkap
    
    def _initializePopulation(self, state: State, *objectives) -> List[State]:
        """Inisialisasi populasi awal dengan individu-individu random"""
        population = [] # List untuk menyimpan populasi
        
        for i in range(self.populationSize): # Generate sebanyak populationSize individu
            individual = state.copy() # Copy state template
            individual.initialize_random_state(*objectives) # Inisialisasi dengan assignment random
            population.append(individual) # Tambahkan ke populasi
        
        return population # Return populasi yang sudah diinisialisasi
    
    def _selection(self, population: List[State]) -> State:
        """Seleksi individu dari populasi berdasarkan metode yang dipilih"""
        if self.selectionMethod == "tournament": # Jika menggunakan tournament selection
            return self._tournamentSelection(population) # Lakukan tournament selection
        elif self.selectionMethod == "roulette": # Jika menggunakan roulette wheel selection
            return self._rouletteSelection(population) # Lakukan roulette selection
        else: # Jika metode tidak dikenali
            return random.choice(population) # Random selection sebagai fallback
    
    def _tournamentSelection(self, population: List[State]) -> State:
        """Tournament selection - pilih individu terbaik dari tournament"""
        tournament = random.sample(population, min(self.tournamentSize, len(population))) # Pilih individu untuk tournament
        return max(tournament, key=lambda ind: ind.state_value) # Return individu dengan fitness tertinggi
    
    def _rouletteSelection(self, population: List[State]) -> State:
        """Roulette wheel selection berdasarkan fitness proporsi"""
        # Hitung total fitness dan buat probabilitas
        minFitness = min(ind.state_value for ind in population) # Cari fitness minimum
        adjustedFitness = [ind.state_value - minFitness + 1 for ind in population] # Adjust fitness agar positif
        totalFitness = sum(adjustedFitness) # Total fitness untuk normalisasi
        
        # Generate random number dan pilih individu berdasarkan probabilitas
        randomValue = random.uniform(0, totalFitness) # Random value untuk roulette
        currentSum = 0 # Counter untuk cumulative probability
        
        for i, fitness in enumerate(adjustedFitness): # Iterasi setiap individu
            currentSum += fitness # Tambahkan fitness ke cumulative sum
            if currentSum >= randomValue: # Jika mencapai random value
                return population[i] # Return individu yang terpilih
        
        return population[-1] # Fallback: return individu terakhir
    
    def _crossover(self, parent1: State, parent2: State, *objectives) -> Tuple[State, State]:
        """Crossover dua parent untuk menghasilkan dua offspring"""
        # Implementasi crossover sederhana: tukar sebagian assignment
        child1 = parent1.copy() # Copy parent1 sebagai child1
        child2 = parent2.copy() # Copy parent2 sebagai child2
        
        # Ambil semua keys assignment dari kedua parent
        allKeys = list(set(list(parent1.assignments.keys()) + list(parent2.assignments.keys()))) # Gabung semua keys
        
        # Tentukan titik crossover
        if len(allKeys) > 1: # Jika ada assignment yang bisa di-crossover
            crossoverPoint = random.randint(1, len(allKeys) - 1) # Pilih titik crossover random
            
            # Tukar assignment setelah crossover point
            keysToSwap = allKeys[crossoverPoint:] # Keys yang akan ditukar
            
            for key in keysToSwap: # Untuk setiap key yang akan ditukar
                if key in parent1.assignments and key in parent2.assignments: # Jika ada di kedua parent
                    # Tukar assignment antara child1 dan child2
                    child1.assignments[key] = parent2.assignments[key] # Child1 ambil dari parent2
                    child2.assignments[key] = parent1.assignments[key] # Child2 ambil dari parent1
        
        # Update state value untuk kedua child
        child1.state_value = child1.count_state_value(*objectives) # Hitung fitness child1
        child2.state_value = child2.count_state_value(*objectives) # Hitung fitness child2
        
        return child1, child2 # Return kedua offspring
    
    def _mutation(self, individual: State, *objectives) -> State:
        """Mutasi individu dengan mengubah beberapa assignment secara random"""
        mutatedIndividual = individual.copy() # Copy individu untuk dimutasi
        
        # Tentukan berapa banyak assignment yang akan dimutasi
        mutationCount = max(1, int(len(mutatedIndividual.assignments) * 0.1)) # Mutasi 10% assignment
        
        # Pilih assignment yang akan dimutasi secara random
        assignmentKeys = list(mutatedIndividual.assignments.keys()) # Ambil semua keys
        keysToMutate = random.sample(assignmentKeys, min(mutationCount, len(assignmentKeys))) # Pilih keys untuk mutasi
        
        # Lakukan mutasi pada assignment yang terpilih
        for key in keysToMutate: # Untuk setiap key yang akan dimutasi
            # Generate assignment baru secara random untuk key tersebut
            roomCode, waktu = key # Ekstrak room dan waktu dari key
            availableCourses = list(mutatedIndividual.repo.mata_kuliah.values()) # Ambil semua mata kuliah
            
            if availableCourses: # Jika ada mata kuliah yang tersedia
                newCourse = random.choice(availableCourses) # Pilih mata kuliah random
                mutatedIndividual.assignments[key] = newCourse # Assign mata kuliah baru
        
        # Update state value setelah mutasi
        mutatedIndividual.state_value = mutatedIndividual.count_state_value(*objectives) # Hitung fitness baru
        
        return mutatedIndividual # Return individu yang sudah dimutasi