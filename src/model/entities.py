from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Ruangan:
    kode_ruangan: str
    kuota_ruangan: int


@dataclass
class Waktu:
    hari: str
    jam: int


@dataclass
class MataKuliah:
    kode: str
    jumlah_mahasiswa: int
    jumlah_sks: int


@dataclass
class Mahasiswa:
    nim: str
    mata_kuliah: List[str]
    prioritas: List[int]
    
@dataclass
class Dosen:
    nama: str
    mata_kuliah_diampu: List[str]
    waktu_preferensi: List[Waktu]