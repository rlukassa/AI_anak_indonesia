from src.io.utils import Utils
from settings.settings import validPath, validJSONFormat
from src.services.OutputService import OutputService

class UserInterfaceService:

    @staticmethod
    def getValidFilePath() -> str:
        """Request JSON file path and validate it."""
        while True:
            filePath = input("Masukkan path file JSON: ").strip()
            if validPath(filePath) and validJSONFormat(filePath):
                return filePath
            print("Path tidak valid! Pastikan file JSON dan format benar.")

    @staticmethod
    def selectAlgorithm() -> str:
        """Select algorithm: HC / SA / GA."""
        valid_choices = {"HC", "SA", "GA"}
        while True:
            Utils.clear_screen()
            OutputService.showWelcome()
            print("\nPilih Algoritma:")
            print("   1. Hill Climbing (HC)")
            print("   2. Simulated Annealing (SA)")
            print("   3. Genetic Algorithm (GA)")

            selected = input("\nPilihan (HC/SA/GA): ").strip().upper()
            if selected in valid_choices:
                return selected

            print("Pilihan tidak valid! Gunakan HC, SA, atau GA.")
            Utils.delay(1100)
