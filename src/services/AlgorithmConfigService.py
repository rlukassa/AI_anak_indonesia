from typing import Dict, Any
import time

class AlgorithmConfigService:
    # /// BUAT HC    
    ## NAH DISINI CONFIG PARAMERTER NYA
    # HC ATAU GA butuh parameter apa, ntar input usernya disini
    # yang dicomment itu contoh
    # nah implement dibawhanya
    @staticmethod
    def configureHillClimbing() -> Dict[str, Any]: # config parameter HC
        print("\n" + "="*50)
        print("KONFIGURASI HILL CLIMBING")
        print("="*50)
        
        print("Pilih variant Hill Climbing:")
        print("1. Steepest Ascent")
        print("2. Sideways Move")
        print("3. Stochastic")
        print("4. Random Restart")
        
        while True:
            variant_choice = input("Masukkan pilihan (1-4): ")
            if variant_choice in ["1", "2", "3", "4"]:
                break
        
        variant_map = {
            "1": "steepest",
            "2": "sideways",
            "3": "stochastic",
            "4": "random_restart"
        }
        
        variant = variant_map.get(variant_choice, "steepest")
        config = {
            'variant': variant,
            'max_sideways': None,
            'max_iteration': None,
            'max_restart': None
        }
        if variant == "sideways":
            max_sideways = int(input("Maksimum sideway: "))
            config['max_sideways'] = max_sideways
        
        if variant == "stochastic":
            max_iteration = int(input("Maksimum Iterasi: "))
            config['max_iteration'] = max_iteration

        if variant == "random_restart":
            max_restart = int(input("Maksimum restart: "))
            config['max_restart'] = max_restart
        
        print(f"\nParameter Hill Climbing:")
        print(f"   Variant: {variant}")
        if variant == "sideways":
            print(f"   Max Sideways: {max_sideways}")
        if variant == "stochastic":
            print(f"   Max Iteration: {max_iteration}")
        if variant == "random_restart":
            print(f"   Max Restarts: {max_restart}")
        
        return config
    
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
        """Konfigurasi parameter Genetic Algorithm"""
        print("\n" + "="*50)
        print("KONFIGURASI GENETIC ALGORITHM")
        print("="*50)
        
        while True:
            population_size =   int(input("Population Size (per iterasi): "))
            max_iteration =     int(input("Maximum Iteration            : "))
            if population_size % 2 != 0:
                print("Population size harus kelipatan 2.")
            else: break
        
        print(f"\nParameter Genetic Algorithm:")
        print(f"   Population Size: {population_size}")
        print(f"   Max Iteration  : {max_iteration}")
        
        return {
            'populationSize': population_size,
            'max_iteration': max_iteration
        }


# NAH ntar kan return parameternya 
# terus bakal bikin object dari parameter nya 
# dan panggil <algoritma>.search() dari yang diimplment dari file algortima masing masing
# cek di main.py
#terus 