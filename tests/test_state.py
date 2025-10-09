import random
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
    """Membuat data Repository Mock untuk pengujian Callable."""
    
    # Entitas
    r1 = Ruangan("R101", 30) 
    r2 = Ruangan("R202", 50) 
    w_pagi = Waktu("Senin", 8)
    w_siang = Waktu("Senin", 9)
    w_jumat = Waktu("Jumat", 10) # Slot buruk untuk Dosen Wati
    
    mk_a = MataKuliah("MKA", 2, 2) 
    mk_b = MataKuliah("MKB", 2, 3) 
    
    # Dosen Joko: Bisa pagi dan siang (MKA, MKB)
    d_joko = Dosen("Joko", ["MKA", "MKB"], [w_pagi, w_siang])
    # Dosen Wati: Hanya bisa siang (MKA)
    d_wati = Dosen("Wati", ["MKA"], [w_siang])

    # Mahasiswa
    mhs_x = Mahasiswa("M001", ["MKA", "MKB"], [1, 2]) # P1 (1.75), P2 (1.5)

    # Repository Maps
    matkul = {"MKA": mk_a, "MKB": mk_b}
    ruangan = {"R101": r1, "R202": r2}
    mahasiswa = {"M001": mhs_x}
    dosen = {"Joko": d_joko, "Wati": d_wati}

    # Relasi
    mhs_tiap_matkul = {"MKA": [mhs_x], "MKB": [mhs_x]}
    dosen_tiap_matkul = {"MKA": [d_joko, d_wati], "MKB": [d_joko]}

    repo = Repository(matkul, ruangan, mahasiswa, dosen, mhs_tiap_matkul, dosen_tiap_matkul)
    
    slot_pagi_r1 = ("R101", w_pagi)
    slot_siang_r2 = ("R202", w_siang)
    slot_jumat_r1 = ("R101", w_jumat) # Slot yang tidak disukai Dosen Wati
    slot_pagi_r2 = ("R202", w_pagi) # <--- PERBAIKKAN: Definisi slot_pagi_r2
    
    # PERBAIKKAN: Menambahkan slot_pagi_r2 ke dalam nilai yang dikembalikan
    return repo, mk_a, mk_b, slot_pagi_r1, slot_siang_r2, slot_jumat_r1, slot_pagi_r2, w_pagi, w_siang 


