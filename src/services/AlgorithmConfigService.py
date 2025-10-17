from typing import Dict, Any
from src.io.utils import Utils

class AlgorithmConfigService:

    @staticmethod
    def configureHillClimbing() -> Dict[str, Any]: 
        Utils.clear_screen()
        Utils.showBox("KONFIGURASI HILL CLIMBING")
        
        print("Pilih variant Hill Climbing:")
        print("1. Steepest Ascent")
        print("2. Sideways Move")
        print("3. Stochastic")
        print("4. Random Restart")
        
        while True:
            variant_choice = input("Masukkan pilihan (1-4): ")
            if variant_choice in ["1", "2", "3", "4"]:
                Utils.clear_screen()
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
        
        return config
    
    @staticmethod
    def configureSimulatedAnnealing() -> Dict[str, Any]:
        """Konfigurasi parameter Simulated Annealing"""
        Utils.clear_screen()
        Utils.showBox("KONFIGURASI SIMULATED ANNEALING")
        
        initial_temp = float(input("Initial Temperature (terakhir cek 1000.0): "))
        cooling_rate = float(input("Cooling Rate (terakhir cek 0.95): "))
        stop_temp = float(input("Stop Temperature (terakhir cek 0.1): "))
        
        print(f"\nParameter Simulated Annealing:")
        print(f"   Initial Temperature: {initial_temp}")
        print(f"   Cooling Rate: {cooling_rate}")
        print(f"   Stop Temperature: {stop_temp}")
        
        Utils.clear_screen()
        print("Searching for optimal solution...")
        
        return {
            'initialTemp': initial_temp,
            'coolingRate': cooling_rate,
            'stopTemp': stop_temp
        }
    
    @staticmethod
    def configureGeneticAlgorithm() -> Dict[str, Any]:
        Utils.clear_screen()
        """Konfigurasi parameter Genetic Algorithm"""
        Utils.showBox("KONFIGURASI GENETIC ALGORITHM")
        
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