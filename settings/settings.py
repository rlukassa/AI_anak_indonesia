
constants = { 
    "Algoritma" : {
        "Hill Climbing" : { 

        }, 

        "Simulated Annealing" : {

        },

        "Genetic Algorithm" : {

        }, 
    },
    "Objective Function" :  { #(HEURISTIK constant kalo ada)  

    }
}


querySQL={
    # buat tabel SQL kosongan 
    # hardcodenya senin - jumat sama jam 
    "buatTabel_SQL" : "CREATE TABLE IF NOT EXISTS {tabel} (id INTEGER PRIMARY KEY, jam INTEGER UNIQUE, senin TEXT, selasa TEXT, rabu TEXT, kamis TEXT, jumat TEXT);" ,  
    #insert data ke tabel 
    "insertData_SQL" : "INSERT INTO {tabel} (jam, senin, selasa, rabu, kamis, jumat) VALUES (?, ?, ?, ?, ?, ?);",
    #hapus tabel berdasarkan nama tabel
    "hapusTabel_SQL" : "DROP TABLE IF EXISTS {tabel};",
    #lihat semua tabel yang ada di database
    "lihatSemuaTabel_SQL" : "SELECT name FROM sqlite_master WHERE type='table';",
    #lihat isi tabel berdasarkan nama tabel
    "lihatIsiTabel_SQL" : "SELECT * FROM {tabel};",
    # cek apakah tabel ada
    "cekTabelAda_SQL" : "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
    # pragma untuk database synchronization
    "pragmaSyncFull_SQL" : "PRAGMA synchronous = FULL;",
    "pragmaJournalDelete_SQL" : "PRAGMA journal_mode = DELETE;"
}