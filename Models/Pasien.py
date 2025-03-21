# Nama        : Ivan Setiawan Ihsan
# NIM/Kelas   : 241524012
# Kelas       : 1-A D4 Teknik Informatika
# Description : Class untuk pendaftaran pasien

import json
import os

class Pasien:
    def __init__(self, nama, jenis_kelamin, tanggal_lahir,  jenis_layanan, poli, dokter, tanggal_temu, keluhan, nomor_antrian, akun):
        self.nama = nama
        self.jenis_kelamin = jenis_kelamin
        self.tanggal_lahir = tanggal_lahir
        self.jenis_layanan = jenis_layanan  # BPJS, Asuransi, Mandiri
        self.poli = poli
        self.dokter = dokter
        self.tanggal_temu = tanggal_temu
        self.keluhan = keluhan  
        self.akun = akun
        self.nomor_antrian = nomor_antrian

    def get_info(self):
        return f"{self.nama},{self.nik},{self.jenis_layanan},{self.poli},{self.dokter},{self.tanggal_temu}"
    
    
def simpan_data(nama, jenis_kelamin, tanggal_lahir, bulan_lahir, jenis_layanan, poli, dokter, keluhan, tanggal_temu, nomor_antrian, akun):
    new_pasien = Pasien(nama, jenis_kelamin, tanggal_lahir, bulan_lahir, jenis_layanan, poli, dokter, keluhan, tanggal_temu, nomor_antrian, akun)

    # Nama file tempat menyimpan data
    filename = "riwayat.json"

    # Struktur data pasien yang akan disimpan
    data_pasien = {
        "nama": new_pasien.nama,
        "jenis_kelamin": new_pasien.jenis_kelamin,
        "tanggal_lahir": new_pasien.tanggal_lahir,
        "jenis_layanan": new_pasien.jenis_layanan,
        "poli": new_pasien.poli,
        "dokter": new_pasien.dokter,
        "tanggal_temu": new_pasien.tanggal_temu,
        "keluhan": new_pasien.keluhan,
        "nomor_antrian": new_pasien.nomor_antrian
    }

    # Cek apakah file sudah ada
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    # Simpan data berdasarkan akun pasien (histori per akun)
    if akun not in data:
        data[akun] = []

    data[akun].append(data_pasien)

    # Simpan kembali ke file JSON
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
