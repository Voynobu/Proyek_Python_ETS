# Nama : Muhamad Dino Dermawan
# Nim  : 241524015
# Desc : generate nomor antrian seusai jalur pendaftaran dan poli, dan akan kembali ke reset antrian jika ganti hari
#        menyesuaikan poli sesuai dengan yang ada di JadwalPoli.json

import sys
import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
ANTRIAN_FILE = BASE_DIR / "Data" / "antrian.json"
POLIKLINIK_FILE = BASE_DIR / "Data" / "jadwalPoli.json"

LAYANAN_MAP = {"BPJS": "BPJS", "Mandiri": "MNDR", "Asuransi": "ASRI"}

def load_antrian_data():
    """Memuat data antrian dari file JSON atau mengembalikan dictionary kosong jika file tidak ditemukan atau kosong."""
    if Path(ANTRIAN_FILE).exists():
        with open(ANTRIAN_FILE, "r", encoding="utf-8") as file:
            content = file.read().strip()
            if not content:
                return {}
            return json.loads(content)
    return {}

def save_antrian_data(antrian_data):
    """Menyimpan data antrian ke file JSON."""
    with open(ANTRIAN_FILE, "w", encoding="utf-8") as file:
        json.dump(antrian_data, file, indent=4)

def get_poli_list():
    """Mengambil daftar poli terbaru dari JadwalPoli.json."""
    with open(POLIKLINIK_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)
        return [poli["nama_poli"] for poli in data["daftar_poli"]]

def clean_antrian_data(antrian_data):
    """Menghapus data antrian untuk poli yang sudah tidak ada di JadwalPoli.json."""
    poli_list = get_poli_list()
    cleaned_data = {}
    for tanggal, layanan_data in antrian_data.items():
        cleaned_layanan_data = {}
        for layanan, poli_data in layanan_data.items():
            cleaned_poli_data = {
                poli: nomor for poli, nomor in poli_data.items() if poli in poli_list
            }
            if cleaned_poli_data:
                cleaned_layanan_data[layanan] = cleaned_poli_data
        if cleaned_layanan_data:
            cleaned_data[tanggal] = cleaned_layanan_data
    return cleaned_data

def ambil_nomor_antrian(tanggal_temu, tipe_layanan, poli):
    """
    Menghasilkan nomor antrian berdasarkan tanggal temu, layanan, dan poli yang dipilih.
    """
    # Validasi poli
    if poli not in get_poli_list():
        raise ValueError(f"Poli '{poli}' tidak ditemukan dalam daftar poli.")
    
    antrian_data = load_antrian_data()
    antrian_data = clean_antrian_data(antrian_data)  # Bersihkan data sebelum diproses

    if tanggal_temu not in antrian_data:
        antrian_data[tanggal_temu] = {}

    if tipe_layanan not in antrian_data[tanggal_temu]:
        antrian_data[tanggal_temu][tipe_layanan] = {}

    if poli not in antrian_data[tanggal_temu][tipe_layanan]:
        antrian_data[tanggal_temu][tipe_layanan][poli] = 1
    else:
        antrian_data[tanggal_temu][tipe_layanan][poli] += 1

    nomor_urut = antrian_data[tanggal_temu][tipe_layanan][poli]
    nomor_antrian = f"{LAYANAN_MAP.get(tipe_layanan, 'UNK')}-{poli}-{nomor_urut}"

    save_antrian_data(antrian_data)
    return nomor_antrian

def is_antrian_penuh(tanggal_temu, tipe_layanan, poli):
    """
    Mengecek apakah antrian untuk poli pada hari tersebut sudah mencapai 5.
    """
    # Validasi poli
    if poli not in get_poli_list():
        return True  # Anggap penuh jika poli tidak valid
    
    antrian_data = load_antrian_data()
    antrian_data = clean_antrian_data(antrian_data)  # Bersihkan data sebelum diproses

    if (
        tanggal_temu in antrian_data and
        tipe_layanan in antrian_data[tanggal_temu] and
        poli in antrian_data[tanggal_temu][tipe_layanan]
    ):
        return antrian_data[tanggal_temu][tipe_layanan][poli] >= 5
    
    return False

if __name__ == "__main__":
    tanggal = "30-03-2025"
    layanan = "BPJS"
    poli = "Mata"

    nomor_antrian = ambil_nomor_antrian(tanggal, layanan, poli)
    print(f"Nomor Antrian: {nomor_antrian}")

    penuh = is_antrian_penuh(tanggal, layanan, poli)
    print(f"Antrian penuh? {penuh}")
