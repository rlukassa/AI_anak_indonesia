import src.io.repo_loader as Repository  # import modul repository loader
from src.model.state import State  # import class state untuk jadwal
from src.services.OutputService import OutputService  # import unified output service
from src.services.UserInterfaceService import UserInterfaceService  # import UI service
from src.services.AlgorithmConfigService import AlgorithmConfigService  # import algorithm config service
from src.services.OutputConfigService import OutputConfigService  # import output config service
from src.services.AlgorithmExecutionService import AlgorithmExecutionService  # import algorithm executor
from src.eval.evaluator import (  # import objective functions
    kasus_mahasiswa_bentrok, 
    kasus_kapasitas_kurang, 
    kasus_dosen_gabisa, 
    kasus_dosen_bentrok
)

def main():  # fungsi utama program sebagai driver
    # tampilkan welcome message
    OutputService.showWelcome()  # panggil service untuk tampilkan welcome
    
    # dapatkan path file yang valid dari user
    filePath = UserInterfaceService.getValidFilePath()  # service untuk input path valid
    
    # buat repository dari file JSON yang valid
    repository = Repository.create_repo(filePath)  # buat repository dari data JSON
    
    # pilih algoritma yang akan digunakan
    selectedAlgorithm = UserInterfaceService.selectAlgorithm()  # service untuk pilih algoritma
    
    # inisialisasi state awal
    initialState = State()  # buat state kosong
    initialState.initialize_domain(repository)  # inisialisasi dengan data repository
    
    # generate initial random state
    objectiveFunctions = (kasus_mahasiswa_bentrok, kasus_kapasitas_kurang, kasus_dosen_gabisa, kasus_dosen_bentrok)
    initialState.initialize_random_state(*objectiveFunctions)  # buat assignment awal
    
    # tampilkan pesan mulai optimasi
    OutputService.showOptimizationStart()  # pesan mulai optimasi
    
    # eksekusi algoritma berdasarkan pilihan user
    if selectedAlgorithm == "HC":  # jika pilih Hill Climbing
        # konfigurasi parameter Hill Climbing
        config = AlgorithmConfigService.configureHillClimbing()  # service konfigurasi HC
        
        # jalankan algoritma Hill Climbing
        finalState, algorithmStats = AlgorithmExecutionService.runHillClimbing(initialState, config)  # eksekusi HC
        
        # nama algoritma untuk output
        algorithmName = f"Hill Climbing ({config['variant']})"  # nama dengan variant
        
    elif selectedAlgorithm == "SA":  # jika pilih Simulated Annealing
        # konfigurasi parameter Simulated Annealing
        config = AlgorithmConfigService.configureSimulatedAnnealing()  # service konfigurasi SA
        
        # jalankan algoritma Simulated Annealing
        finalState, algorithmStats = AlgorithmExecutionService.runSimulatedAnnealing(initialState, config)  # eksekusi SA
        
        # nama algoritma untuk output
        algorithmName = "Simulated Annealing"  # nama algoritma
        
    elif selectedAlgorithm == "GA":  # jika pilih Genetic Algorithm
        # konfigurasi parameter Genetic Algorithm
        config = AlgorithmConfigService.configureGeneticAlgorithm()  # service konfigurasi GA
        
        # jalankan algoritma Genetic Algorithm
        finalState, algorithmStats = AlgorithmExecutionService.runGeneticAlgorithm(initialState, config)  # eksekusi GA
        
        # nama algoritma untuk output
        algorithmName = "Genetic Algorithm"  # nama algoritma
    
    # tampilkan header hasil
    OutputService.showResultHeader()  # tampilkan header hasil
    
    # display semua hasil optimasi
    OutputService.displayResults(finalState, algorithmName, config, algorithmStats)  # display lengkap
    
    # tanyakan apakah ingin save ke file
    if OutputConfigService.askSaveOption():  # tanya save option
        filename = OutputConfigService.generateFilename(algorithmName)  # generate nama file
        print(f"Fitur save akan ditambahkan nanti dengan nama: {filename}")  # placeholder

