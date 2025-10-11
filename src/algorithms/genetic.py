# Genetic Algorithm
from typing import Dict, List, Callable, Tuple
from src.io.repo_loader import Repository
from src.eval.evaluator import *
from src.model.entities import *
from src.model.state import State
import random

class GeneticAlgorithm:

    def __init__(self, state:State, conf_crossover:Dict[str, List[bool]]):
        self.state = state
        self.conf_crossover: Dict[str, List[bool]] = conf_crossover # Dict[kode_matkul, list_konfigurasi]
        # list_konfigurasi = list berisi 0 atau 1
        # 0 = tidak di-cross-kan; 1 = di-cross-kan
        # ukuran list sesuai jumlah sks
        # mutation = matkul dengan slot tabarakan di-assign ke slot kosong


    def __init__(self, state:State):
        self.state = state
        self.conf_crossover = {
            kode_matkul: [
                True if i == state.repo.mata_kuliah[kode_matkul].jumlah_sks - 1 else False for i in range(
                    state.repo.mata_kuliah[kode_matkul].jumlah_sks
                )
            ] for kode_matkul in state.repo.mata_kuliah.keys()
        }
        # self.conf_crossover = {
        #     kode_matkul: [True] * matkul.jumlah_sks  # Semua slot bisa di-cross
        #     for kode_matkul, matkul in self.state.repo.mata_kuliah.items()
        # }


    def search(self, jml_parent:int, jml_iterasi:int, *objectives:Callable) -> State:
        """Genetic Algorithm"""
        
        if jml_parent % 2 != 0:
            raise ValueError("N harus kelipatan 2.")

        # 1. Inisialisasi Parent
        selected_parent:List[State] = []
        for _ in range(jml_parent):
            parent_state = self.state.copy()
            parent_state.initialize_random_state(*objectives)
            selected_parent.append(parent_state)
        
        min_state_value = min([s.state_value for s in selected_parent])
        for i in range(jml_iterasi):

            # 2. Menhghitung fitness function
            adaptive_scaler = abs(min_state_value) + 1
            fitness_function = []
            for _, state in enumerate(selected_parent):
                fitness_function.append(adaptive_scaler + state.state_value)
            
            # 3. Selection
            selected_parent = random.choices(selected_parent, weights=fitness_function, k=jml_parent)

            # 4. Crossover and Mutation
            for i in range(0, jml_parent, 2):
                p1 = selected_parent[i]
                p2 = selected_parent[i+1]
                
                self.crossover_mutation(p1, p2)

                # Cek Ketercapaian Solusi
                if p1.state_value == 0: return p1
                if p2.state_value == 0: return p2

            # 5. Evaluasi min_state_value
            min_state_value = min(min_state_value, min([s.state_value for s in selected_parent]))

    def crossover_mutation(self, stateA:State, stateB:State, *objectives:Callable):
        """Melakukan crossover dan mutation. Mengapa disatukan? 
        karena mutationnya sangat bergantung dengan hasil crossover"""
        
        # 1. Extract (matkul -> slots)
        matkul_slots_A = stateA.mk_to_slots
        matkul_slots_B = stateB.mk_to_slots

        # 2. Get crossover-able matkul_slot
        crossable_A: Dict[str, List[Tuple[str, Waktu]]] = {}
        crossable_B: Dict[str, List[Tuple[str, Waktu]]] = {}
        for kode_matkul, list_crossability in self.conf_crossover.items():
            for i, crossable in enumerate(list_crossability):
                if crossable:
                    crossable_A.setdefault(kode_matkul, []).append(matkul_slots_A[kode_matkul][i])
                    crossable_B.setdefault(kode_matkul, []).append(matkul_slots_B[kode_matkul][i])

        # 3. Check Conflicted crossable
        mutable_A: List[str] = []
        mutable_B: List[str] = []
        for (kode_matkul_A, list_slot_A), (kode_matkul_B, list_slot_B) in zip(crossable_A.items(), crossable_B.items()):
            for slot_A, slot_B in zip(list_slot_A, list_slot_B):
                # Conflict on A
                if slot_B in stateA.assignments:
                    # Mana yang harus mengalah
                    mutable_matkul = GeneticAlgorithm.select_mutable_matkul(stateA, slot_B, kode_matkul_A)
                    mutable_A.append(mutable_matkul)
                    if mutable_matkul != kode_matkul_A:
                        stateA.remove_mk(slot_A[0], slot_A[1]) # awal
                        stateA.remove_mk(slot_B[0], slot_B[1]) # tujuan
                        stateA.assign_mk(kode_matkul_A, slot_B[0], slot_B[1])
                # No Conflict on A
                else:
                    stateA.swap_mk(slot_A, slot_B)

                # Conflict on B
                if slot_A in stateB.assignments:
                    # Mana yang harus mengalah
                    mutable_matkul = GeneticAlgorithm.select_mutable_matkul(stateB, slot_A, kode_matkul_B)
                    mutable_B.append(mutable_matkul)
                    if mutable_matkul != kode_matkul_B:
                        stateB.remove_mk(slot_B[0], slot_B[1]) # awal
                        stateB.remove_mk(slot_A[0], slot_A[1]) # tujuan
                        stateB.assign_mk(kode_matkul_B, slot_A[0], slot_A[1])
                # No Conflict on B
                else:
                    stateB.swap_mk(slot_A, slot_B)

        # 4. Mutation
        for kode_matkul_A in mutable_A:
            possible_slots = [slot for slot in stateA.available_slots if slot not in stateA.assignments]
            new_slot = random.choice(possible_slots)
            stateA.assign_mk(kode_matkul_A, new_slot[0], new_slot[1])
        for kode_matkul_B in mutable_B:
            possible_slots = [slot for slot in stateB.available_slots if slot not in stateB.assignments]
            new_slot = random.choice(possible_slots)
            stateB.assign_mk(kode_matkul_B, new_slot[0], new_slot[1])

        # 5. Update state_value
        stateA.state_value = stateA.count_state_value(*objectives)
        stateB.state_value = stateB.count_state_value(*objectives)
    

    def select_mutable_matkul(state:State, slot:Tuple[str, Waktu], new_matkul:str, *objectives:Callable) -> str:
        """Mencari matkul yang akan dimutasi karena konflik diantara matkul lama dan matkul yang hendak di-crossover"""
        old_matkul = state.assignments[slot].kode
        new_state = state.copy()
        new_state.remove_mk(slot[0], slot[1])
        new_state.assign_mk(new_matkul, slot[0], slot[1])
        new_state.state_value = new_state.count_state_value(*objectives)
        if state.state_value > new_state.state_value:
            return old_matkul
        else:
            return new_matkul
