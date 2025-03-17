#Author : Zaidan Zulkaisi Setiaji
#NIM/Kelas : 241524031/1A-D4
#Deskripsi : class untuk Poli

from Jadwal import Jadwal

class Poli:
    def __init__(self, nama_poli):
        self.nama_poli = nama_poli
        self.dokter_list = []
        self.jadwal_list = []
        
    def __str__(self):
        return self.nama_poli
        
    def TambahDokter(self, dokter):
        self.dokter_list.append(dokter)

    def TambahJadwal(self, jadwal):
        self.jadwal_list.append(jadwal)

    def TampilDaftar(self):
        print (f"Daftar Dokter ({self.nama_poli}) :")
        for idx, dokter in enumerate (self.dokter_list, start=1):
            print(f"{idx}. {dokter}")

    def TampilJadwal(self):
        print (f"Daftar Jadwal ({self.nama_poli}) :")
        for idx, jadwal in enumerate (self.jadwal_list, start=1):
            print(f"{idx}. {jadwal}")    

    def PilihanDokter(self, pilihan):
        if 1 <= pilihan <= len(self.dokter_list):
            return self.dokter_list[pilihan - 1]
        else:
            None

    def PilihanJadwal(self, pilihan):
        if 1 <= pilihan <= len(self.jadwal_list):
            return self.jadwal_list[pilihan - 1]
        else:
            None

    def TambahJadwalBaru(poli):
        poli.TampilDaftar()
        pilihan_dokter = int(input("Pilih dokter (nomor): "))
        Dokter_terpilih = poli.PilihanDokter(pilihan_dokter)

        if Dokter_terpilih:
            hari = input("Masukkan Jadwal baru[Hari], Contoh(Monday):")
            jam_awal = input("Masukkan Jadwal baru[Jam Awal], Format(HH:MM): ")
            jam_akhir = input("Masukkan Jadwal baru[Jam Akhir], Format(HH:MM): ")

            jadwal_baru = Jadwal(Dokter_terpilih, hari, jam_awal, jam_akhir)
            poli.TambahJadwal(jadwal_baru)
            print("Jadwal berhasil ditambahkan.")
        else:
            print("Pilihan Dokter Invalid.")


    def UpdateJadwal(poli):
        poli.TampilJadwal()
        pilihan_jadwal = int(input("Pilih Jadwal yang ingin diubah(nomor): "))
        Jadwal_terpilih = poli.PilihanJadwal(pilihan_jadwal)

        if Jadwal_terpilih:
            print(f"Jadwal yang dipilih: {Jadwal_terpilih}")
            hari_baru = input("Masukkan Jadwal baru[Hari], Contoh(Monday):")
            jam_awal_baru = input("Masukkan Jadwal baru[Jam Awal], Format(HH:MM): ")
            jam_akhir_baru = input("Masukkan Jadwal baru[Jam Akhir], Format(HH:MM): ")

            Jadwal_terpilih.hari = hari_baru
            Jadwal_terpilih.jam_awal = jam_awal_baru
            Jadwal_terpilih.jam_akhir = jam_akhir_baru
            print("Jadwal berhasil diubah!")
        else:
            print("Pilihan jadwal tidak valid.")
