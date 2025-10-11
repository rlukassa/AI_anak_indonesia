from typing import Dict, List, Any, Optional
from src.model.state import State
from ..io.Table import Table
from ..io.Info import Info

class OutputService:
    
    @staticmethod
    def generateAlgorithmInfo(algorithmName: str, parameters: Dict[str, Any], 
                            executionStats: Dict[str, Any]) -> Info:
        info = Info()
        info.addInfo("Algoritma", algorithmName)
        
        if algorithmName == "Simulated Annealing":
            info.addInfo("Initial Temperature", f"{parameters.get('initialTemp', 0):.2f}")
            info.addInfo("Cooling Rate", f"{parameters.get('coolingRate', 0):.4f}")
            info.addInfo("Stop Temperature", f"{parameters.get('stopTemp', 0):.4f}")
        
        elif "Hill Climbing" in algorithmName:
            info.addInfo("Variant", parameters.get('variant', 'steepest'))
            info.addInfo("Max Iterations", f"{parameters.get('maxIterations', 0):,}")
            if parameters.get('restarts', 1) > 1:
                info.addInfo("Restarts", f"{parameters.get('restarts', 1)}")
        
        elif algorithmName == "Genetic Algorithm":
            info.addInfo("Population Size", f"{parameters.get('populationSize', 0):,}")
            info.addInfo("Max Generations", f"{parameters.get('generations', 0):,}")
            info.addInfo("Crossover Rate", f"{parameters.get('crossoverRate', 0):.2f}")
            info.addInfo("Mutation Rate", f"{parameters.get('mutationRate', 0):.2f}")
        
        # Add execution statistics
        if 'execution_time' in executionStats:
            info.addInfo("Waktu Eksekusi", f"{executionStats['execution_time']:.3f} detik")
        
        if 'iterations' in executionStats:
            info.addInfo("Jumlah Iterasi", f"{executionStats['iterations']:,}")
        
        if 'initial_state_value' in executionStats:
            info.addInfo("State Value Awal", f"{executionStats['initial_state_value']:.2f}")
        
        if 'final_state_value' in executionStats:
            info.addInfo("State Value Akhir", f"{executionStats['final_state_value']:.2f}")
        
        if 'initial_state_value' in executionStats and 'final_state_value' in executionStats:
            improvement = executionStats['final_state_value'] - executionStats['initial_state_value']
            info.addInfo("Peningkatan", f"{improvement:+.2f}")
        
        return info
    
    @staticmethod
    def generateScheduleAnalysis(state: State) -> Info:
        """Generate analisis jadwal"""
        info = Info()
        
        # Hitung statistik
        totalCourses = len(state.repo.mata_kuliah)
        totalRooms = len(state.repo.ruangan) 
        totalAssignments = len(state.assignments)
        
        # Analisis konflik
        conflicts = 0
        for waktu, mataKuliahList in state.times_to_mk.items():
            if len(mataKuliahList) > 1:
                conflicts += len(mataKuliahList) - 1
        
        analysisContent = f"""Total Mata Kuliah: {totalCourses}
                            Total Ruangan: {totalRooms}
                            Total Assignment: {totalAssignments}
                            Konflik Terdeteksi: {conflicts}
                            Kualitas Jadwal: {'Baik' if state.state_value > -10 else 'Perlu Perbaikan'}
                            Utilisasi Slot: {(totalAssignments / (totalRooms * 55)) * 100:.1f}%"""
        
        info.addSection("ANALISIS JADWAL", analysisContent)
        
        return info
    
    @staticmethod
    def generateScheduleTables(state: State) -> Dict[str, Table]:
        """Generate tabel jadwal per ruangan"""
        tablesByRoom = {}
        
        # Group assignments by room
        roomSchedules = {}
        for (roomCode, waktu), matkul in state.assignments.items():
            if roomCode not in roomSchedules:
                roomSchedules[roomCode] = {}
            
            day = waktu.hari
            hour = waktu.jam
            
            if day not in roomSchedules[roomCode]:
                roomSchedules[roomCode][day] = {}
            
            roomSchedules[roomCode][day][hour] = matkul.kode
        
        # Create table for each room
        for roomCode, schedule in roomSchedules.items():
            table = Table()
            
            # Set headers
            headers = ["Jam", "Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
            table.setHeaders(headers)
            
            # Fill table with schedule data
            days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
            for hour in range(7, 18):
                row = [str(hour)]
                
                for day in days:
                    if day in schedule and hour in schedule[day]:
                        row.append(schedule[day][hour])
                    else:
                        row.append("")
                
                table.addRow(row)
            
            tablesByRoom[roomCode] = table
        
        return tablesByRoom
    
    @staticmethod
    def displayResults(state: State, algorithmName: str, parameters: Dict[str, Any], 
                      executionStats: Dict[str, Any]) -> None:
        """Display semua hasil optimasi"""
        
        # Generate dan display algorithm info
        algorithmInfo = OutputService.generateAlgorithmInfo(algorithmName, parameters, executionStats)
        algorithmInfo.display()
        
        # Generate dan display schedule analysis
        scheduleAnalysis = OutputService.generateScheduleAnalysis(state)
        scheduleAnalysis.display()
        
        # Generate dan display tables
        tables = OutputService.generateScheduleTables(state)
        
        if tables:
            for roomCode, table in tables.items():
                print(f"\nJADWAL RUANGAN: {roomCode}")
                print("=" * 80)
                table.display()
                print("*Kolom jam di output merupakan jam mulai")
        else:
            print("\nTidak ada jadwal yang dapat ditampilkan.")
            print("State mungkin kosong atau tidak ada assignment.")
    
    @staticmethod # (1.) Ini cuman nampilin pesan doang
    # langsung ke Settings.getValidFilePath (2.) --> tapi itu buat cek validPathnya aja si
    # langsung ketiga deng (3.) UserInterfaceServices.selectAlgorithm
    def showWelcome() -> None:
        """Tampilkan welcome message"""
        print("\n" + "="*80)
        print("SISTEM OPTIMASI PENJADWALAN KULIAH")
        print("="*80)
    
    @staticmethod
    def showOptimizationStart() -> None:
        """Tampilkan pesan mulai optimasi"""
        print("\nMemulai optimasi penjadwalan...")
    
    @staticmethod
    def showResultHeader() -> None:
        """Tampilkan header hasil optimasi"""
        print("\n" + "="*80)
        print("HASIL OPTIMASI PENJADWALAN KULIAH")
        print("="*80)