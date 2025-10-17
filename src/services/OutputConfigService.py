import time

class OutputConfigService:
	@staticmethod
	def askSaveOption() -> bool:
		"""Prompt user whether to save results and return True/False."""
		saveOption = input("\nSimpan hasil ke file? (y/n): ").lower()
		return saveOption == 'y'
	
	@staticmethod
	def generateFilename(algorithmName: str) -> str:
		"""Generate unique filename prefix using algorithm name and timestamp."""
		timestamp = int(time.time())
		cleanAlgName = algorithmName.lower().replace(" ", "_")
		return f"hasil_{cleanAlgName}_{timestamp}"
	
	@staticmethod
	def showSaveSuccess(filename: str) -> None:
		"""Display confirmation message after saving results."""
		print(f"\n Proses penyimpanan selesai!")
		print(f"Semua file tersimpan di folder 'results/' dengan prefix: {filename}")
