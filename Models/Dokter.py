#Author : Zaidan Zulkaisi Setiaji
#NIM/Kelas : 241524031/1A-D4
#Deskripsi : class untuk JadwalPoli

class Dokter:
    def __init__(self, nama, spesialis):
        self.nama = nama
        self.spesialis = spesialis
    
    def __str__(self):
        return f"{self.nama} ({self.spesialis})"
