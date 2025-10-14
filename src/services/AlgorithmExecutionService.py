from typing import Dict, Any, Tuple
from src.model.state import State
from src.algorithms.simulated_annealing import SA
from src.algorithms.hill_climbing import HillClimbing  
from src.algorithms.genetic import GeneticAlgorithm
from src.eval.evaluator import kasus_mahasiswa_bentrok, kasus_kapasitas_kurang, kasus_dosen_gabisa, kasus_dosen_bentrok

class AlgorithmExecutionService:
    
    @staticmethod
    def runHillClimbing(initialState: State, config: Dict[str, Any]) -> Tuple[State, Dict[str, Any]]:
        # definisi objective functions untuk evaluasi
        objectiveFunctions = (
            kasus_mahasiswa_bentrok,  # fungsi untuk deteksi bentrok mahasiswa
            kasus_kapasitas_kurang,   # fungsi untuk deteksi kapasitas ruangan kurang
            kasus_dosen_gabisa,       # fungsi untuk deteksi dosen tidak bisa mengajar
            kasus_dosen_bentrok       # fungsi untuk deteksi bentrok dosen
        )
        
        # initialize random state sebelum algoritma dimulai
        initialState.initialize_random_state(*objectiveFunctions)  # generate initial assignment
        
        # buat instance algoritma hill climbing
        hillClimbingAlgorithm = HillClimbing(
            config['variant'],
            config['max_sideways'],
            config['max_iteration'],
            config['max_restart']
        )
        
        # jalankan algoritma dan return hasil
        # nah return nya disini 
        return hillClimbingAlgorithm.search(initialState, *objectiveFunctions)
    
    @staticmethod
    def runSimulatedAnnealing(initialState: State, config: Dict[str, Any]) -> Tuple[State, Dict[str, Any]]:
        """Menjalankan algoritma Simulated Annealing dengan konfigurasi yang diberikan"""
        # definisi objective functions untuk evaluasi
        objectiveFunctions = (
            kasus_mahasiswa_bentrok,  # fungsi untuk deteksi bentrok mahasiswa
            kasus_kapasitas_kurang,   # fungsi untuk deteksi kapasitas ruangan kurang
            kasus_dosen_gabisa,       # fungsi untuk deteksi dosen tidak bisa mengajar
            kasus_dosen_bentrok       # fungsi untuk deteksi bentrok dosen
        )
        
        # initialize random state sebelum algoritma dimulai
        initialState.initialize_random_state(*objectiveFunctions)  # generate initial assignment
        
        # buat instance algoritma simulated annealing
        simulatedAnnealingAlgorithm = SA(
            config['initialTemp'],    # suhu awal
            config['coolingRate'],    # laju pendinginan
            config['stopTemp']        # suhu berhenti
        )
        
        # jalankan algoritma dan return hasil
        return simulatedAnnealingAlgorithm.search(initialState, *objectiveFunctions)
    
    @staticmethod
    def runGeneticAlgorithm(initialState: State, config: Dict[str, Any]) -> Tuple[State, Dict[str, Any]]:
        """Menjalankan algoritma Genetic Algorithm dengan konfigurasi yang diberikan"""
        # definisi objective functions untuk evaluasi
        objectiveFunctions = (
            kasus_mahasiswa_bentrok,  # fungsi untuk deteksi bentrok mahasiswa
            kasus_kapasitas_kurang,   # fungsi untuk deteksi kapasitas ruangan kurang
            kasus_dosen_gabisa,       # fungsi untuk deteksi dosen tidak bisa mengajar
            kasus_dosen_bentrok       # fungsi untuk deteksi bentrok dosen
        )
        
        # initialize random state sebelum algoritma dimulai
        initialState.initialize_random_state(*objectiveFunctions)  # generate initial assignment
        
        # buat instance algoritma genetic algorithm
        geneticAlgorithm = GeneticAlgorithm(
            config['populationSize'], # ukuran populasi per iterasi
            config['max_iteration'],  # maksimum iterasi
        )
        
        # jalankan algoritma dan return hasil
        return geneticAlgorithm.search(initialState, *objectiveFunctions)