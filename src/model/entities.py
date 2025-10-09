from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Ruangan:
    kode_ruangan: str
    kuota_ruangan: int


@dataclass(frozen=True)
class Waktu:
    hari: str
    jam: int


@dataclass
class MataKuliah:
    kode: str
    jumlah_mahasiswa: int
    jumlah_sks: int

    def __hash__(self):
        return hash(self.kode)

    def __eq__(self, other):
        if not isinstance(other, MataKuliah):
            return False
        return self.kode == other.kode


@dataclass
class Mahasiswa:
    nim: str
    mata_kuliah: List[str]
    prioritas: List[int]
    
    def __hash__(self):
        return hash(self.nim)

    def __eq__(self, other):
        if not isinstance(other, Mahasiswa):
            return False
        return self.nim == other.nim


@dataclass
class Dosen:
    nama: str
    mata_kuliah_diampu: List[str]
    waktu_preferensi: List[Waktu]

    def __hash__(self):
        return hash(self.nama)

    def __eq__(self, other):
        if not isinstance(other, Dosen):
            return False
        return self.nama == other.nama