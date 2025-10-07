from dataclasses import dataclass
from typing import List
from .json_parser import JSONParser
from src.model.entities import *

# -----------------------------
#  Repository: data container
# -----------------------------
@dataclass
class Repository:
    mata_kuliah: List[MataKuliah]
    ruangan: List[Ruangan]
    mahasiswa: List[Mahasiswa]
    dosen: List[Dosen]

def _to_waktu(raw_slot: list) -> Waktu:
    hari, jam = raw_slot
    return Waktu(hari=hari, jam=jam)

def create_repo(path: str) -> Repository:
    parser = JSONParser(path)
    data = parser.data

    mk_list = [
        MataKuliah(item["kode"], int(item["jumlah_mahasiswa"]), int(item["sks"]))
        for item in data.get("kelas_mata_kuliah", [])
    ]

    ruangan_list = [
        Ruangan(item["kode"], int(item["kuota"]))
        for item in data.get("ruangan", [])
    ]

    mahasiswa_list = [
        Mahasiswa(
            nim=item["nim"],
            mata_kuliah=item.get("daftar_mk", []),
            prioritas=[int(p) for p in item.get("prioritas", [])],
        )
        for item in data.get("mahasiswa", [])
    ]

    dosen_list = [
        Dosen(
            nama=item["nama"],
            mata_kuliah_diampu=item.get("mata_kuliah_diampu", []),
            waktu_preferensi=[_to_waktu(s) for s in item.get("waktu_preferensi", [])],
        )
        for item in data.get("dosen", [])
    ]

    return Repository( mata_kuliah=mk_list, ruangan=ruangan_list, mahasiswa=mahasiswa_list, dosen=dosen_list,)