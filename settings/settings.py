
# kumpulan settingan global
import os 

def validPath(path: str) -> bool: # ngecek kalo dia input harus json dan ada Valid 
    return path.endswith(".json") and os.path.isfile(path) 
# ini brarti blm termasuk kalo isi jsonnya sesuai 

# TODO:
def validJSONFormat(path: str) -> bool: 
    #  nah buat disini buat cek format JSONNYA bener ato kaga
    # smeentara return true dulu
    return True   

