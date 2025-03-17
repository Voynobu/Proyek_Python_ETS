from datetime import datetime, time

#Author : Zaidan Zulkaisi Setiaji
#NIM/Kelas : 241524031/1A-D4
#Deskripsi : class untuk Jadwal

class Jadwal:
    def __init__(self, dokter, hari, jam_awal, jam_akhir):
        self.dokter = dokter
        self.hari = hari
        self.jam_awal = jam_awal
        self.jam_akhir = jam_akhir

    def StatusDokter(self):
        saatini = datetime.now()
        Hari_saatini = saatini.strftime("%A")
        Waktu_saatini = saatini.time()

        jam_awal = datetime.strptime(self.jam_awal, "%H:%M").time()
        jam_akhir = datetime.strptime(self.jam_akhir, "%H:%M").time()

        if Hari_saatini == self.hari and jam_awal <= Waktu_saatini <= jam_akhir:
            return "Available"
        else:
            return "Unavailable"

    def __str__(self):
        status = self.StatusDokter()
        return f"{self.dokter} -- {self.hari} ({self.jam_awal} - {self.jam_akhir}). Status : {status}"
    