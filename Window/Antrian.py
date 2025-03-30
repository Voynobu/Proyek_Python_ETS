import sys
import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
ANTRIAN_FILE = BASE_DIR / "Data" / "antrian.json"

LAYANAN_MAP = {"BPJS": "BPJS", "Mandiri": "MNDR", "Asuransi": "ASRI"}

def load_antrian_data():
    """Memuat data antrian dari file JSON atau mengembalikan dictionary kosong jika file tidak ditemukan atau kosong."""
    if Path(ANTRIAN_FILE).exists():
        with open(ANTRIAN_FILE, "r", encoding="utf-8") as file:
            content = file.read().strip()  # Membaca isi file dan menghapus spasi kosong
            if not content:  # Jika file kosong, kembalikan dictionary kosong
                return {}
            return json.loads(content)  # Parse JSON jika ada isi
    return {}  # Jika file tidak ditemukan, kembalikan dictionary kosong


def save_antrian_data(antrian_data):
    """Menyimpan data antrian ke file JSON."""
    with open(ANTRIAN_FILE, "w", encoding="utf-8") as file:
        json.dump(antrian_data, file, indent=4)

def ambil_nomor_antrian(tanggal_temu, tipe_layanan, poli):
    """
    Menghasilkan nomor antrian berdasarkan tanggal temu, layanan, dan poli yang dipilih.

    tanggal_temu: str (format "dd-mm-yyyy")
    tipe_layanan: str (BPJS, Mandiri, Asuransi)
    poli: str (nama poli, misal "Mata", "Jantung")

    Return: Nomor antrian (contoh: "BPJS-Mata-1")
    """
    antrian_data = load_antrian_data()

    # Jika tanggal belum ada, buat entry baru
    if tanggal_temu not in antrian_data:
        antrian_data[tanggal_temu] = {}

    # Jika layanan belum ada dalam tanggal tersebut, buat entry baru
    if tipe_layanan not in antrian_data[tanggal_temu]:
        antrian_data[tanggal_temu][tipe_layanan] = {}

    # Jika poli belum ada dalam layanan tersebut, mulai antrian dari 1
    if poli not in antrian_data[tanggal_temu][tipe_layanan]:
        antrian_data[tanggal_temu][tipe_layanan][poli] = 1
    else:
        # Jika sudah ada, tambahkan 1 ke nomor antrian terakhir
        antrian_data[tanggal_temu][tipe_layanan][poli] += 1

    # Ambil nomor antrian baru
    nomor_urut = antrian_data[tanggal_temu][tipe_layanan][poli]
    nomor_antrian = f"{LAYANAN_MAP.get(tipe_layanan, 'UNK')}-{poli}-{nomor_urut}"

    # Simpan perubahan ke file JSON
    save_antrian_data(antrian_data)

    return nomor_antrian

def is_antrian_penuh(tanggal_temu, tipe_layanan, poli):
    """
    Mengecek apakah antrian untuk poli pada hari tersebut sudah mencapai 5.

    tanggal_temu: str (format "dd-mm-yyyy")
    tipe_layanan: str (BPJS, Mandiri, Asuransi)
    poli: str (nama poli, misal "Mata", "Jantung")

    Return: True jika antrian sudah mencapai 5, False jika masih bisa menerima pasien.
    """
    antrian_data = load_antrian_data()

    # Cek apakah tanggal temu, layanan, dan poli ada dalam data
    if (
        tanggal_temu in antrian_data and
        tipe_layanan in antrian_data[tanggal_temu] and
        poli in antrian_data[tanggal_temu][tipe_layanan]
    ):
        return antrian_data[tanggal_temu][tipe_layanan][poli] >= 5
    
    return False  # Jika belum ada antrian, berarti belum penuh

# Contoh Penggunaan
if __name__ == "__main__":
    tanggal = "30-03-2025"
    layanan = "BPJS"
    poli = "Mata"

    nomor_antrian = ambil_nomor_antrian(tanggal, layanan, poli)
    print(f"Nomor Antrian: {nomor_antrian}")  # Contoh output: BPJS-Mata-1

    penuh = is_antrian_penuh(tanggal, layanan, poli)
    print(f"Antrian penuh? {penuh}")  # False jika belum mencapai 5
