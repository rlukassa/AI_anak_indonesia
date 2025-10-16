from os import system, name
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
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')
    OutputService.showWelcome()  
    filePath = UserInterfaceService.getValidFilePath()
    repository = Repository.create_repo(filePath) # yang ubah ke object itu
    selectedAlgorithm = UserInterfaceService.selectAlgorithm()  # service untuk pilih algoritma
    initialState = State()  # buat state kosong
    initialState.initializeDomain(repository)  # inisialisasi dengan data repository
    objectiveFunctions = (kasus_mahasiswa_bentrok, kasus_kapasitas_kurang, kasus_dosen_gabisa, kasus_dosen_bentrok)
    initialState.initializeRandomSuccessor(*objectiveFunctions)  # buat assignment awal
    OutputService.showOptimizationStart()  # pesan mulai 

    # // Buat HC
    if selectedAlgorithm == "HC":  # pilih Hill Climbing
        config = AlgorithmConfigService.configureHillClimbing()  # service konfigurasi HC

        # driver algo       
        finalState, algorithmStats = AlgorithmExecutionService.runHillClimbing(initialState, config)  # eksekusi HC
        algorithmName = f"Hill Climbing"  # nama dengan variant kek HC Random Restart 
    
    # // BUAT SA
    elif selectedAlgorithm == "SA":  # jika pilih Simulated Annealing
        config = AlgorithmConfigService.configureSimulatedAnnealing()  # service konfigurasi SA
        finalState, algorithmStats = AlgorithmExecutionService.runSimulatedAnnealing(initialState, config)  # eksekusi SA
        algorithmName = "Simulated Annealing"  # nama algoritma
        
    # // BUAT GA
    elif selectedAlgorithm == "GA":  # jika pilih Genetic Algorithm
        config = AlgorithmConfigService.configureGeneticAlgorithm()  # service konfigurasi GA
        
        finalState, algorithmStats = AlgorithmExecutionService.runGeneticAlgorithm(initialState, config)  # eksekusi GA
        algorithmName = "Genetic Algorithm"  # nama algoritma

    # nah finalState dan algorithmStats itu hasil dari algoritma nya 
    # terus keluarain display Resultsnya (6.) 7.
    # tapi ini yang dibawah biarin aja
    # jadi fokuske 4. dan 5. 
    # dah itu
    # harusnya udah keluar tabelnya kalo bener 

    
    
    # HEADER OUTPUT    
    OutputService.showResultHeader()  # tampilkan header hasil yang HASIL OPTIMASI
    
    # display semua hasil optimasi
    OutputService.displayResults(finalState, algorithmName, config, algorithmStats, initialState)  # display lengkap dari informasi optimasi sampe tabel dan info
    
    if OutputConfigService.askSaveOption():  # tanya save option
        filename = OutputConfigService.generateFilename(algorithmName)  # generate nama file
        # Implementasi save yang sebenarnya
        OutputService.saveResults(finalState, algorithmName, config, algorithmStats, filename, initialState)


