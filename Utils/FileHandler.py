# Author      : Nauval Khairiyan
# NIM/Kelas   : 241524021 / 1A-D4
# Description : Fungsi baca/tulis file

import os

def read_file(file_path):
    """Membaca isi file dan mengembalikan dalam bentuk list baris."""
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines()]

def write_file(file_path, data, mode="w"):
    """Menulis atau menambahkan data ke file."""
    with open(file_path, mode, encoding="utf-8") as file:
        if isinstance(data, list):
            file.write("\n".join(data) + "\n")
        else:
            file.write(str(data) + "\n")

def append_to_file(file_path, data):
    """Menambahkan data ke file tanpa menghapus isi sebelumnya."""
    write_file(file_path, data, mode="a")


def search_in_file(file_path, keyword):
    """Mencari data dalam file berdasarkan keyword."""
    lines = read_file(file_path)
    return [line for line in lines if keyword in line]
