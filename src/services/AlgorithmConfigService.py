from typing import Dict, Any
import time

class AlgorithmConfigService:
    """Service khusus untuk konfigurasi parameter algoritma (Single Responsibility)"""
    # /// BUAT HC    
    ## NAH DISINI CONFIG PARAMERTER NYA
    # HC ATAU GA butuh parameter apa, ntar input usernya disini
    # yang dicomment itu contoh
    # nah implement dibawhanya
    @staticmethod
    def configureHillClimbing() -> Dict[str, Any]: # config parameter HC
        pass
        # TODO :
        # print("\n" + "="*50)
        # print("KONFIGURASI HILL CLIMBING")
        # print("="*50)
        
        # print("Pilih variant Hill Climbing:")
        # print("1. Steepest Ascent")
        # print("2. Sideways Move")
        # print("3. Stochastic")
        # print("4. Random Restart")
        
        # variant_choice = input("Masukkan pilihan (1-4): ")
        
        # variant_map = {
        #     "1": "steepest",
        #     "2": "sideways",
        #     "3": "stochastic",
        #     "4": "random_restart"
        # }
        
        # variant = variant_map.get(variant_choice, "steepest")
        # max_iterations = int(input("Maksimum iterasi (rekomendasi 1000): "))
        # restarts = 1
        
        # if variant == "random_restart":
        #     restarts = int(input("Jumlah restart (rekomendasi 10): "))
        
        # print(f"\nParameter Hill Climbing:")
        # print(f"   Variant: {variant}")
        # print(f"   Max Iterations: {max_iterations}")
        # if variant == "random_restart":
        #     print(f"   Restarts: {restarts}")
        
        # return {
        #     'variant': variant,
        #     'maxIterations': max_iterations,
        #     'restarts': restarts
        # }
    
    @staticmethod
    # Simulated Annealing, inimah udah w
    def configureSimulatedAnnealing() -> Dict[str, Any]:
        """Konfigurasi parameter Simulated Annealing"""
        print("\n" + "="*50)
        print("KONFIGURASI SIMULATED ANNEALING")
        print("="*50)
        
        initial_temp = float(input("Initial Temperature (terakhir cek 1000.0): "))
        cooling_rate = float(input("Cooling Rate (terakhir cek 0.95): "))
        stop_temp = float(input("Stop Temperature (terakhir cek 0.1): "))
        
        print(f"\nParameter Simulated Annealing:")
        print(f"   Initial Temperature: {initial_temp}")
        print(f"   Cooling Rate: {cooling_rate}")
        print(f"   Stop Temperature: {stop_temp}")
        
        return {
            'initialTemp': initial_temp,
            'coolingRate': cooling_rate,
            'stopTemp': stop_temp
        }
    
    @staticmethod
    # buat GA
    # sama kayak HC, config parameternya disini 
    def configureGeneticAlgorithm() -> Dict[str, Any]:
        pass 
        # TODO :
        # """Konfigurasi parameter Genetic Algorithm"""
        # print("\n" + "="*50)
        # print("KONFIGURASI GENETIC ALGORITHM")
        # print("="*50)
        
        # population_size = int(input("Population Size (rekomendasi 50): "))
        # generations = int(input("Max Generations (rekomendasi 100): "))
        # mutation_rate = float(input("Mutation Rate (rekomendasi 0.1): "))
        # crossover_rate = float(input("Crossover Rate (rekomendasi 0.8): "))
        
        # print(f"\nParameter Genetic Algorithm:")
        # print(f"   Population Size: {population_size}")
        # print(f"   Max Generations: {generations}")
        # print(f"   Mutation Rate: {mutation_rate}")
        # print(f"   Crossover Rate: {crossover_rate}")
        
        # return {
        #     'populationSize': population_size,
        #     'generations': generations,
        #     'mutationRate': mutation_rate,
        #     'crossoverRate': crossover_rate
        # }


# NAH ntar kan return parameternya 
# terus bakal bikin object dari parameter nya 
# dan panggil <algoritma>.search() dari yang diimplment dari file algortima masing masing
# cek di main.py
#terus 