import services.ReadInput_services as readServices 
import database.Output as dbOutput 

def ujiCoba() :
    readInput = readServices.ReadInputService('') 
    db = dbOutput.SQLOutput('output.db')
    readInput.bacaInput('TestingJson.json') 
    print("\n") 
    print(readInput.getFileInput()) 
    print("\n") 
    print(readInput.getKelas_MataKuliah()) 
    print("\n") 
    print(readInput.getRuangan()) 
    print("\n") 
    print(readInput.getMahasiswa()) 
    print("\n") 
    print(readInput.getALLNim())
    print("\n")
    print(readInput.getPrioritasByNim(13523601)) 
    print("\n")
    print(readInput.getDaftarMKByNim(13523601))
    print("\n")

    #Perihal SQL - karena sempet perlu refresh kalo udah dihapus
    # Buat tabel dengan nama 'jadwal_kuliah'
    nama_tabel = "jadwal_kuliah"
    db.buatTable(nama_tabel)
    # Tampilkan semua tabel yang ada
    db.getAllTables()
    # butuh insert data (dari json) -- tapi ntaran aj


    # db.insertSampleData(nama_tabel)
    db.hapusTable(nama_tabel)
    
    
    # Lihat semua tabel yang tersisa
    db.getAllTables()

    ### JADI NTAR IDENYA untuk nyimpen state dari 1 - 10 misalkan ... itu simpan di json
    ### terus pake SQL (Output.py) buat transfer ke tabel SQL
    ### SQL ini cuman biar tabular aja (numpang tabel doang)


if __name__ == "__main__":
    ujiCoba()
    
### NTAR DIGANTI JADI Main() ###