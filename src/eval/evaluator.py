# Objective Cost

from src.model.state import State

def kasus_mahasiswa_bentrok(state: State) -> float:
    """Menghitung beban untuk matakuliah yang bentrok berdasarkan prioritas mahasiswa"""
    list_matkul_bentrok = [
        list_matkul for _, list_matkul in state.times_to_mk.items() if len(list_matkul) > 1
    ]
    beban_state = 0.0
    for matkul_bentrok in list_matkul_bentrok:
        mahasiswa_mungkin_bentrok = [
            set(state.repo.mahasiswa_tiap_matkul[matkul.kode]) for matkul in matkul_bentrok
        ]
        mahasiswa_bentrok = set.intersection(*mahasiswa_mungkin_bentrok)
        if not mahasiswa_bentrok:
            continue

        for mahasiswa in mahasiswa_bentrok:
            for matkul in matkul_bentrok:
                try:
                    idx = mahasiswa.mata_kuliah.index(matkul.kode)
                    prioritas = mahasiswa.prioritas[idx]
                except ValueError:
                    prioritas = 4  # Default priority if not found

                if prioritas == 1:
                    beban_state += 1.75
                elif prioritas == 2:
                    beban_state += 1.5
                elif prioritas == 3:
                    beban_state += 1.25
                else:
                    beban_state += 1
    return beban_state


def kasus_kapasitas_kurang(state:State) -> int:
    """Menghitung beban untuk setiap slot yang ditempati oleh 
    matakuliah dengan pendaftar melebihi kapasitas"""
    
    beban_state = 0
    for slot, matkul in state.assignments.items():
        jumlah_mahasiswa = len(state.repo.mahasiswa_tiap_matkul[matkul.kode])
        kapasitas_ruangan = state.repo.ruangan[slot[0]].kuota_ruangan
        sks_matakuliah = matkul.jumlah_sks
        beban_state += max(0, (jumlah_mahasiswa - kapasitas_ruangan)*sks_matakuliah)
        # beban_state += max(0, (jumlah_mahasiswa - kapasitas_ruangan))
    
    return beban_state


def kasus_dosen_gabisa(state:State) -> int:
    """Menghitung beban matakuliah yang tidak bisa diajar oleh dosen pada waktu tersebut"""
    beban_state = 0
    for slot, matkul in state.assignments.items():
        dosen_pengampu = state.repo.dosen_tiap_matkul[matkul.kode]
        add_beban_state = 0
        for dosen in dosen_pengampu:
            # Minimal ada 1 dosen yang bisa mengajar
            if slot[1] in dosen.waktu_preferensi:
                add_beban_state *= 0
                break
            else:
                add_beban_state += len(state.repo.mahasiswa_tiap_matkul[matkul.kode])
        beban_state += add_beban_state

    return beban_state


def kasus_dosen_bentrok(state: State) -> int:
    """Menghitung beban dosen yang matkulnya berbentrokan"""
    list_matkul_bentrok = [
        list_matkul for _, list_matkul in state.times_to_mk.items() if len(list_matkul) > 1
    ]
    beban_state = 0
    for matkul_bentrok in list_matkul_bentrok:
        dosen_mungkin_bentrok = [
            set(state.repo.dosen_tiap_matkul[matkul.kode]) for matkul in matkul_bentrok
        ]
        # Compare all pairs of lecturer sets for conflicts
        for i in range(len(dosen_mungkin_bentrok)):
            for j in range(i + 1, len(dosen_mungkin_bentrok)):
                if not dosen_mungkin_bentrok[i].isdisjoint(dosen_mungkin_bentrok[j]):
                    # Add the number of students enrolled in both conflicting courses
                    beban_state += len(state.repo.mahasiswa_tiap_matkul[matkul_bentrok[i].kode])
                    beban_state += len(state.repo.mahasiswa_tiap_matkul[matkul_bentrok[j].kode])
    return beban_state