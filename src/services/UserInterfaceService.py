import os
from settings.settings import validPath, validJSONFormat

# buat menangani input handling dari user

class UserInterfaceService:    
    @staticmethod
    def getValidFilePath() -> str:
        while True:  # loop sampai input valid
            filePath = str(input("Masukkan path file JSON: "))  # input path dari user
            if validPath(filePath) and validJSONFormat(filePath):  # validasi path dan format
                return filePath  # return path yang valid
            else:
                print("Path tidak valid! Pastikan file JSON dan path benar.")  # pesan error
    
    @staticmethod
    def selectAlgorithm() -> str:
        while True:  # loop sampai pilihan valid
            print("\nPilih Algoritma:")  # header pilihan
            print("1. Hill Climbing (HC)")  # pilihan 1
            print("2. Simulated Annealing (SA)")  # pilihan 2  
            print("3. Genetic Algorithm (GA)")  # pilihan 3
            
            selectedAlgorithm = str(input("Pilihan (HC/SA/GA): ")).upper()  # input dan convert ke uppercase
            
            if selectedAlgorithm in ["HC", "SA", "GA"]:  # validasi pilihan
                return selectedAlgorithm  # return pilihan yang valid
            else:
                print("Pilihan tidak valid! Gunakan HC, SA, atau GA.")  # pesan error
            # nah return selectedAlgorithm ini bakal ke main.py 
            # disitu bakal dicek masing masing, kalo HC -> config HC 
            # lanjut ke (4.) AlgorithmConfigService.py 