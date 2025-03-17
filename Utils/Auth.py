# File Auth.py untuk autentikasi username dan password

import json
import os

# Path ke file JSON
USER_FILE = "Users.json"
ADMIN_FILE = "Admins.json"

def load_data(file_path):
    """Membaca data dari file JSON."""
    if not os.path.exists(file_path):
        return {}  # Jika file tidak ada, kembalikan dictionary kosong
    with open(file_path, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            print(f"⚠️ Error: File {file_path} rusak atau formatnya salah!")
            return {}  # Jika JSON rusak, kembalikan dictionary kosong

def check_login(username, password, role):
    """
    Memeriksa apakah username dan password valid.
    role: "user" untuk login user, "admin" untuk login admin.
    """
    file_path = USER_FILE if role == "user" else ADMIN_FILE
    data = load_data(file_path)

    if username in data and data[username] == password:
        return True  # Login berhasil
    return False  # Login gagal

def register_user(username, password, role):
    """
    Menambahkan user/admin baru ke file JSON.
    role: "user" untuk mendaftar user, "admin" untuk mendaftar admin.
    """
    file_path = USER_FILE if role == "user" else ADMIN_FILE
    data = load_data(file_path)

    if username in data:
        return False  # Username sudah terdaftar

    # Simpan data baru
    data[username] = password
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    
    return True  # Pendaftaran berhasil
