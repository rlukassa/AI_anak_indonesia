import matplotlib.pyplot as plt
from typing import Dict, Any
from src.io.utils import Utils
from src.model.state import State
from ..io.Table import Table
from ..io.Info import Info

class OutputService:
    
    @staticmethod
    def generateAlgorithmInfo(algorithmName: str, parameters: Dict[str, Any], executionStats: Dict[str, Any]) -> Info:
        """Build Info object describing algorithm parameters and execution stats."""
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
        
        if 'initial_stateValue' in executionStats:
            info.addInfo("State Value Awal", f"{executionStats['initial_stateValue']:.2f}")
        
        if 'final_stateValue' in executionStats:
            info.addInfo("State Value Akhir", f"{executionStats['final_stateValue']:.2f}")
        
        if 'initial_stateValue' in executionStats and 'final_stateValue' in executionStats:
            improvement = executionStats['final_stateValue'] - executionStats['initial_stateValue']
            info.addInfo("Peningkatan", f"{improvement:+.2f}")

        if 'restarts' in executionStats and 'iter_restart' in executionStats:
            info.addInfo("Jumlah Restart", f"{executionStats['restarts']}")
            for i in range(executionStats['restarts']):
                info.addInfo(f"Iterasi Restart ke-{i}", f"{executionStats['iter_restart'][i]}")

        if 'stuck_freq' in executionStats:
            info.addInfo("Stuck Frequency", f"{executionStats['stuck_freq']}")

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
            f"Kualitas Jadwal: {'Baik' if state.stateValue > -10 else 'Perlu Perbaikan'}\n"
            f"Utilisasi Slot: {(totalAssignments / (totalRooms * 55)) * 100:.1f}%"
        )
        
        info.addSection("ANALISIS JADWAL", analysisContent)
        return info
    
    
    @staticmethod
    def generateScheduleTables(state: State) -> Dict[str, Table]:
        """Generate per-room schedule tables from the current state assignments."""
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
        """Render line plots from executionStats['plot_graph'] grouped by axes labels."""
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
                      executionStats: Dict[str, Any], initialState: State = None) -> None:
        
        # Generate dan display algorithm info
        algorithmInfo = OutputService.generateAlgorithmInfo(algorithmName, parameters, executionStats)
        algorithmInfo.display()
        
        # Generate dan display initial state schedule tables (jadwal state awal)
        if initialState:
            print(f"\nJADWAL INITIAL STATE")
            print("=" * 80)
            initialTables = OutputService.generateScheduleTables(initialState)
            
            if initialTables:
                for roomCode, table in initialTables.items():
                    print(f"\nJADWAL RUANGAN (INITIAL): {roomCode}")
                    table.display()
            else:
                print("Tidak ada jadwal awal yang dapat ditampilkan.")
                print("Initial state mungkin kosong atau tidak ada assignment.")
        
        # Generate dan display schedule analysis
        scheduleAnalysis = OutputService.generateScheduleAnalysis(state)
        scheduleAnalysis.display()
        
        # Generate dan display final state tables (jadwal hasil optimasi)
        print(f"\nJADWAL HASIL OPTIMASI")
        print("=" * 80)
        tables = OutputService.generateScheduleTables(state)
        
        if tables:
            for roomCode, table in tables.items():
                print(f"\nJADWAL RUANGAN (FINAL): {roomCode}")
                table.display()
        else:
            print("\nTidak ada jadwal yang dapat ditampilkan.")
            print("State mungkin kosong atau tidak ada assignment.")

        # Generate Graph
        OutputService.generateGraph(algorithmName, executionStats)
    
    
    @staticmethod
    def showWelcome() -> None:
        """Print a width-aware, ANSI-styled CLI banner."""
        Utils.showBox("SISTEM OPTIMASI PENJADWALAN KULIAH", "Local Search")

    
    @staticmethod
    def saveResults(state: State, algorithmName: str, parameters: Dict[str, Any], 
                   executionStats: Dict[str, Any], filename: str, initialState: State = None) -> None:
        """Save hasil optimasi ke file dan save plot jika ada"""
        import os
        from datetime import datetime
        
        # Buat folder results jika belum ada
        results_dir = "results"
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        
        # Save hasil teks ke file
        text_filename = os.path.join(results_dir, f"{filename}.txt")
        with open(text_filename, 'w', encoding='utf-8') as f:
            
            # Informasi algoritma
            info = OutputService.generateAlgorithmInfo(algorithmName, parameters, executionStats)
            f.write("INFORMASI ALGORITMA\n")
            f.write("-" * 40 + "\n")
            for key, value in info.infos.items():
                f.write(f"{key:20}: {value}\n")
            f.write("\n")
            
            # Informasi state value
            f.write("NILAI FUNGSI OBJEKTIF\n")
            f.write("-" * 40 + "\n")
            f.write(f"State Value Akhir   : {state.stateValue:.2f}\n")
            
            # Detail constraint violations jika ada
            if hasattr(state, 'constraint_violations'):
                f.write(f"Pelanggaran Ruang   : {state.constraint_violations.get('room_conflict', 0)}\n")
                f.write(f"Pelanggaran Waktu   : {state.constraint_violations.get('time_conflict', 0)}\n")
                f.write(f"Pelanggaran Dosen   : {state.constraint_violations.get('lecturer_conflict', 0)}\n")
            f.write("\n")
            
            # Initial state tables
            if initialState:
                f.write("JADWAL STATE AWAL\n")
                f.write("=" * 40 + "\n")
                initialTables = OutputService.generateScheduleTables(initialState)
                
                if initialTables:
                    for roomCode, table in initialTables.items():
                        f.write(f"\nJADWAL RUANGAN (INITIAL): {roomCode}\n")
                        f.write(OutputService._tableToString(table))
                else:
                    f.write("Tidak ada jadwal awal yang dapat ditampilkan.\n")
                f.write("\n")
            
            # Final state tables
            f.write("JADWAL HASIL OPTIMASI\n")
            f.write("=" * 40 + "\n")
            tables = OutputService.generateScheduleTables(state)
            
            if tables:
                for roomCode, table in tables.items():
                    f.write(f"\nJADWAL RUANGAN (FINAL): {roomCode}\n")
                    f.write(OutputService._tableToString(table))
            else:
                f.write("Tidak ada jadwal yang dapat ditampilkan.\n")
        
        # Save plot jika ada data plotting
        plot_saved = False
        if 'plot_graph' in executionStats:
            plot_data = executionStats['plot_graph']
            plot_filename = os.path.join(results_dir, f"{filename}_plots.png")
            
            try:
                # Create subplots untuk multiple graphs
                num_plots = len(plot_data)
                fig, axes = plt.subplots(num_plots, 1, figsize=(10, 6*num_plots))
                if num_plots == 1:
                    axes = [axes]
                
                for i, (title, data) in enumerate(plot_data.items()):
                    axes[i].plot(data['x_data'], data['y_data'], 'b-', linewidth=1.5, label=title)
                    axes[i].set_xlabel(data['x_label'])
                    axes[i].set_ylabel(data['y_label'])
                    axes[i].set_title(f"{algorithmName} - {title}")
                    axes[i].grid(True, alpha=0.3)
                    axes[i].legend()
                
                plt.tight_layout()
                plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
                plt.close()
                plot_saved = True
                
            except Exception as e:
                print(f"Warning: Gagal menyimpan plot - {e}")
        
        # Konfirmasi save
        print(f"\nHasil berhasil disimpan:")
        print(f"   File teks: {text_filename}")
        if plot_saved:
            print(f"   File plot: {plot_filename}")
        
        # Update pesan sukses di OutputConfigService
        from .OutputConfigService import OutputConfigService
        OutputConfigService.showSaveSuccess(filename)
    
    @staticmethod
    def _tableToString(table: Table) -> str:
        """Convert Table object ke string untuk save ke file"""
        try:
            return table.render()
        except Exception as e:
            return f"Error: Unable to convert table to string - {str(e)}"