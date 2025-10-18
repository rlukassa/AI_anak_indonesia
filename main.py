import src.io.repo_loader as Repository
from src.model.state import State
from src.io.utils import Utils
from src.services.OutputService import OutputService
from src.services.UserInterfaceService import UserInterfaceService
from src.services.AlgorithmConfigService import AlgorithmConfigService
from src.services.OutputConfigService import OutputConfigService
from src.services.AlgorithmExecutionService import AlgorithmExecutionService
from src.eval.evaluator import (
    kasus_mahasiswa_bentrok,
    kasus_kapasitas_kurang,
    kasus_dosen_gabisa,
    kasus_dosen_bentrok
)

def main():
    while True:
        Utils.clear_screen()
        OutputService.showWelcome()  
        filePath = UserInterfaceService.getValidFilePath()
        repository = Repository.create_repo(filePath)
        selectedAlgorithm = UserInterfaceService.selectAlgorithm()
        initialState = State()
        initialState.initializeDomain(repository)
        objectiveFunctions = (kasus_mahasiswa_bentrok, kasus_kapasitas_kurang, kasus_dosen_gabisa, kasus_dosen_bentrok)
        initialState.initializeRandomSuccessor(*objectiveFunctions)
        
        # Hill Climbing
        if selectedAlgorithm == "HC":
            config = AlgorithmConfigService.configureHillClimbing()
            finalState, algorithmStats = AlgorithmExecutionService.runHillClimbing(initialState, config)
            algorithmName = f"Hill Climbing"
            
        # Simmulated Annealing
        elif selectedAlgorithm == "SA":
            config = AlgorithmConfigService.configureSimulatedAnnealing()
            finalState, algorithmStats = AlgorithmExecutionService.runSimulatedAnnealing(initialState, config)
            algorithmName = "Simulated Annealing"
            
        # Genetic Algorithm
        elif selectedAlgorithm == "GA":
            config = AlgorithmConfigService.configureGeneticAlgorithm()
            finalState, algorithmStats = AlgorithmExecutionService.runGeneticAlgorithm(initialState, config)
            algorithmName = "Genetic Algorithm"
        
        Utils.clear_screen()
        OutputService.showWelcome()  
        
        # Display optimized results
        OutputService.displayResults(finalState, algorithmName, config, algorithmStats, initialState)
        
        # Save file option
        if OutputConfigService.askSaveOption():
            Utils.clear_screen()
            OutputService.showWelcome()  
            filename = OutputConfigService.generateFilename(algorithmName)
            OutputService.saveResults(finalState, algorithmName, config, algorithmStats, filename, initialState)
        
        # Again?
        if not Utils.askYesNo("Again? (Y/N) : "): 
            break


