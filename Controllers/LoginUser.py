import hashlib
import json
import os

class Register:
    def __init__(self, username, password):
        self.username = username
        self.password = self.hash_password(password)
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Membuat hash SHA-256 dari password"""
        return hashlib.sha256(password.encode()).hexdigest()

def register_user():
    """Fungsi untuk pendaftaran pengguna baru"""
    username = input("Masukkan username: ")
    password = input("Masukkan password: ")
    
    # Cek apakah username sudah ada
    if is_username_taken(username):
        print("Username sudah terdaftar!")
        return
    
    # Buat akun baru
    new_user = Register(username, password)
    
    # Simpan ke file JSON
    users = load_users()
    users.append({
        "username": new_user.username,
        "password": new_user.password
    })
    
    save_users(users)
    print("Registrasi berhasil!")

def login_user():
    """Fungsi untuk login pengguna"""
    username = input("Masukkan username: ")
    password = input("Masukkan password: ")
    
    users = load_users()
    for user in users:
        if user["username"] == username:
            # Verifikasi password
            hashed_input = Register.hash_password(password)
            if user["password"] == hashed_input:
                print("Login berhasil!")
                return
            else:
                print("Password salah!")
                return
    
    print("Username tidak ditemukan!")

def load_users():
    """Memuat data pengguna dari file JSON"""
    if not os.path.exists('users.json'):
        return []
    
    with open('users.json', 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_users(users):
    """Menyimpan data pengguna ke file JSON"""
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

def is_username_taken(username):
    """Memeriksa ketersediaan username"""
    users = load_users()
    return any(user["username"] == username for user in users)
