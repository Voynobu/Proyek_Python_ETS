# Author      : Nauval Khairiyan
# NIM/Kelas   : 241524021 / 1A-D4
# Description : Class untuk user (daftar poli, cek riwayat, dll.)  

from Utils.file_handler import load_data, save_data

class User:
    def __init__(self, nama, username, password):
        self.nama = nama
        self.username = username
        self.password = password  # Dalam implementasi nyata, harus dienkripsi

    def daftar_poli(self, pasien):
        """Mendaftarkan pasien ke poli berdasarkan jenis pendaftaran."""
        file_map = {
            "BPJS": "data/BPJS.json",
            "Asuransi": "data/Asuransi.json",
            "Mandiri": "data/Mandiri.json"
        }
        file_path = file_map.get(pasien.jenis_pendaftaran)
        
        if file_path:
            data = load_data(file_path)
            data.append(pasien.to_dict())  # Gunakan metode to_dict() pada pasien untuk menyimpan data JSON
            save_data(file_path, data)
            return "Pendaftaran berhasil!"
        
        return "Jenis pendaftaran tidak valid."
    
    def cek_status_pendaftaran(self, nik):
        """Mengecek status pendaftaran pasien berdasarkan NIK."""
        for category in ["BPJS", "Asuransi", "Mandiri"]:
            file_path = f"data/{category}.json"
            data = load_data(file_path)
            for entry in data:
                if entry.get("nik") == nik:
                    return f"Status Pendaftaran: {entry}"
        
        return "Data tidak ditemukan."
