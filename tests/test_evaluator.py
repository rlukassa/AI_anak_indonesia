from src.io.repo_loader import Repository
from src.eval.evaluator import *
from src.model.entities import *
from src.model.state import State

# --- FUNGSI PEMBANTU DAN PENGUJIAN ---

def print_test_section(title: str):
    print(f"\n==========================================")
    print(f"TEST: {title}")
    print(f"==========================================")


def create_mock_repo():
    """Membuat data Repository Mock yang kaya untuk pengujian."""
    
    # 1. ENTITAS
    r1 = Ruangan("R101", 30) # Kuota 30
    r2 = Ruangan("R202", 50) # Kuota 50
    w_pagi = Waktu("Senin", 8)
    w_siang = Waktu("Senin", 9)

    mk_a = MataKuliah("MKA", 2, 2) # Pendaftar 2, SKS 2
    mk_b = MataKuliah("MKB", 2, 3) # Pendaftar 2, SKS 3
    mk_c = MataKuliah("MKC", 2, 4) # Pendaftar 2, SKS 4
    
    # Perbaikan: Tambahkan w_siang agar Joko bisa mengajar di siang hari
    d_joko = Dosen("Joko", ["MKA", "MKB"], [w_pagi, w_siang])
    d_wati = Dosen("Wati", ["MKA", "MKC"], [w_siang])

    # Mahasiswa
    mhs_x = Mahasiswa("M001", ["MKA", "MKB"], [1, 2]) # Ambil A (P1), B (P2)
    mhs_y = Mahasiswa("M002", ["MKB", "MKC"], [3, 4]) # Ambil B (P3), C (P4)
    mhs_z = Mahasiswa("M003", ["MKA", "MKC"], [1, 1]) # Ambil A (P1), C (P1)

    # 2. REPOSITORY MAPS
    matkul = {"MKA": mk_a, "MKB": mk_b, "MKC": mk_c}
    ruangan = {"R101": r1, "R202": r2}
    mahasiswa = {"M001": mhs_x, "M002": mhs_y, "M003": mhs_z}
    dosen = {"Joko": d_joko, "Wati": d_wati}

    # 3. RELASI
    mhs_tiap_matkul = {
        mk_a.kode: [mhs_x, mhs_z],  # 2 Mhs (X, Z)
        mk_b.kode: [mhs_x, mhs_y],  # 2 Mhs (X, Y)
        mk_c.kode: [mhs_y, mhs_z],  # 2 Mhs (Y, Z)
    }
    dosen_tiap_matkul = {
        mk_a.kode: [d_joko, d_wati],
        mk_b.kode: [d_joko],
        mk_c.kode: [d_wati],
    }

    repo = Repository(matkul, ruangan, mahasiswa, dosen, mhs_tiap_matkul, dosen_tiap_matkul)
    
    slot_pagi_r1 = ("R101", w_pagi)
    slot_siang_r2 = ("R202", w_siang)
    slot_pagi_r2 = ("R202", w_pagi)
    
    return repo, slot_pagi_r1, slot_siang_r2, slot_pagi_r2, w_pagi, w_siang


def run_tests():
    """Menjalankan semua tes untuk fungsi-fungsi Evaluator."""
    repo, slot_pagi_r1, slot_siang_r2, slot_pagi_r2, w_pagi, w_siang = create_mock_repo()
    mk_a = repo.mata_kuliah["MKA"]
    mk_b = repo.mata_kuliah["MKB"]
    mk_c = repo.mata_kuliah["MKC"]
    
    # -----------------------------------------------------------
    print_test_section("SKENARIO 1: DASAR (Tanpa Konflik)")
    
    state1 = State()
    state1.initializeDomain(repo)  # Ensure domain is initialized
    state1.assignMK(mk_a.kode, slot_pagi_r1[0], slot_pagi_r1[1]) 
    state1.assignMK(mk_b.kode, slot_siang_r2[0], slot_siang_r2[1]) 
    
    cost1 = state1.countStateValue(
        kasus_mahasiswa_bentrok, 
        kasus_kapasitas_kurang, 
        kasus_dosen_gabisa, 
        kasus_dosen_bentrok
    )
    
    print(f"Total Cost (Tanpa Konflik): {-cost1} (Diharapkan 0.0)")
    if abs(cost1) < 0.001:
        print("RESULT: Skenario 1 BERHASIL.")
    else:
        print("RESULT: Skenario 1 GAGAL. Cost tidak nol.")

    # -----------------------------------------------------------
    print_test_section("SKENARIO 2: KONFLIK MAHASISWA DAN KAPASITAS")

    state2 = State()
    state2.initializeDomain(repo)
    
    # Jadwal bentrok di waktu yang sama: MKA & MKB @ waktu yang sama
    # Assign MKA dan MKB ke waktu yang sama
    state2.assignMK(mk_a.kode, slot_pagi_r2[0], w_pagi) 
    state2.assignMK(mk_b.kode, slot_pagi_r1[0], w_pagi) 
    
    cost_mhs = kasus_mahasiswa_bentrok(state2)
    print(f"Cost Mahasiswa Bentrok: {cost_mhs} (Diharapkan 3.25)")
    
    cost_kapasitas = kasus_kapasitas_kurang(state2)
    print(f"Cost Kapasitas Kurang: {cost_kapasitas} (Diharapkan 0.0)")

    if abs(cost_mhs - 3.25) < 0.001 and abs(cost_kapasitas) < 0.001:
        print("RESULT: Skenario 2 (Mhs & Kapasitas) BERHASIL.")
    else:
        print("RESULT: Skenario 2 (Mhs & Kapasitas) GAGAL.")
        
    # -----------------------------------------------------------
    print_test_section("SKENARIO 3: KONFLIK DOSEN")

    state3 = State()
    state3.initializeDomain(repo)
    
    # Jadwal bentrok di waktu yang sama: MKA & MKC @ waktu yang sama
    # Assign MKA dan MKC ke waktu yang sama
    state3.assignMK(mk_a.kode, slot_pagi_r1[0], w_pagi) 
    state3.assignMK(mk_c.kode, slot_pagi_r2[0], w_pagi) 
    
    cost_dosen_gabisa = kasus_dosen_gabisa(state3)
    print(f"Cost Dosen Gabisa: {cost_dosen_gabisa} (Diharapkan 2.0)")
    
    cost_dosen_bentrok = kasus_dosen_bentrok(state3)
    print(f"Cost Dosen Bentrok: {cost_dosen_bentrok} (Diharapkan 4.0)")

    if abs(cost_dosen_gabisa - 2.0) < 0.001 and abs(cost_dosen_bentrok - 4.0) < 0.001:
        print("RESULT: Skenario 3 (Dosen) BERHASIL.")
    else:
        print("RESULT: Skenario 3 (Dosen) GAGAL.")
        
    print(f"\n==========================================")
    print("SEMUA PENGUJIAN EVALUATOR SELESAI.")
    print(f"==========================================")


if __name__ == "__main__":
    run_tests()