# Author      : Nauval Khairiyan
# NIM/Kelas   : 241524021 / 1A-D4
# Description : Class untuk admin (edit poli, dokter, biaya, dll.) 

import json
from file_handler import load_data, save_data

class Admin:
    def __init__(self, username, password):
        self.username = username
        self.password = password  # Dalam implementasi nyata, harus dienkripsi

    def tambah_poli(self, poli_name, dokter, jadwal, kuota):
        data = load_data("data/DokterPoli.json")
        if poli_name not in data:
            data[poli_name] = {"dokter": dokter, "jadwal": jadwal, "kuota": kuota}
            save_data("data/DokterPoli.json", data)
            return f"Poli {poli_name} dengan dokter {dokter} berhasil ditambahkan."
        return f"Poli {poli_name} sudah ada."

    def hapus_poli(self, poli_name):
        data = load_data("data/DokterPoli.json")
        if poli_name in data:
            del data[poli_name]
            save_data("data/DokterPoli.json", data)
            return f"Poli {poli_name} berhasil dihapus."
        return f"Poli {poli_name} tidak ditemukan."

    def edit_jadwal_poli(self, poli_name, jadwal_baru):
        data = load_data("data/DokterPoli.json")
        if poli_name in data:
            data[poli_name]["jadwal"] = jadwal_baru
            save_data("data/DokterPoli.json", data)
            return f"Jadwal poli {poli_name} berhasil diperbarui."
        return f"Poli {poli_name} tidak ditemukan."

    def update_kuota_poli(self, poli_name, kuota_baru):
        data = load_data("data/DokterPoli.json")
        if poli_name in data:
            data[poli_name]["kuota"] = kuota_baru
            save_data("data/DokterPoli.json", data)
            return f"Kuota poli {poli_name} berhasil diperbarui."
        return f"Poli {poli_name} tidak ditemukan."
