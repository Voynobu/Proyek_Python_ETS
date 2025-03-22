#author    : Muhamad Dino Dermawan
#nim       : 241524015
#deskripsi : class nomor antrian

import os
import datetime

class NomorAntrian:
    def __init__(self):
        self.antrian = {"bpjs": {}, "mandiri": {}, "asuransi": {}}
        self.tanggal_terakhir = None
        self.nama_file = "antrianUnikWaktu.txt"  # Simpan di file baru
        self.load_antrian()

    def generate_nomor(self, jalur, poli):
        self.cek_reset_otomatis()  # Cek apakah perlu reset berdasarkan tanggal

        if poli not in self.antrian[jalur]:
            self.antrian[jalur][poli] = 1
        else:
            self.antrian[jalur][poli] += 1

        nomor_unik = f"{self.antrian[jalur][poli]}-{jalur}-{poli}"
        self.simpan_antrian()
        return nomor_unik

    def simpan_antrian(self):
        with open(self.nama_file, "w") as file:
            file.write(f"Tanggal:{datetime.date.today()}\n")  # Simpan tanggal saat ini
            for jalur, polis in self.antrian.items():
                for poli, nomor in polis.items():
                    file.write(f"{jalur},{poli},{nomor}\n")

    def load_antrian(self):
        if os.path.exists(self.nama_file):
            with open(self.nama_file, "r") as file:
                lines = file.readlines()
                if lines and lines[0].startswith("Tanggal:"):
                    self.tanggal_terakhir = lines[0].strip().split(":")[1]

                for line in lines[1:]:
                    parts = line.strip().split(",")
                    if len(parts) == 3:
                        jalur, poli, nomor = parts
                        self.antrian[jalur][poli] = int(nomor)

    def cek_reset_otomatis(self):
        tanggal_hari_ini = str(datetime.date.today())

        if self.tanggal_terakhir is None or self.tanggal_terakhir != tanggal_hari_ini:
            self.reset_antrian()
            self.tanggal_terakhir = tanggal_hari_ini

    def reset_antrian(self):
        self.antrian = {"bpjs": {}, "mandiri": {}, "asuransi": {}}
        self.simpan_antrian()  # Simpan agar tanggal terbaru tersimpan

if __name__ == "__main__":
    antrian = NomorAntrian()
    
    while True:
        try:
            print("\n1. Ambil Nomor Antrian")
            print("2. Keluar")
            
            pilihan = input("Pilih menu: ").strip()

            if pilihan == "1":
                print("\nSilakan pilih jalur:")
                print("1. BPJS")
                print("2. Mandiri")
                print("3. Asuransi")
                jalur_pilihan = input("Masukkan pilihan (1/2/3): ").strip()
                
                jalur_dict = {"1": "bpjs", "2": "mandiri", "3": "asuransi"}
                jalur = jalur_dict.get(jalur_pilihan)

                if not jalur:
                    print("Pilihan jalur tidak valid!")
                    continue

                print("\nSilakan pilih poli:")
                print("1. Mata")
                print("2. THT-KH")
                print("3. Saraf")
                print("4. Jantung")
                print("5. Anak")
                poli_pilihan = input("Masukkan pilihan (1/2/3): ").strip()
                
                poli_dict = {"1": "mata", "2": "tht-kh", "3": "saraf", "4": "jantung", "5": "anak"}
                poli = poli_dict.get(poli_pilihan)

                if not poli:
                    print("Pilihan poli tidak valid!")
                    continue

                nomor = antrian.generate_nomor(jalur, poli)
                
                jalur_alias = {"bpjs": "bpjs", "mandiri": "mdr", "asuransi": "as"}
                nomor = nomor.replace(jalur, jalur_alias[jalur])

                print(f"Nomor Antrian Anda: {nomor}")

            elif pilihan == "2":
                print("Keluar dari program.")
                break

            else:
                print("Pilihan tidak valid! Mohon masukkan angka 1-2.")

        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
