
import sqlite3
import os
import settings.settings as Query 


class SQLOutput: 
    def __init__(self, db_name): 
        # Buat folder output di dalam folder database
        database_dir = os.path.dirname(__file__)  # folder database saat ini
        outputDir = os.path.join(database_dir, 'output')
        os.makedirs(outputDir, exist_ok=True)

        # Path lengkap ke database di folder database/output/
        self.db_path = os.path.join(outputDir, db_name)
        self.conn = sqlite3.connect(self.db_path) 
        self.cursor = self.conn.cursor()
 
    def buatTable(self, tabel : str ) -> None: # maksudnya outputnya tabel si di output/  
        buatTabel = Query.querySQL["buatTabel_SQL"].format(tabel=tabel) 
        self.cursor.execute(buatTabel) 
        self.conn.commit()
        # Auto-refresh untuk memastikan tabel tersimpan dengan benar
        self.autoRefresh()
 
    def insertData(self, tabel: str, jam: int, senin=None, selasa=None, rabu=None, kamis=None, jumat=None):
        insertQuery = Query.querySQL["insertData_SQL"].format(tabel=tabel)
        self.cursor.execute(insertQuery, (jam, senin, selasa, rabu, kamis, jumat))
        self.conn.commit()
        # print(f"Data berhasil dimasukkan ke tabel '{tabel}': Jam {jam}") debug
    
    def insertSampleData(self, tabel: str): # ntar diganti dengan insertData()
        sample_data = [
            (8, "Matematika", "Fisika", None, "Kimia", "Biologi"),
            (9, "Bahasa Inggris", None, "Sejarah", "Geografi", None),
            (10, None, "Olahraga", "Seni", None, "Agama"),
        ]
        for data in sample_data:
            self.insertData(tabel, *data)
        # Auto-refresh setelah insert data
        self.autoRefresh()
    
    def getAllTables(self):
        self.autoRefresh()  # Refresh untuk mendapatkan data terbaru
        self.cursor.execute(Query.querySQL["lihatSemuaTabel_SQL"])
        tables = self.cursor.fetchall()
        if tables: # ini debug doang, tabel nya apa aja
            for table in tables:
                print(f"- {table[0]}")
        else:
            print("Tidak ada tabel dalam database.")
        return tables
    
    def closeConnection(self):
        self.conn.close()
        print("Koneksi database ditutup.")
    
    def autoRefresh(self):
        if hasattr(self, 'conn'):
            self.conn.close()
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.conn.execute("PRAGMA synchronous = FULL;")
        self.conn.execute("PRAGMA journal_mode = DELETE;")

    def hapusTable(self, tabel: str) -> None:
        # Cek apakah tabel ada sebelum menghapus
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (tabel,))
        table = self.cursor.fetchone()
        if table:
            self.cursor.execute(Query.querySQL["hapusTabel_SQL"].format(tabel=tabel))
            self.conn.commit()
            self.autoRefresh()
    
    def __del__(self): 
        if hasattr(self, 'conn'):
            self.conn.close()