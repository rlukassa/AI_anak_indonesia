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

    # print
    for i, mk in enumerate(repo.mata_kuliah, start=1):
        print_entity(f"MataKuliah #{i}", mk)

    for i, r in enumerate(repo.ruangan, start=1):
        print_entity(f"Ruangan #{i}", r)

    for i, m in enumerate(repo.mahasiswa, start=1):
        print_entity(f"Mahasiswa #{i}", m)

    for i, d in enumerate(repo.dosen, start=1):
        print_entity(f"Dosen #{i}", d)


if __name__ == "__main__":
    json_path = "data/sample_input.json"  
    run(json_path)
