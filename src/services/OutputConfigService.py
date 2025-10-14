from typing import Dict, Any
import time

class OutputConfigService:    
    @staticmethod
    def askSaveOption() -> bool: # mau nyimpen ga
        saveOption = input("\nSimpan hasil ke file? (y/n): ").lower()  # input save option
        return saveOption == 'y'  # return boolean
    
    @staticmethod
    def generateFilename(algorithmName: str) -> str:
        timestamp = int(time.time())  # buat timestamp unik
        cleanAlgName = algorithmName.lower().replace(" ", "_")  # bersihkan nama algoritma
        return f"hasil_{cleanAlgName}_{timestamp}"  # return nama file dengan timestamp
    
    @staticmethod
    def showSaveSuccess(filename: str):
        print(f"\n Proses penyimpanan selesai!")
        print(f"Semua file tersimpan di folder 'results/' dengan prefix: {filename}")