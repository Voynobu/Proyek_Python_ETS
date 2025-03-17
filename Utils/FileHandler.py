# Author      : Nauval Khairiyan
# NIM/Kelas   : 241524021 / 1A-D4
# Description : Fungsi baca/tulis file

import json
import os

# Path ke file JSON
FILES = {
    "bpjs": "BPJS.json",
    "mandiri": "Mandiri.json",
    "asuransi": "Asuransi.json",
    "admins": "Admins.json",
    "users": "Users.json",
    "dokter_poli": "DokterPoli.json"
}

def load_data(file_key):
    """Membaca data dari file JSON berdasarkan key yang ada di FILES."""
    file_path = FILES.get(file_key)
    if not file_path:
        raise ValueError("Invalid file key!")

    if not os.path.exists(file_path):
        return {}  # Jika file tidak ditemukan, kembalikan dictionary kosong
    
    with open(file_path, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {}  # Jika format JSON rusak, kembalikan dictionary kosong

def save_data(file_key, data):
    """Menyimpan data ke file JSON berdasarkan key yang ada di FILES."""
    file_path = FILES.get(file_key)
    if not file_path:
        raise ValueError("Invalid file key!")

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def add_patient(file_key, patient_data):
    """Menambahkan data pasien ke file JSON yang sesuai (BPJS, Mandiri, atau Asuransi)."""
    if file_key not in ["bpjs", "mandiri", "asuransi"]:
        raise ValueError("File key harus 'bpjs', 'mandiri', atau 'asuransi'!")

    data = load_data(file_key)
    patient_id = str(len(data) + 1)  # ID pasien berdasarkan jumlah data saat ini

    data[patient_id] = patient_data  # Simpan data pasien
    save_data(file_key, data)

    return patient_id  # Kembalikan ID pasien untuk referensi

def update_data(file_key, record_id, updated_data):
    """Mengupdate data pada file JSON berdasarkan record_id."""
    data = load_data(file_key)

    if record_id not in data:
        return False  # Data tidak ditemukan

    data[record_id] = updated_data
    save_data(file_key, data)
    return True  # Berhasil diupdate

def delete_data(file_key, record_id):
    """Menghapus data dari file JSON berdasarkan record_id."""
    data = load_data(file_key)

    if record_id not in data:
        return False  # Data tidak ditemukan

    del data[record_id]
    save_data(file_key, data)
    return True  # Berhasil dihapus

def check_quota(poli_name, date):
    """Memeriksa apakah kuota pendaftaran untuk poli pada tanggal tertentu masih tersedia."""
    data = load_data("dokter_poli")

    if poli_name not in data:
        return False, 0  # Poli tidak ditemukan

    poli_info = data[poli_name]
    quota_harian = poli_info.get("kuota_harian", 0)

    # Cek jumlah pasien terdaftar pada tanggal tersebut
    registered_patients = poli_info.get("jadwal", {}).get(date, 0)

    return registered_patients < quota_harian, quota_harian - registered_patients
