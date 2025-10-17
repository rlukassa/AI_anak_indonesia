from typing import Dict, Any, Tuple
from src.model.state import State
from src.algorithms.simulated_annealing import SA
from src.io.utils import Utils
from src.algorithms.hill_climbing import HillClimbing  
from src.algorithms.genetic import GeneticAlgorithm
from src.eval.evaluator import kasus_mahasiswa_bentrok, kasus_kapasitas_kurang, kasus_dosen_gabisa, kasus_dosen_bentrok
from src.services.OutputService import OutputService

class AlgorithmExecutionService:
    
    @staticmethod
    def runHillClimbing(initialState: State, config: Dict[str, Any]) -> Tuple[State, Dict[str, Any]]:
        """Menjalankan algoritma Hill Climbing dengan konfigurasi yang diberikan"""
        
        Utils.clear_screen()
        OutputService.showWelcome()
        print("Searching for optimal solution...")
        
        # Set objective function
        objectiveFunctions = (
            kasus_mahasiswa_bentrok,
            kasus_kapasitas_kurang,
            kasus_dosen_gabisa,
            kasus_dosen_bentrok
        )
        
        # initialize random state
        initialState.initializeRandomSuccessor(*objectiveFunctions)
        
        # buat instance algoritma hill climbing
        hillClimbingAlgorithm = HillClimbing(
            config['variant'],
            config['max_sideways'],
            config['max_iteration'],
            config['max_restart']
        )
        
        # jalankan algoritma dan return hasil
        return hillClimbingAlgorithm.search(initialState, *objectiveFunctions)
    
    @staticmethod
    def runSimulatedAnnealing(initialState: State, config: Dict[str, Any]) -> Tuple[State, Dict[str, Any]]:
        """Menjalankan algoritma Simulated Annealing dengan konfigurasi yang diberikan"""
        
        Utils.clear_screen()
        OutputService.showWelcome()
        print("Searching for optimal solution...")
        
        # Set objective function
        objectiveFunctions = (
            kasus_mahasiswa_bentrok,
            kasus_kapasitas_kurang,
            kasus_dosen_gabisa,
            kasus_dosen_bentrok
        )
        
        # initialize random state
        initialState.initializeRandomSuccessor(*objectiveFunctions)
        
        # buat instance algoritma simulated annealing
        simulatedAnnealingAlgorithm = SA(
            config['initialTemp'],
            config['coolingRate'], 
            config['stopTemp']
        )
        
		# jalankan algoritma dan return hasil
        return simulatedAnnealingAlgorithm.search(initialState, *objectiveFunctions)
    
    @staticmethod
    def runGeneticAlgorithm(initialState: State, config: Dict[str, Any]) -> Tuple[State, Dict[str, Any]]:
        """Menjalankan algoritma Genetic Algorithm dengan konfigurasi yang diberikan"""
        
        Utils.clear_screen()
        OutputService.showWelcome()
        print("Searching for optimal solution...")
        
        # Set objective function
        objectiveFunctions = (
            kasus_mahasiswa_bentrok,
            kasus_kapasitas_kurang,
            kasus_dosen_gabisa,
            kasus_dosen_bentrok
        )
        
        # initialize random state
        initialState.initializeRandomSuccessor(*objectiveFunctions)
        
        # buat instance algoritma genetic algorithm
        geneticAlgorithm = GeneticAlgorithm(
            config['populationSize'],
            config['max_iteration'],
        )
        
        # jalankan algoritma dan return hasil
        return geneticAlgorithm.search(initialState, *objectiveFunctions)