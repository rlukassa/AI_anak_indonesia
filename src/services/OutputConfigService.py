from typing import Dict, Any
import time

class OutputConfigService:
    """Service untuk konfigurasi output - Single Responsibility: Output Configuration"""
    
    @staticmethod
    def askSaveOption() -> bool: # mau nyimpen ga
        saveOption = input("\nSimpan hasil ke file? (y/n): ").lower()  # input save option
        return saveOption == 'y'  # return boolean
    
    @staticmethod
    def generateFilename(algorithmName: str) -> str:
        """Generate nama file dengan timestamp"""
        timestamp = int(time.time())  # buat timestamp unik
        cleanAlgName = algorithmName.lower().replace(" ", "_")  # bersihkan nama algoritma
        return f"hasil_{cleanAlgName}_{timestamp}"  # return nama file dengan timestamp
    
    @staticmethod
    def showSaveSuccess(filename: str):
        """Tampilkan pesan sukses save file"""
        print(f"\nHasil berhasil disimpan dengan nama: {filename}_*.txt")