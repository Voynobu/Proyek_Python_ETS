#Author : Zaidan Zulkaisi Setiaji
#NIM/Kelas : 241524031/1A-D4
#Deskripsi : class untuk Jadwal

import json
from datetime import datetime, time
from Utils.FileHandler import load_data, save_data

class Jadwal:
    def __init__(self, dokter, hari, jam_awal, jam_akhir):
        self.dokter = dokter
        self.hari = hari
        self.jam_awal = jam_awal
        self.jam_akhir = jam_akhir

    def status_dokter(self):
        saat_ini = datetime.now()
        hari_saat_ini = saat_ini.strftime("%A")
        waktu_saat_ini = saat_ini.time()

        jam_awal = datetime.strptime(self.jam_awal, "%H:%M").time()
        jam_akhir = datetime.strptime(self.jam_akhir, "%H:%M").time()

        return "Available" if hari_saat_ini == self.hari and jam_awal <= waktu_saat_ini <= jam_akhir else "Unavailable"

    def __str__(self):
        status = self.status_dokter()
        return f"{self.dokter} -- {self.hari} ({self.jam_awal} - {self.jam_akhir}). Status : {status}"

    
