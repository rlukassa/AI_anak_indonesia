from dataclasses import dataclass
from typing import Dict, Set
from .json_parser import JSONParser
from src.model.entities import *


# -----------------------------
#  Repository: data container
# -----------------------------
@dataclass
class Repository:
    mata_kuliah: Dict[str, MataKuliah]
    ruangan: Dict[str, Ruangan]
    mahasiswa: Dict[str, Mahasiswa]
    dosen: Dict[str, Dosen]

    # tambahan relasi
    mahasiswa_tiap_matkul: Dict[str, List[Mahasiswa]]
    dosen_tiap_matkul: Dict[str, List[Dosen]]


def _to_waktu(raw_slot: list) -> Waktu:
    hari, jam = raw_slot
    return Waktu(hari=hari, jam=jam)


def create_repo(path: str) -> Repository:
    parser = JSONParser(path)
    data = parser.data

    # --- buat dictionary utama ---
    mk_dict = {
        item["kode"]: MataKuliah(
            item["kode"], int(item["jumlah_mahasiswa"]), int(item["sks"])
        )
        for item in data.get("kelas_mata_kuliah", [])
    }

    ruangan_dict = {
        item["kode"]: Ruangan(item["kode"], int(item["kuota"]))
        for item in data.get("ruangan", [])
    }

    mahasiswa_dict = {
        item["nim"]: Mahasiswa(
            nim=item["nim"],
            mata_kuliah=item.get("daftar_mk", []),
            prioritas=[int(p) for p in item.get("prioritas", [])],
        )
        for item in data.get("mahasiswa", [])
    }

    dosen_dict = {
        item["nama"]: Dosen(
            nama=item["nama"],
            mata_kuliah_diampu=item.get("mata_kuliah_diampu", []),
            waktu_preferensi=[_to_waktu(s) for s in item.get("waktu_preferensi", [])],
        )
        for item in data.get("dosen", [])
    }

    # --- buat relasi mahasiswa <-> mata kuliah ---
    mahasiswa_tiap_matkul: Dict[str, List[Mahasiswa]] = {kode: list() for kode in mk_dict}
    for m in mahasiswa_dict.values():
        for kode_mk in m.mata_kuliah:
            if kode_mk in mahasiswa_tiap_matkul:
                mahasiswa_tiap_matkul[kode_mk].append(m)

    # --- buat relasi dosen <-> mata kuliah ---
    dosen_tiap_matkul: Dict[str, List[Dosen]] = {kode: list() for kode in mk_dict}
    for d in dosen_dict.values():
        for kode_mk in d.mata_kuliah_diampu:
            if kode_mk in dosen_tiap_matkul:
                dosen_tiap_matkul[kode_mk].append(d)

    # --- return Repository ---
    return Repository(
        mata_kuliah=mk_dict,
        ruangan=ruangan_dict,
        mahasiswa=mahasiswa_dict,
        dosen=dosen_dict,
        mahasiswa_tiap_matkul=mahasiswa_tiap_matkul,
        dosen_tiap_matkul=dosen_tiap_matkul,
    )
