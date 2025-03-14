# Author      : Nauval Khairiyan
# NIM/Kelas   : 241524021 / 1A-D4
# Description : Class untuk menyimpan data pasien 


class Pasien:
    def __init__(self, nama, nik, jenis_pendaftaran, poli, dokter, tanggal_temu, pembayaran=None):
        self.nama = nama
        self.nik = nik
        self.jenis_pendaftaran = jenis_pendaftaran  # BPJS, Asuransi, Mandiri
        self.poli = poli
        self.dokter = dokter
        self.tanggal_temu = tanggal_temu
        self.pembayaran = pembayaran  # Hanya untuk Asuransi dan Mandiri

    def get_info(self):
        return f"{self.nama},{self.nik},{self.jenis_pendaftaran},{self.poli},{self.dokter},{self.tanggal_temu},{self.pembayaran or '-'}"
