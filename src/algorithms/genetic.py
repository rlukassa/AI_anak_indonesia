from typing import Dict, List, Callable, Set, Tuple, Any
from src.eval.evaluator import *
from src.model.entities import *
from src.model.state import State
from src.algorithms.local_search import LocalSearch
import random
import time

from src.services.OutputService import OutputService

class GeneticAlgorithm(LocalSearch):

    def __init__(self, jml_parent:int=4, jml_iterasi:int=500):
        self.state:State = State()
        self.jml_parent:int = jml_parent
        self.jml_iterasi:int = jml_iterasi
        
    
    def _initialize_availableTime_for_matkul(self):
        self.matkul_slot_domain = {
            kode_mk : {
                slot
                for slot in self.state.availableSlots
                if slot[0] in {
                    waktu
                    for dosen in self.state.repo.dosen_tiap_matkul[kode_mk]
                    for waktu in dosen.waktu_preferensi
                }
            }
            for kode_mk in list(self.state.repo.mata_kuliah.keys())
        }

    
    def _initialize_conf_crossover(self, conf_crossover=None):
        if conf_crossover == None:
            self.conf_crossover = {
                kode_matkul: [
                    True if i == self.state.repo.mata_kuliah[kode_matkul].jumlah_sks - 1 else False for i in range(
                        self.state.repo.mata_kuliah[kode_matkul].jumlah_sks
                    )
                ] for kode_matkul in self.state.repo.mata_kuliah.keys()
            }
            # self.conf_crossover = {
            #     kode_matkul: [
            #         True if i % 2 == 0 else False for i in range(
            #             self.state.repo.mata_kuliah[kode_matkul].jumlah_sks
            #         )
            #     ]
            #     for kode_matkul, _ in self.state.repo.mata_kuliah.items()
            # }
        else:
            self.conf_crossover = conf_crossover


    def search(self, state:State, *objectives:Callable, conf_crossover=None) -> Tuple[State, Dict[str, Any]]: 
        self.state = state
        
        if self.jml_parent % 2 != 0:
            raise ValueError("N harus kelipatan 2.")
        self._initialize_availableTime_for_matkul()
        self._initialize_conf_crossover(conf_crossover)

        start_time = time.time()

        # 1. Inisialisasi Parent
        # print("\n[*] Inisialisasi Parent")
        selected_parent:List[State] = self._initialize_parent(*objectives)
        max_stateValue = [max([s.stateValue for s in selected_parent])]
        avg_stateValue = [sum([s.stateValue for s in selected_parent])/self.jml_parent]
        iterasi = [0]
        
        min_stateValue = min([s.stateValue for s in selected_parent])
        best_state = [s for s in selected_parent if s.stateValue == max([s.stateValue for s in selected_parent])][0]
        found = False
        for i in range(self.jml_iterasi):
            # print(f"\n========== Iterasi {i} ==========")

            # 2. Menhghitung fitness function
            # try:
            #     print(f"[*] Fitness function\n    {fitness_function} -> ", end="")
            # except:
            #     print(f"[*] Fitness function\n    [] -> ", end="")
            adaptive_scaler = abs(min_stateValue) + 1
            fitness_function = []
            for _, s in enumerate(selected_parent):
                fitness_function.append(adaptive_scaler + s.stateValue)
            # print(f"{fitness_function}")
            # print(f"[*] Adaptive Scaler {i}: {adaptive_scaler}")
            # print(f"[*] Generation State Value {i}\n    {[s.stateValue for s in selected_parent]}")
            
            # 3. Selection
            # print(f"[*] Selection {i}")
            selected_parent = random.choices(selected_parent, weights=fitness_function, k=self.jml_parent)

            # 4. Crossover
            # print(f"[*] Crossover {i}")
            for j in range(0, self.jml_parent, 2):
                p1 = selected_parent[j]
                p2 = selected_parent[j+1]
                
                # print(f"    [+] Crossover {i}: ({j}, {j+1})")
                c1, c2 = self._crossover(p1, p2, *objectives)

                # Konsep Elitisme
                urutan_state = sorted([p1, p2, c1, c2], key=lambda x: x.stateValue, reverse=True)
                good_state1 = urutan_state[0]
                good_state2 = urutan_state[1]

                # 5. Mutation
                # print(f"    [+] Mutation {i}: ({j}, {j+1})")
                good_state1 = self._mutation(good_state1, *objectives)
                good_state2 = self._mutation(good_state2, *objectives)
                    
                # Cek Ketercapaian Solusi
                if good_state1.stateValue >= best_state.stateValue: best_state = good_state1
                if good_state2.stateValue >= best_state.stateValue: best_state = good_state2

                selected_parent[j]  = good_state1
                selected_parent[j+1]= good_state2

                if good_state1.stateValue == 0 or good_state2.stateValue == 0: 
                    found = True; break

            # 5. Evaluasi min_stateValue
            min_stateValue = min(min_stateValue, min([s.stateValue for s in selected_parent]))
                
            # Plot Hasil
            max_stateValue.append(max([s.stateValue for s in selected_parent]))
            avg_stateValue.append(sum([s.stateValue for s in selected_parent])/self.jml_parent)
            iterasi.append(iterasi[-1]+1)

            if found: break
        
        end_time = time.time()
        execution_time = end_time - start_time

        # Plotting Hasil
        plotting_hasil = {
            'Maximum State Values': {
                'x_label': 'Iterasi',
                'y_label': 'State Value',
                'x_data': iterasi,
                'y_data': max_stateValue
            },
            'Average State Values': {
                'x_label': 'Iterasi',
                'y_label': 'State Value',
                'x_data': iterasi,
                'y_data': avg_stateValue
            }
        }

        stats = {
            'algorithm_name': 'Genetic Algorithm',
            'iterations': iterasi[-1],
            'initial_stateValue': max_stateValue[0],
            'final_stateValue': best_state.stateValue,
            'execution_time': execution_time,
            'plot_graph': plotting_hasil
        }
        # print("========== Done ==========\n")
        return best_state, stats
    
    def _initialize_parent(self, *objectives) -> List[State]:
        """Inisialisasi Parent"""
        selected_parent:List[State] = []
        # print("\n[*] State Value Awal")
        for i in range(self.jml_parent):
            parent_state = self.state.copy()
            parent_state.initializeRandomSuccessor(*objectives)
            selected_parent.append(parent_state)
            # print(f"    parent {i}: {parent_state.stateValue}")
        return selected_parent

    def _crossover(self, stateA:State, stateB:State, *objectives:Callable) -> Tuple[State, State]:
        """Melakukan crossover"""
        
        state_A = stateA.copy()
        state_B = stateB.copy()

        # 1. Extract (matkul -> slots)
        matkul_slots_A = state_A.MKtoSlots
        matkul_slots_B = state_B.MKtoSlots

        # 2. Crossover
        random_crossable_selector = random.randint(0, 1)
        for kode_matkul, list_crossability in self.conf_crossover.items():
            for i, crossable in enumerate(list_crossability):
                if  ((random_crossable_selector==0 and crossable) or 
                     (random_crossable_selector==1 and not crossable)):
                    state_A.swapMK(
                        matkul_slots_A[kode_matkul][i],
                        matkul_slots_B[kode_matkul][i]
                    )
                    state_B.swapMK(
                        matkul_slots_A[kode_matkul][i],
                        matkul_slots_B[kode_matkul][i]
                    )

        # 3. Update stateValue
        state_A.stateValue = state_A.countStateValue(*objectives)
        state_B.stateValue = state_B.countStateValue(*objectives)

        return state_A, state_B
    

    def _mutation(self, state:State, *objectives:Callable) -> State:
        """Melakukan Mutation"""
        new_state = state.generateRandomSuccessor(*objectives)
        if new_state.stateValue >= state.stateValue:
            return new_state
        else:
            return state.copy()