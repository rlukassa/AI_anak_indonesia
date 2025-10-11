# test_genetic.py
import unittest
import json
from typing import List, Callable

from src.io.repo_loader import Repository, create_repo
from src.model.entities import Dosen, MataKuliah, Mahasiswa, Waktu, Ruangan
from src.model.state import State
from src.eval.evaluator import (
    kasus_mahasiswa_bentrok,
    kasus_kapasitas_kurang,
    kasus_dosen_gabisa,
    kasus_dosen_bentrok,
)
from src.algorithms.genetic import GeneticAlgorithm

# Kode JSON yang akan digunakan sebagai input data
REPO_DATA_JSON = {
    "kelas_mata_kuliah": [
        {
            "kode": "IF3071_K01",
            "jumlah_mahasiswa": 60,
            "sks": 3
        },
        {
            "kode": "IF3130_K01",
            "jumlah_mahasiswa": 45,
            "sks": 2
        },
        {
            "kode": "IF3110_K02",
            "jumlah_mahasiswa": 70,
            "sks": 3
        },
        {
            "kode": "IF3140_K01",
            "jumlah_mahasiswa": 55,
            "sks": 2
        }
    ],
    "ruangan": [
        {
            "kode": "7609",
            "kuota": 60
        },
        {
            "kode": "7606",
            "kuota": 80
        },
        {
            "kode": "multimedia",
            "kuota": 40
        }
    ],
    "mahasiswa": [
        {
            "nim": "13523601",
            "daftar_mk": ["IF3071_K01", "IF3130_K01"],
            "prioritas": [1, 2]
        },
        {
            "nim": "135236641",
            "daftar_mk": ["IF3110_K02", "IF3130_K01"],
            "prioritas": [1, 2]
        },
        {
            "nim": "13523669",
            "daftar_mk": ["IF3140_K01", "IF3071_K01"],
            "prioritas": [1, 2]
        },
        {
            "nim": "13523600",
            "daftar_mk": ["IF3110_K02"],
            "prioritas": [1]
        }
    ],
    "dosen": [
        {
            "nama": "Prof. Muhaman Nazih Najmudin, M.Eng.",
            "mata_kuliah_diampu": ["IF3071_K01", "IF3140_K01"],
            "waktu_preferensi": [["Senin", 9], ["Senin", 10], ["Rabu", 13], ["Kamis", 14], ["Jumat", 15]]
        },
        {
            "nama": "Ir. Brian Ricardo Tamin, S.Kom.",
            "mata_kuliah_diampu": ["IF3110_K02"],
            "waktu_preferensi": [["Selasa", 8], ["Selasa", 9], ["Kamis", 10]]
        },
        {
            "nama": "Drs. Lukas Raja Agripa, M.T., M.Sc.",
            "mata_kuliah_diampu": ["IF3130_K01"],
            "waktu_preferensi": [["Rabu", 9], ["Rabu", 10], ["Jumat", 8]]
        }
    ]
}

# Membuat file JSON sementara untuk pengujian
def create_dummy_json(file_path: str):
    """Membuat file dummy JSON dengan data yang diberikan."""
    with open(file_path, 'w') as f:
        json.dump(REPO_DATA_JSON, f, indent=4)

class JSONParser:
    def __init__(self, path: str):
        with open(path, 'r') as f:
            self.data = json.load(f)

class TestGeneticAlgorithmWithJSON(unittest.TestCase):
    def setUp(self):
        # Mengatur path file JSON sementara
        self.json_path = "dummy_repo_data.json"
        
        # Mengubah modul 'repo_loader' agar menggunakan JSONParser dummy
        import sys
        sys.modules['src.io.repo_loader'].JSONParser = JSONParser
        
        create_dummy_json(self.json_path)
        self.repo = create_repo(self.json_path)

        # Mendefinisikan fungsi objektif yang akan digunakan
        self.objectives: List[Callable] = [
            kasus_mahasiswa_bentrok,
            kasus_kapasitas_kurang,
            kasus_dosen_gabisa,
            kasus_dosen_bentrok,
        ]

    def test_genetic_algorithm_solves_problem(self):
        """
        Menguji apakah Algoritma Genetika menemukan solusi dengan nilai beban 0
        untuk data dari file JSON.
        """
        # Inisialisasi state awal
        initial_state = State()
        initial_state.initialize_domain(self.repo)

        # Inisialisasi dan jalankan algoritma genetika
        ga = GeneticAlgorithm(initial_state)
        # Menjalankan GA dengan parameter yang disesuaikan
        solution = ga.search(
            10,
            100000000000000000,
            *self.objectives
        )

        # Verifikasi hasil
        print("\n--- Hasil Uji Algoritma Genetika dengan Data JSON ---")
        print(f"Nilai akhir solusi (state_value): {solution.state_value}")
        
        # Periksa apakah nilai beban adalah nol (atau sangat mendekati nol)
        self.assertLessEqual(solution.state_value, 0, "State value harus 0 atau kurang")
        
        # Periksa setiap pelanggaran secara terpisah untuk verifikasi yang lebih rinci
        mahasiswa_bentrok_val = kasus_mahasiswa_bentrok(solution)
        kapasitas_kurang_val = kasus_kapasitas_kurang(solution)
        dosen_gabisa_val = kasus_dosen_gabisa(solution)
        dosen_bentrok_val = kasus_dosen_bentrok(solution)

        print(f"Beban Mahasiswa Bentrok: {mahasiswa_bentrok_val}")
        print(f"Beban Kapasitas Kurang: {kapasitas_kurang_val}")
        print(f"Beban Dosen Tidak Bisa: {dosen_gabisa_val}")
        print(f"Beban Dosen Bentrok: {dosen_bentrok_val}")

        self.assertEqual(mahasiswa_bentrok_val, 0, "Pelanggaran mahasiswa bentrok harus 0.")
        self.assertEqual(kapasitas_kurang_val, 0, "Pelanggaran kapasitas kurang harus 0.")
        self.assertEqual(dosen_gabisa_val, 0, "Pelanggaran dosen tidak bisa harus 0.")
        self.assertEqual(dosen_bentrok_val, 0, "Pelanggaran dosen bentrok harus 0.")
        
        if solution.state_value == 0:
            print("\n✅ Algoritma Genetika berhasil menemukan solusi optimal!")
        else:
            print("\n❌ Algoritma Genetika tidak menemukan solusi optimal dalam iterasi yang diberikan.")

# Jalankan test
if __name__ == '__main__':
    unittest.main()