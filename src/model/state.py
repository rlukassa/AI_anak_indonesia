from typing import Dict, Tuple, Set, List, Optional, Callable
from src.io.repo_loader import Repository
from src.model.entities import *
import random
import bisect

class State:
    
    # Static Domain
    _availableTimes: Set[Waktu] = {
        Waktu(hari, jam) for hari in ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"] for jam in range(7, 18)
    }
    

    def __init__(self):
        # Object Domain
        self.repo              : Repository                # Must be initialize
        self.availableSlots   : Set[Tuple[str, Waktu]]    # Must be initialize
        
        # Attribute
        self.assignments: Dict[Tuple[str, Waktu], MataKuliah] = {}
        self.timesToMK: Dict[Waktu, List[MataKuliah]] = {}

        # Attribute for Genetic Algorithm
        self.MKtoSlots: Dict[str, List[Tuple[str, Waktu]]] = {}

        # State Value
        self.stateValue: float = 0


    def initializeDomain(self, repo: Repository, _withDosen:bool=True):
        self.repo = repo
        availableTime:Set[Waktu] = {}
        if _withDosen:
            availableTime = {
                waktu
                for _, dosen in self.repo.dosen.items()
                for waktu in dosen.waktu_preferensi
            }
        else:
            availableTime = State._availableTimes
        self.availableSlots = {
            (kode_ruangan, waktu)
            for kode_ruangan in list(self.repo.ruangan.keys())
            for waktu in availableTime
        }
        minSlot = sum(
            matkul.jumlah_sks
            for matkul in self.repo.mata_kuliah.values()
        )
        if len(self.availableSlots) <= minSlot:
            raise ValueError("DOMAIN ERROR! slot dosen tidak cukup")


    # Ubah method copy() seperti di bawah ini:
    def copy(self) -> "State": # Mengembalikan salinan mendalam dari state 
        new_state = State()
        new_state.repo = self.repo
        new_state.availableSlots = self.availableSlots
        new_state.assignments = dict(self.assignments)
        new_state.timesToMK = {k: list(v) for k, v in self.timesToMK.items()}
        new_state.MKtoSlots = {k: list(v) for k, v in self.MKtoSlots.items()}
        new_state.stateValue = self.stateValue
        return new_state


    def assignMK(self, kode_mk: str, kode_ruangan: str, waktu: Waktu):
        slot = (kode_ruangan, waktu)
        
        if slot in self.assignments:
            raise ValueError(f"Slot {slot} sudah terisi oleh mata kuliah lain.")
        matkul = self.repo.mata_kuliah[kode_mk]
        self.assignments[slot] = matkul

        if waktu not in self.timesToMK:
            self.timesToMK[waktu] = list()
        self.timesToMK[waktu].append(matkul)

        if matkul.kode not in self.MKtoSlots:
            self.MKtoSlots[matkul.kode] = list()
        State.autoSortedAppend(self.MKtoSlots[matkul.kode], slot, list(self.repo.ruangan.keys()))
        # self.MKtoSlots[matkul.kode].append(slot)
        
    
    def removeMK(self, kode_ruangan: str, waktu: Waktu) -> Optional[MataKuliah]:
        # hapus matkul
        slot = (kode_ruangan, waktu)
        if slot not in self.assignments:
            return None

        matkul = self.assignments[slot]
        del self.assignments[slot]

        self.timesToMK[waktu].remove(matkul)
        if not self.timesToMK[waktu]:
            del self.timesToMK[waktu]

        self.MKtoSlots[matkul.kode].remove(slot)
        if not self.MKtoSlots[matkul.kode]:
            del self.MKtoSlots[matkul.kode]

        return matkul
    

    def swapMK(self, slot1: Tuple[str, Waktu], slot2: Tuple[str, Waktu]):
        # tuker 2 matkul dari 2 slot
        # kalo salah satu slot kosong, anggap aja assign ke slot itu 
        kode_ruangan1, waktu1 = slot1
        kode_ruangan2, waktu2 = slot2

        mk1 = self.removeMK(kode_ruangan1, waktu1)
        mk2 = self.removeMK(kode_ruangan2, waktu2)

        if mk1 is not None:
            self.assignMK(mk1.kode, kode_ruangan2, waktu2)
        if mk2 is not None:
            self.assignMK(mk2.kode, kode_ruangan1, waktu1)


    def countStateValue(self, *objectives: Callable) -> float:
        # hitung state value, ini nilainya ---- ... 0
        stateValue = 0
        for func in objectives:
            stateValue -= func(self)
        return stateValue


    def generateAllSuccessors(self, *objectives) -> list["State"]:
        successors = []
        for slot1 in list(self.assignments.keys()):
            for slot2 in self.availableSlots:
                if slot1 == slot2:
                    continue
                if slot2 in self.assignments and self.assignments[slot2] == self.assignments[slot1]:
                    continue
                s = self.copy()
                s.swapMK(slot1, slot2)
                s.stateValue = s.countStateValue(*objectives)
                successors.append(s)
        return successors

    def generateRandomSuccessor(self, *objectives) -> "State":
        successor = self.copy()
        if not successor.assignments:
            return successor

        slot1 = random.choice(list(successor.assignments.keys()))
        mk1 = successor.assignments[slot1]

        valid_slots = [
            slot for slot in successor.availableSlots
            if slot != slot1 and (
                slot not in successor.assignments or successor.assignments[slot] != mk1
            )
        ]
        if not valid_slots:
            return successor

        slot2 = random.choice(valid_slots)
        successor.swapMK(slot1, slot2)
        successor.stateValue = successor.countStateValue(*objectives)
        return successor

    def initializeRandomSuccessor(self, *objectives: Callable):
        # Hapus segala yang ada
        self.assignments = {}
        self.timesToMK = {}

        # Buat salinan slot yang tersedia agar bisa diacak dan di-pop
        availableSlots = list(self.availableSlots)
        random.shuffle(availableSlots)

        # Untuk setiap mata kuliah, assign ke slot random sebanyak sks-nya
        for kode_mk in self.repo.mata_kuliah.keys():
            mk = self.repo.mata_kuliah[kode_mk]
            for _ in range(mk.jumlah_sks):
                if not availableSlots:
                    raise ValueError("Tidak cukup slot untuk meng-assign semua mata kuliah.")
                slot = availableSlots.pop()
                kode_ruangan, waktu = slot
                self.assignMK(kode_mk, kode_ruangan, waktu)
        
        # Hitung stateValue
        self.stateValue = self.countStateValue(*objectives)

    
    def autoSortedAppend( # buat append ke list yang udah terurut
        myList: List[Tuple[str, Waktu]], 
        newItem: Tuple[str, Waktu],
        firstOrder: List[str],
        hariOrder: List[str] = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
    ) -> None:
        first_str, waktu = newItem
        
        if first_str not in firstOrder:
            raise ValueError(f"first_str harus {firstOrder}")
        if waktu.hari not in hariOrder:
            raise ValueError(f"hari harus {hariOrder}")
        
        # Key untuk sorting descending berdasarkan indeks
        def sort_key(item:Tuple[str, Waktu]):
            first_str, waktu = item
            # Untuk descending, gunakan negative dari indeks
            first_idx = -firstOrder.index(first_str)
            hari_idx = -hariOrder.index(waktu.hari)
            return (first_idx, hari_idx, -waktu.jam)
        
        # Insert di posisi yang tepat
        bisect.insort(myList, newItem, key=sort_key)