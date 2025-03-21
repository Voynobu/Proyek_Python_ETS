# Author      : Ivan Setiawan
# NIM/Kelas   : 241524012 / 1A-D4
# Description : Class untuk fitur login dan daftar akun

import hashlib
import json
import os
from pathlib import Path

# Mendapatkan path absolut ke file users.json
BASE_DIR = Path(__file__).parent.parent  # Naik satu level ke folder ETS
USERS_FILE = BASE_DIR / "Data" / "daftarUsers.json"

class Register:
    def __init__(self, username, password):
        self.username = username
        self.password = self.hash_password(password)
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Membuat hash SHA-256 dari password"""
        return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    """Fungsi untuk pendaftaran pengguna baru dengan return message."""
    if not is_valid_username(username):
        return "Username tidak boleh mengandung spasi!"
    
    elif not is_valid_password(password):
        return "Password harus minimal 8 karakter, mengandung setidaknya 1 huruf besar dan 1 simbol!"
    
    elif is_username_taken(username):
        return "Username sudah terdaftar!"
    
    else:
        new_user = Register(username, password)
        users = load_users()
        users.append({
        "username": new_user.username,
        "password": new_user.password
        })
        save_users(users)
        return "Registrasi berhasil!"

def login_user(username, password):
    """Fungsi untuk login pengguna"""

    users = load_users()
    for user in users:
        if user["username"] == username:
            # Verifikasi password
            hashed_input = Register.hash_password(password)
            if user["password"] == hashed_input:
                return "Login berhasil!"
            else:
                return "Password salah!"
    
    return("Username tidak ditemukan!")

def is_valid_password(password):
    """Cek apakah password memenuhi syarat minimal."""
    if len(password) < 8:
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char in "!@#$%^&*()-_=+[]{};:'\"|\\,.<>?/" for char in password):
        return False
    if " " in password:
        return False
    return True

def is_valid_username(username):
    """Cek apakah username tidak mengandung spasi."""
    return " " not in username

def load_users():
    """Memuat data pengguna dari file JSON"""
    if not USERS_FILE.exists():
        return []
    
    with USERS_FILE.open("r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_users(users):
    """Menyimpan data pengguna ke file JSON"""
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)  # Pastikan folder "Data" ada
    with USERS_FILE.open("w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)

def is_username_taken(username):
    """Memeriksa ketersediaan username"""
    users = load_users()
    return any(user["username"] == username for user in users)