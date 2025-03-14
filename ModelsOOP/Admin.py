# Author      : Nauval Khairiyan
# NIM/Kelas   : 241524021 / 1A-D4
# Description : Class untuk admin (edit poli, dokter, biaya, dll.) 

class Admin:
    def __init__(self, username, password):
        self.username = username
        self.password = password  # Dalam implementasi nyata, harus dienkripsi

    def tambah_poli(self, poli_name, dokter, biaya):
        from Utils.FileHandler import append_to_file
        append_to_file("data/poli.txt", f"{poli_name},{dokter},{biaya}")
        return f"Poli {poli_name} dengan dokter {dokter} berhasil ditambahkan."

    def hapus_poli(self, poli_name):
        from Utils.FileHandler import read_file, write_file
        lines = read_file("data/poli.txt")
        new_lines = [line for line in lines if not line.startswith(poli_name)]
        write_file("data/poli.txt", new_lines)
        return f"Poli {poli_name} berhasil dihapus."