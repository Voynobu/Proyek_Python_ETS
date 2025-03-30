# Nama        : Ivan Setiawan Ihsan
# NIM/Kelas   : 241524012
# Kelas       : 1-A D4 Teknik Informatika
# Description : Class untuk pendaftaran pasien

import sys
import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent  # Naik satu level ke folder ETS
RIWAYAT_FILE = BASE_DIR / "Data" / "riwayat.json"
class Pasien:
    def __init__(self, nama, jenis_kelamin, tanggal_temu, jenis_layanan, poli, dokter, jadwal, keluhan, akun, nomor_antrian):
        self.nama = nama
        self.jenis_kelamin = jenis_kelamin
        self.tanggal_temu = tanggal_temu
        self.jenis_layanan = jenis_layanan  # BPJS, Asuransi, Mandiri
        self.poli = poli
        self.dokter = dokter
        self.jadwal = jadwal
        self.keluhan = keluhan  
        self.akun = akun
        self.nomor_antrian = nomor_antrian

    def get_info(self):
        return f"{self.nama},{self.jenis_layanan},{self.poli},{self.dokter},{self.jadwal}"
    
    
def simpan_data(nama, jenis_kelamin, tanggal_temu, jenis_layanan, poli, dokter, keluhan, jadwal, akun, nomor_antrian):
    new_pasien = Pasien(nama, jenis_kelamin, tanggal_temu, jenis_layanan, poli, dokter, jadwal, keluhan, akun, nomor_antrian)
    
    # Struktur data pasien yang akan disimpan
    data_pasien = {
        "nama": new_pasien.nama,
        "jenis_kelamin": new_pasien.jenis_kelamin,
        "jenis_layanan": new_pasien.jenis_layanan,
        "poli": new_pasien.poli,
        "dokter": new_pasien.dokter,
        "jadwal": new_pasien.jadwal,
        "tanggal_temu": new_pasien.tanggal_temu,
        "keluhan": new_pasien.keluhan,
        "nomor antrian" : nomor_antrian,
    }

    # Cek apakah file sudah ada
    if os.path.exists(RIWAYAT_FILE):
        with open(RIWAYAT_FILE, "r", encoding="utf-8") as file:
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
    with open(RIWAYAT_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