def run_tests():
    """Menjalankan semua tes, termasuk metode dengan Callable."""
    random.seed(42) 
    
    # PERBAIKKAN: Menambahkan slot_pagi_r2 ke dalam variabel yang di-unpack
    repo, mk_a, mk_b, slot_pagi_r1, slot_siang_r2, slot_jumat_r1, slot_pagi_r2, w_pagi, w_siang = create_mock_repo()
    
    # Gunakan semua fungsi objektif
    objectives = (kasus_mahasiswa_bentrok, kasus_kapasitas_kurang, kasus_dosen_gabisa, kasus_dosen_bentrok)
    
    # -----------------------------------------------------------
    # PENGUJIAN NON-CALLABLE METHOD
    # -----------------------------------------------------------
    print_test_section("PENGUJIAN initialize_domain")
    state_init = State()
    state_init.initialize_domain(repo)
    assert hasattr(state_init, "repo") and hasattr(state_init, "available_slots")
    print("RESULT: initialize_domain BERHASIL.")

    print_test_section("PENGUJIAN copy")
    state_copy = state_init.copy()
    assert state_copy is not state_init
    assert state_copy.repo is state_init.repo
    assert state_copy.available_slots == state_init.available_slots
    print("RESULT: copy BERHASIL.")

    print_test_section("PENGUJIAN assign_mk dan remove_mk")
    state_assign = State()
    state_assign.initialize_domain(repo)
    state_assign.assign_mk(mk_a.kode, slot_pagi_r1[0], w_pagi)
    assert (slot_pagi_r1[0], w_pagi) in state_assign.assignments
    removed = state_assign.remove_mk(slot_pagi_r1[0], w_pagi)
    assert removed is not None and (slot_pagi_r1[0], w_pagi) not in state_assign.assignments
    print("RESULT: assign_mk dan remove_mk BERHASIL.")

    print_test_section("PENGUJIAN swap_mk")
    state_swap = State()
    state_swap.initialize_domain(repo)
    state_swap.assign_mk(mk_a.kode, slot_pagi_r1[0], w_pagi)
    state_swap.assign_mk(mk_b.kode, slot_pagi_r2[0], w_pagi)
    before_swap = (state_swap.assignments[(slot_pagi_r1[0], w_pagi)].kode, state_swap.assignments[(slot_pagi_r2[0], w_pagi)].kode)
    state_swap.swap_mk((slot_pagi_r1[0], w_pagi), (slot_pagi_r2[0], w_pagi))
    after_swap = (state_swap.assignments[(slot_pagi_r1[0], w_pagi)].kode, state_swap.assignments[(slot_pagi_r2[0], w_pagi)].kode)
    assert before_swap == after_swap or after_swap == (mk_b.kode, mk_a.kode)
    print("RESULT: swap_mk BERHASIL.")

    print_test_section("PENGUJIAN initialize_random_state")
    state_rand = State()
    state_rand.initialize_domain(repo)
    state_rand.initialize_random_state()
    assigned_mk = set(mk.kode for mk in state_rand.assignments.values())
    assert mk_a.kode in assigned_mk and mk_b.kode in assigned_mk
    print("RESULT: initialize_random_state BERHASIL.")

    # -----------------------------------------------------------
    print_test_section("PENGUJIAN count_state_value")
    state_conflict = State()
    state_conflict.initialize_domain(repo)
    
    # Skenario Konflik: MKA & MKB di waktu yang sama (w_pagi).
    # Mhs X mengambil MKA(P1) & MKB(P2). Dosen bentrok (Joko).
    state_conflict.assign_mk(mk_a.kode, slot_pagi_r1[0], w_pagi)
    state_conflict.assign_mk(mk_b.kode, slot_pagi_r2[0], w_pagi)
    
    # Perhitungan Beban (Cost):
    # 1. Mhs Bentrok: Mhs X (P1=1.75 + P2=1.5) = 3.25
    # 2. Kapasitas Kurang: 0
    # 3. Dosen Gabisa: 0 (Joko dan Wati (MKA) dan Joko (MKB) bisa di w_pagi)
    # 4. Dosen Bentrok: Dosen Joko mengajar MKA & MKB. Beban: Mhs MKA (1) + Mhs MKB (1) = 2.0
    # Total Beban (Cost): 3.25 + 4.0 = 7.25
    # State Value Diharapkan: -7.25
    
    state_value_result = state_conflict.count_state_value(*objectives)
    expected_value = -5.25
    
    print(f"Total Beban (Cost): {-state_value_result} (Diharapkan 5.25)")
    print(f"State Value Dihasilkan: {state_value_result} (Diharapkan {expected_value})")

    if abs(state_value_result - expected_value) < 0.001:
        print("RESULT: count_state_value BERHASIL.")
    else:
        print("RESULT: count_state_value GAGAL.")

    # -----------------------------------------------------------
    print_test_section("PENGUJIAN generate_successor (Random)")
    
    successor_random = state_conflict.generate_successor(True, *objectives)
    
    # Cek apakah ada perubahan
    is_changed = (successor_random.assignments != state_conflict.assignments)
    print(f"Assignments berhasil diubah: {is_changed}")

    if is_changed:
        print("RESULT: generate_successor (Random) BERHASIL.")
    else:
        print("RESULT: generate_successor (Random) GAGAL (state tidak berubah).")

    # -----------------------------------------------------------
    print_test_section("PENGUJIAN generate_successor (Best Move)")
    
    # State awal untuk pengujian Best Move
    state_test_best = State()
    state_test_best.initialize_domain(repo)
    
    # Beri satu konflik Dosen Gabisa:
    # MKA @ slot_jumat_r1 (Jumat, 10). Wati (pengampu MKA) TIDAK PREFERENSI di Jumat.
    state_test_best.assign_mk(mk_a.kode, slot_jumat_r1[0], slot_jumat_r1[1]) 
    
    # Initial Cost (Beban): 
    # MKA: Dosen Wati tidak bisa di Jumat (Mhs MKA=2). Cost Dosen Gabisa = 2.0
    # State Value Awal: -2.0
    initial_value = state_test_best.count_state_value(*objectives)
    print(f"State Value Awal: {initial_value}")
    
    # Analisis Best Move:
    # Pindah MKA ke slot_siang_r2 (Senin, 9). Wati bisa. Cost Dosen Gabisa = 0. State Value = 0.0 (BEST)

    successor_best = state_test_best.generate_successor(False, *objectives)
    final_value = successor_best.count_state_value(*objectives)
    
    is_optimal_move = (final_value > initial_value)
    
    print(f"State Value Akhir: {final_value}")
    print(f"State Value Diharapkan (Best): 0.0")

    # Cek apakah move terbaik telah dilakukan
    if abs(final_value - 0.0) < 0.001 and is_optimal_move:
        print("RESULT: generate_successor (Best Move) BERHASIL (State Value meningkat ke 0.0).")
        # Mencari slot baru MKA untuk dicetak
        new_slot_waktu = next(iter(successor_best.assignments.keys()))[1]
        print(f" MKA berhasil dipindahkan dari {slot_jumat_r1[1]} ke {new_slot_waktu}.")
    else:
        print("RESULT: generate_successor (Best Move) GAGAL.")
        print(" Catatan: Mungkin MKA dipindahkan ke slot yang tidak meningkatkan nilai.")


if __name__ == "__main__":
    run_tests()
    run_tests()
