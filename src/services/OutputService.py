import matplotlib.pyplot as plt
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
            if parameters.get('max_sideways') is not None:
                info.addInfo("Max Sideways", parameters.get('max_sideways'))
            if parameters.get('max_iteration') is not None:
                info.addInfo("Max Iteration", parameters.get('max_iteration'))
            if parameters.get('max_restart') is not None:
                info.addInfo("Max Restart", parameters.get('max_restart'))
        
        elif algorithmName == "Genetic Algorithm":
            info.addInfo("Population Size", f"{parameters.get('populationSize', 0):,}")
            info.addInfo("Max Iteration", f"{parameters.get('max_iteration', 0):,}")
        
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

        if 'restarts' in executionStats and 'iter_restart' in executionStats:
            info.addInfo("Jumlah Restart", f"{executionStats['restarts']}")
            for i in range(executionStats['restarts']):
                info.addInfo(f"Iterasi Restart ke-{i}", f"{executionStats['iter_restart'][i]}")

        return info
    
    @staticmethod
    def generateScheduleAnalysis(state: State) -> Info:
        """Generate analisis jadwal"""
        info = Info()
        
        # Hitung statistik
        totalCourses = len(state.repo.mata_kuliah)
        totalRooms = len(state.repo.ruangan) 
        totalAssignments = len(state.assignments)
        
        analysisContent = (
            f"Total Mata Kuliah: {totalCourses}\n"
            f"Total Ruangan: {totalRooms}\n"
            f"Total Assignment: {totalAssignments}\n"
            f"Kualitas Jadwal: {'Baik' if state.state_value > -10 else 'Perlu Perbaikan'}\n"
            f"Utilisasi Slot: {(totalAssignments / (totalRooms * 55)) * 100:.1f}%"
        )
        
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
    def generateGraph(algorithmName: str, executionStats: Dict[str, Any]) -> None:
        """
        Menggenerasi dan menampilkan grafik dari data yang ada di executionStats.
        
        Data grafik diharapkan berada di bawah key 'plot_graph' dengan format:
        Dict[str, Dict[str, List[float]]]
        
        Contoh:
        {
            'state_value': {
                'x_label': 'Iterasi',
                'y_label': 'Nilai State',
                'x_data': [1.0, 2.0, 3.0, 4.0, 5.0],
                'y_data': [10.0, 8.0, 6.0, 7.0, 5.0]
            },
            'temperature_value': {
                'x_label': 'Iterasi',
                'y_label': 'Nilai Temperatur',
                'x_data': [1.0, 2.0, 3.0, 4.0, 5.0],
                'y_data': [100.0, 80.0, 60.0, 40.0, 20.0]
            }
        }
        """
        if 'plot_graph' not in executionStats:
            print("\nTidak ada data grafik yang tersedia.")
            return

        plot_data = executionStats['plot_graph']
        grouped_plots = {}

        # Mengelompokkan data berdasarkan x_label dan y_label
        for line_label, data_dict in plot_data.items():
            x_label = data_dict.get('x_label', 'X-Axis')
            y_label = data_dict.get('y_label', 'Y-Axis')
            plot_key = (x_label, y_label)

            if plot_key not in grouped_plots:
                grouped_plots[plot_key] = []
            
            grouped_plots[plot_key].append({
                'label': line_label,
                'x_data': data_dict.get('x_data', []),
                'y_data': data_dict.get('y_data', [])
            })

        # Menggenerasi dan menampilkan grafik untuk setiap grup
        for (x_label, y_label), lines in grouped_plots.items():
            plt.figure(figsize=(10, 6))
            
            for line in lines:
                plt.plot(line['x_data'], line['y_data'], label=line['label'])
            
            plt.title(f'{algorithmName} - {y_label} vs {x_label}')
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.legend()
            plt.grid(True)
            plt.show()

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

        # Generate Graph
        OutputService.generateGraph(algorithmName, executionStats)
    
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