from typing import Any
from src.io.repo_loader import create_repo, Repository


def print_entity(title: str, obj: Any) -> None:
    print(f"\n=== {title} ===")
    for attr, val in vars(obj).items():
        print(f"{attr:20}: {val}")


def run(path: str) -> None:
    repo = create_repo(path)

    print("\n=== REPO ===")
    print(f"jumlah mata_kuliah : {len(repo.mata_kuliah)}")
    print(f"jumlah ruangan     : {len(repo.ruangan)}")
    print(f"jumlah mahasiswa   : {len(repo.mahasiswa)}")
    print(f"jumlah dosen       : {len(repo.dosen)}")

    # karena sekarang dictionary, kita loop lewat .items()
    for i, (kode, mk) in enumerate(repo.mata_kuliah.items(), start=1):
        print_entity(f"MataKuliah #{i} (kode={kode})", mk)

    for i, (kode, r) in enumerate(repo.ruangan.items(), start=1):
        print_entity(f"Ruangan #{i} (kode={kode})", r)

    for i, (nim, m) in enumerate(repo.mahasiswa.items(), start=1):
        print_entity(f"Mahasiswa #{i} (nim={nim})", m)

    for i, (nama, d) in enumerate(repo.dosen.items(), start=1):
        print_entity(f"Dosen #{i} (nama={nama})", d)

    print("\n=== Mahasiswa tiap Mata Kuliah ===")
    for kode, daftar_mhs in repo.mahasiswa_tiap_matkul.items():
        print(f"{kode}: {[m.nim for m in daftar_mhs]}")

    print("\n=== Dosen tiap Mata Kuliah ===")
    for kode, daftar_dsn in repo.dosen_tiap_matkul.items():
        print(f"{kode}: {[d.nama for d in daftar_dsn]}")

if __name__ == "__main__":
    json_path = "data/sample_input.json"  
    run(json_path)
