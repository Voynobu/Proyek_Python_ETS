#Author : Zaidan Zulkaisi Setiaji
#NIM/Kelas : 241524031/1A-D4
#Deskripsi : class untuk JadwalPoli

class JadwalPoli():
    def __init__(self, nama):
        self.nama = nama
        self.daftar_poli = []

    def TambahPoli(self, poli):
        self.daftar_poli.append(poli)

    def TampilPoli(self):
        print (f"Daftar Poli :")
        for idx, poli in enumerate (self.daftar_poli, start=1):
            print(f"{idx}. {poli}")
        
    def PilihanPoli(self, pilihan):
        if 1 <= pilihan <= len(self.daftar_poli):
            return self.daftar_poli[pilihan - 1]
        else:
            return None