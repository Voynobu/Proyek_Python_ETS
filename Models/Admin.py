# Author      : Nauval Khairiyan
# NIM/Kelas   : 241524021 / 1A-D4
# Description : Class untuk admin (edit poli, dokter, jadwal, dll.) 

import json
from datetime import datetime
from utils.FileHandler import FileHandler

class Admin:
    """
    Class untuk menangani manajemen data poli dan dokter dalam sistem.
    """
    def __init__(self, username, password):
        self.username = username  # Username admin
        self.password = password  # Password admin

    @staticmethod
    def lihat_poli():
        """Menampilkan daftar poli dan datanya."""
        return FileHandler.load_data("data/poli.json")

    @staticmethod
    def tambah_poli(nama_poli, kuota_awal):
        """Menambahkan poli baru dengan kuota tertentu."""
        poli_data = FileHandler.load_data("data/poli.json")
        if nama_poli in poli_data:
            return "Poli sudah ada!"
        
        # Menambahkan poli baru dengan struktur default
        poli_data[nama_poli] = {
            "kuota": kuota_awal,
            "kuota_awal": kuota_awal,
            "dokter": {},
            "jadwal": {},
            "status_dokter": {}
        }
        FileHandler.save_data("data/poli.json", poli_data)
        return f"Poli {nama_poli} berhasil ditambahkan!"

    @staticmethod
    def edit_poli(nama_poli, kuota_awal):
        """Mengedit data poli yang sudah ada."""
        poli_data = FileHandler.load_data("data/poli.json")
        if nama_poli not in poli_data:
            return "Poli tidak ditemukan!"
        
        poli_data[nama_poli]["kuota_awal"] = kuota_awal
        poli_data[nama_poli]["kuota"] = kuota_awal
        FileHandler.save_data("data/poli.json", poli_data)
        return f"Data poli {nama_poli} berhasil diperbarui!"

    @staticmethod
    def hapus_poli(nama_poli):
        """Menghapus poli berdasarkan nama."""
        poli_data = FileHandler.load_data("data/poli.json")
        if nama_poli not in poli_data:
            return "Poli tidak ditemukan!"
        
        del poli_data[nama_poli]
        FileHandler.save_data("data/poli.json", poli_data)
        return f"Poli {nama_poli} berhasil dihapus!"

    @staticmethod
    def tambah_dokter(nama_poli, nama_dokter):
        """Menambahkan dokter ke poli tertentu."""
        poli_data = FileHandler.load_data("data/poli.json")
        if nama_poli not in poli_data:
            return "Poli tidak ditemukan!"
        
        poli_data[nama_poli]["dokter"][nama_dokter] = "available"
        FileHandler.save_data("data/poli.json", poli_data)
        return f"Dokter {nama_dokter} berhasil ditambahkan ke poli {nama_poli}!"

    @staticmethod
    def edit_dokter(nama_poli, nama_dokter, status):
        """Mengedit status dokter dalam poli tertentu."""
        poli_data = FileHandler.load_data("data/poli.json")
        if nama_poli not in poli_data or nama_dokter not in poli_data[nama_poli]["dokter"]:
            return "Dokter tidak ditemukan di poli ini!"
        
        poli_data[nama_poli]["dokter"][nama_dokter] = status
        FileHandler.save_data("data/poli.json", poli_data)
        return f"Status dokter {nama_dokter} di poli {nama_poli} berhasil diperbarui!"

    @staticmethod
    def hapus_dokter(nama_poli, nama_dokter):
        """Menghapus dokter dari poli tertentu."""
        poli_data = FileHandler.load_data("data/poli.json")
        if nama_poli not in poli_data or nama_dokter not in poli_data[nama_poli]["dokter"]:
            return "Dokter tidak ditemukan di poli ini!"
        
        del poli_data[nama_poli]["dokter"][nama_dokter]
        FileHandler.save_data("data/poli.json", poli_data)
        return f"Dokter {nama_dokter} berhasil dihapus dari poli {nama_poli}!"

    @staticmethod
    def tambah_jadwal(nama_poli, nama_dokter, hari, jam):
        """Menambahkan jadwal dokter dalam poli."""
        poli_data = FileHandler.load_data("data/poli.json")
        if nama_poli not in poli_data or nama_dokter not in poli_data[nama_poli]["dokter"]:
            return "Poli atau dokter tidak ditemukan!"
        
        poli_data[nama_poli]["jadwal"][nama_dokter] = {"hari": hari, "jam": jam}
        FileHandler.save_data("data/poli.json", poli_data)
        return f"Jadwal dokter {nama_dokter} berhasil ditambahkan di poli {nama_poli}!"

    @staticmethod
    def edit_jadwal(nama_poli, nama_dokter, hari, jam):
        """Mengedit jadwal dokter dalam poli."""
        poli_data = FileHandler.load_data("data/poli.json")
        if nama_poli not in poli_data or nama_dokter not in poli_data[nama_poli]["jadwal"]:
            return "Jadwal dokter tidak ditemukan!"
        
        poli_data[nama_poli]["jadwal"][nama_dokter] = {"hari": hari, "jam": jam}
        FileHandler.save_data("data/poli.json", poli_data)
        return f"Jadwal dokter {nama_dokter} di poli {nama_poli} berhasil diperbarui!"

    @staticmethod
    def hapus_jadwal(nama_poli, nama_dokter):
        """Menghapus jadwal dokter dalam poli."""
        poli_data = FileHandler.load_data("data/poli.json")
        if nama_poli not in poli_data or nama_dokter not in poli_data[nama_poli]["jadwal"]:
            return "Jadwal dokter tidak ditemukan!"
        
        del poli_data[nama_poli]["jadwal"][nama_dokter]
        FileHandler.save_data("data/poli.json", poli_data)
        return f"Jadwal dokter {nama_dokter} di poli {nama_poli} berhasil dihapus!"

    @staticmethod
    def kurangi_kuota(nama_poli):
        """Mengurangi kuota poli saat ada pasien yang mendaftar."""
        poli_data = FileHandler.load_data("data/poli.json")
        if nama_poli in poli_data and poli_data[nama_poli]["kuota"] > 0:
            poli_data[nama_poli]["kuota"] -= 1
            FileHandler.save_data("data/poli.json", poli_data)
            return f"Kuota poli {nama_poli} berkurang 1!"
        return "Kuota tidak tersedia atau poli tidak ditemukan!"

    @staticmethod
    def reset_kuota():
        """Mereset kuota semua poli ke kuota awal di setiap pergantian hari."""
        poli_data = FileHandler.load_data("data/poli.json")
        for poli in poli_data:
            poli_data[poli]["kuota"] = poli_data[poli]["kuota_awal"]
        FileHandler.save_data("data/poli.json", poli_data)
        return "Kuota poli telah direset untuk hari ini!"

    @staticmethod
    def update_status_dokter():
        """Memperbarui status dokter berdasarkan kuota poli."""
        poli_data = FileHandler.load_data("data/poli.json")
        for poli, data in poli_data.items():
            for dokter in data["dokter"]:
                data["status_dokter"][dokter] = "available" if data["kuota"] > 0 else "unavailable"
        FileHandler.save_data("data/poli.json", poli_data)
        return "Status dokter telah diperbarui!"

    @staticmethod
    def tambah_admin(username, password):
        """Menambahkan admin baru ke dalam sistem."""
        admin_data = FileHandler.load_data("data/admins.json")
        if username in admin_data:
            return "Admin sudah terdaftar!"
        
        admin_data[username] = password
        FileHandler.save_data("data/admins.json", admin_data)
        return f"Admin {username} berhasil ditambahkan!"

    @staticmethod
    def validasi_admin(username, password):
        """Memvalidasi login admin."""
        admin_data = FileHandler.load_data("data/admins.json")
        return admin_data.get(username) == password

