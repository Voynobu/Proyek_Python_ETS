#Author : Zaidan Zulkaisi Setiaji
#NIM/Kelas : 241524031/1A-D4
#Deskripsi : class untuk Poli

import json
from Utils.file_handler import load_data

class Poli:
    def __init__(self, nama_poli):
        self.nama_poli = nama_poli

    def __str__(self):
        return self.nama_poli

    @staticmethod
    def tampilkan_daftar_poli():
        """Menampilkan daftar poli yang tersedia."""
        data_poli = load_data("data/DokterPoli.json")
        if not data_poli:
            print("Belum ada poli yang tersedia.")
            return
        
        print("Daftar Poli:")
        for idx, poli in enumerate(data_poli.keys(), start=1):
            print(f"{idx}. {poli}")
    
    @staticmethod
    def tampilkan_jadwal_poli(nama_poli):
        """Menampilkan jadwal dokter berdasarkan poli."""
        data_poli = load_data("data/DokterPoli.json")
        
        if nama_poli not in data_poli:
            print(f"Poli {nama_poli} tidak ditemukan.")
            return
        
        print(f"Jadwal Dokter untuk Poli {nama_poli}:")
        for dokter_info in data_poli[nama_poli]:
            dokter = dokter_info["dokter"]
            hari = dokter_info["hari"]
            jam_awal = dokter_info["jam_awal"]
            jam_akhir = dokter_info["jam_akhir"]
            print(f"- {dokter}: {hari}, {jam_awal} - {jam_akhir}")
