# Author      : Nauval Khairiyan
# NIM/Kelas   : 241524021 / 1A-D4
# Description : Class untuk user (daftar poli, cek riwayat, dll.)  

class User:
    def __init__(self, nama, username, password):
        self.nama = nama
        self.username = username
        self.password = password  # Dalam implementasi nyata, harus dienkripsi

    def daftar_poli(self, pasien):
        from Utils.FileHandler import append_to_file
        file_map = {
            "BPJS": "data/bpjs.txt",
            "Asuransi": "data/asuransi.txt",
            "Mandiri": "data/mandiri.txt"
        }
        file_path = file_map.get(pasien.jenis_pendaftaran)
        if file_path:
            append_to_file(file_path, pasien.get_info())
            return "Pendaftaran berhasil!"
        return "Jenis pendaftaran tidak valid."
    
    def cek_status_pendaftaran(self, nik):
        from Utils.FileHandler import search_in_file
        for category in ["bpjs", "asuransi", "mandiri"]:
            results = search_in_file(f"data/{category}.txt", nik)
            if results:
                return f"Status Pendaftaran: {results}"
        return "Data tidak ditemukan."