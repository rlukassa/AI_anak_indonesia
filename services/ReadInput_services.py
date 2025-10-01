import json

class ReadInputService: 
    def __init__(self, fileInput):
        self.fileInput = fileInput # file input sebagai .json 
    
    def bacaInput(self, f) -> None : 
        with open(f, 'r') as file: # baca input dari file .json 
            self.fileInput = json.load(file) 
            # return self.fileInput 
    
    def getFileInput(self) -> dict:  #getter json file yang diinput 
        return self.fileInput
    
    # ini getter dari json terkait list kelas mata kuliah, ruangan, mahasiswa
    def getKelas_MataKuliah(self) -> list: 
        return self.fileInput['kelas_mata_kuliah']

    def getRuangan(self) -> list: 
        return self.fileInput['ruangan']
    
    def getMahasiswa(self) -> list: 
        return self.fileInput['mahasiswa']
    
    # kalau butuh list sekumpulan nim, daftar_mk , prioritas secara keseluruhan dalam list, contoh : 
    # [13523001, 13523002, 13523003 ... ]
    # w anggap nim nya sebagai key, jadi ntar idenya punya list nim, ntar manggil bawahnya tinggal

    def getALLNim(self) -> list: 
        listNim = [] 
        for mhs in self.getMahasiswa(): 
            listNim.append(mhs['nim']) # kan mhs dict
        return listNim 
    
    ### main info daleman pake key = nim 
    # karena di jsonnya pakai string, jadi str(nim)
    def getPrioritasByNim(self, nim) -> str: 
        if str(nim) not in self.getALLNim():
            return "gaada nim di json"
        for mhs in self.getMahasiswa():
            if mhs['nim'] == str(nim):
                return mhs['prioritas']
        return "Tidak ketemu!"
    
    def getDaftarMKByNim(self, nim) -> str: 
        if str(nim) not in self.getALLNim():
            return "gaada nim di json"
        for mhs in self.getMahasiswa():
            if mhs['nim'] == str(nim):
                return mhs['daftar_mk']
        return "Tidak ketemu!"
    
    ## KALAU BUTUH GABUNGAN DAFTAR MK + PRIORITAS -> BOLEH TAMBAHIN 1 FUNGSI, tapi kata w gak perlu sih
    ## tinggal concat 

