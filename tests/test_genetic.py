import unittest
from typing import List, Callable

from src.io.repo_loader import create_repo
from src.model.state import State
from src.eval.evaluator import (
    kasus_mahasiswa_bentrok,
    kasus_kapasitas_kurang,
    kasus_dosen_gabisa,
    kasus_dosen_bentrok,
)
from src.algorithms.genetic import GeneticAlgorithm


class TestGeneticAlgorithmWithJSON(unittest.TestCase):
    def setUp(self):
        self.json_path = "data/sample_input.json"
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
        initial_state.initialize_random_state(*self.objectives)

        print("======================================================================")
        print("Initial State")
        print("----------------------------------------------------------------------")
        # Periksa setiap pelanggaran secara terpisah untuk verifikasi yang lebih rinci
        mahasiswa_bentrok_val = kasus_mahasiswa_bentrok(initial_state)
        kapasitas_kurang_val = kasus_kapasitas_kurang(initial_state)
        dosen_gabisa_val = kasus_dosen_gabisa(initial_state)
        dosen_bentrok_val = kasus_dosen_bentrok(initial_state)
        print(f"Beban Mahasiswa Bentrok: {mahasiswa_bentrok_val}")
        print(f"Beban Kapasitas Kurang: {kapasitas_kurang_val}")
        print(f"Beban Dosen Tidak Bisa: {dosen_gabisa_val}")
        print(f"Beban Dosen Bentrok: {dosen_bentrok_val}")
        print("======================================================================")
        print()

        # Inisialisasi dan jalankan algoritma genetika
        ga = GeneticAlgorithm(
            jml_parent=10,
            jml_iterasi=1000
        )
        # Menjalankan GA dengan parameter yang disesuaikan
        solution, _ = ga.search(
            initial_state,
            *self.objectives,
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