# Author      : Nauval Khairiyan
# NIM/Kelas   : 241524021 / 1A-D4
# Description : Validasi input data
import re
import json
import os

def validate_nik(nik):
    """Validasi NIK (Nomor Induk Kependudukan) harus 16 digit angka."""
    return bool(re.fullmatch(r"\d{16}", nik))

def validate_name(name):
    """Validasi nama hanya boleh berisi huruf dan spasi, minimal 3 karakter."""
    return bool(re.fullmatch(r"[A-Za-z\s]{3,}", name))

def validate_date(date):
    """Validasi format tanggal (YYYY-MM-DD)."""
    return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", date))

def validate_poli_choice(poli_name, file_path="DokterPoli.json"):
    """Memastikan bahwa pilihan poli tersedia dalam data DokterPoli.json."""
    if not os.path.exists(file_path):
        return False

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return poli_name in data  # Memastikan nama poli ada dalam JSON

def validate_doctor_choice(poli_name, doctor_name, file_path="DokterPoli.json"):
    """Memastikan dokter tersedia untuk poli yang dipilih."""
    if not os.path.exists(file_path):
        return False

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if poli_name in data:
        return doctor_name in data[poli_name]["dokter"]

    return False

def validate_kuota(poli_name, file_path="DokterPoli.json"):
    """Memeriksa apakah kuota masih tersedia untuk poli yang dipilih."""
    if not os.path.exists(file_path):
        return False

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if poli_name in data:
        return data[poli_name]["kuota"] > 0  # Kuota harus lebih dari 0

    return False

def validate_username(username):
    """Validasi username (huruf dan angka, minimal 5 karakter)."""
    return bool(re.fullmatch(r"[A-Za-z0-9_]{5,}", username))

def validate_password(password):
    """Validasi password (minimal 6 karakter, harus ada huruf dan angka)."""
    return bool(re.fullmatch(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$", password))
