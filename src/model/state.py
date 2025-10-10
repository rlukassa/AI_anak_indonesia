# class state
from typing import Dict, Tuple, Set, List, Optional, Callable
from src.io.repo_loader import Repository
from src.model.entities import *
import random

class State:
    
    # Static Domain
    _available_times: Set[Waktu] = {
        Waktu(hari, jam) for hari in ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"] for jam in range(7, 18)
    }
    

    def __init__(self):
        # Object Domain
        self.repo              : Repository                # Must be initialize
        self.available_slots   : Set[Tuple[str, Waktu]]    # Must be initialize
        
        # Attribute
        self.assignments: Dict[Tuple[str, Waktu], MataKuliah] = {}
        self.times_to_mk: Dict[Waktu, List[MataKuliah]] = {}

        # State Value
        self.state_value: float = 0


    def initialize_domain(self, repo: Repository):
        """Inisialisasi Object Domain, termasuk repo"""
        self.repo = repo
        self.available_slots = [
            (kode_ruangan, waktu)
            for kode_ruangan in list(self.repo.ruangan.keys())
            for waktu in State._available_times
        ]


    def copy(self) -> "State":
        """Mengcopy State. Salinan hanya mencapai tingkat pemetaan, adapun tuple dan repo
        masih merujuk ke objek yang sama."""
        new_state = State()
        new_state.repo = self.repo
        new_state.available_slots = self.available_slots
        new_state.assignments = dict(self.assignments)
        new_state.times_to_mk = {k: list(v) for k, v in self.times_to_mk.items()}
        new_state.state_value = self.state_value
        return new_state


    def assign_mk(self, kode_mk: str, kode_ruangan: str, waktu: Waktu):
        """Menempatkan MataKuliah ke slot"""
        slot = (kode_ruangan, waktu)
        
        if slot in self.assignments:
            raise ValueError(f"Slot {slot} sudah terisi oleh mata kuliah lain.")
        matkul = self.repo.mata_kuliah[kode_mk]
        self.assignments[slot] = matkul

        if waktu not in self.times_to_mk:
            self.times_to_mk[waktu] = list()
        self.times_to_mk[waktu].append(matkul)
        
    
    def remove_mk(self, kode_ruangan: str, waktu: Waktu) -> Optional[MataKuliah]:
        """Menghapus mata kuliah dari slot"""
        slot = (kode_ruangan, waktu)
        if slot not in self.assignments:
            return None

        matkul = self.assignments[slot]
        del self.assignments[slot]

        self.times_to_mk[waktu].remove(matkul)
        if not self.times_to_mk[waktu]:
            del self.times_to_mk[waktu]

        return matkul
    

    def swap_mk(self, slot1: Tuple[str, Waktu], slot2: Tuple[str, Waktu]):
        """Menukar dua buah Matkul pada dua buah slot berbeda.
        Apabila ditukar dengan slot yang kosong, akan berperilaku seperti pemindahan matkul."""
        kode_ruangan1, waktu1 = slot1
        kode_ruangan2, waktu2 = slot2

        mk1 = self.remove_mk(kode_ruangan1, waktu1)
        mk2 = self.remove_mk(kode_ruangan2, waktu2)

        if mk1 is not None and mk2 is not None and mk1.kode == mk2.kode:
            return

        if mk1 is not None:
            self.assign_mk(mk1.kode, kode_ruangan2, waktu2)
        if mk2 is not None:
            self.assign_mk(mk2.kode, kode_ruangan1, waktu1)


    def count_state_value(self, *objectives: Callable) -> float:
        """Menghitung state value berdasarkan input fungsi-fungsi objektif.
        Semakin besar state value (mendekati 0) semakin baik."""
        state_value = 0
        for func in objectives:
            state_value -= func(self)
        return state_value


    def generate_all_successors(self, *objectives) -> list["State"]:
        successors = []
        for slot1 in list(self.assignments.keys()):
            for slot2 in self.available_slots:
                if slot1 == slot2:
                    continue
                if slot2 in self.assignments and self.assignments[slot2] == self.assignments[slot1]:
                    continue
                s = self.copy()
                s.swap_mk(slot1, slot2)
                s.state_value = s.count_state_value(*objectives)
                successors.append(s)
        return successors

    def generate_random_successor(self, *objectives) -> "State":
        successor = self.copy()
        if not successor.assignments:
            return successor

        slot1 = random.choice(list(successor.assignments.keys()))
        mk1 = successor.assignments[slot1]

        valid_slots = [
            slot for slot in successor.available_slots
            if slot != slot1 and (
                slot not in successor.assignments or successor.assignments[slot] != mk1
            )
        ]
        if not valid_slots:
            return successor

        slot2 = random.choice(valid_slots)
        successor.swap_mk(slot1, slot2)
        successor.state_value = successor.count_state_value(*objectives)
        return successor

    def initialize_random_state(self, *objectives: Callable):
        """Inisialisasi sebuah state secara random"""
        # Hapus segala yang ada
        self.assignments = {}
        self.times_to_mk = {}

        # Buat salinan slot yang tersedia agar bisa diacak dan di-pop
        available_slots = list(self.available_slots)
        random.shuffle(available_slots)

        # Untuk setiap mata kuliah, assign ke slot random sebanyak sks-nya
        for kode_mk in self.repo.mata_kuliah.keys():
            mk = self.repo.mata_kuliah[kode_mk]
            for _ in range(mk.jumlah_sks):
                if not available_slots:
                    raise ValueError("Tidak cukup slot untuk meng-assign semua mata kuliah.")
                slot = available_slots.pop()
                kode_ruangan, waktu = slot
                self.assign_mk(kode_mk, kode_ruangan, waktu)
        
        # Hitung state_value
        self.state_value = self.count_state_value(*objectives)