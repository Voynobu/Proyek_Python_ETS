#Nama: Zaidan Zulkaisi Setiaji
#Kelas: 1A - D4
#NIM: 241524031
#Desc: - Pasien dapat mengetahui jadwal yang tersedia.
#      - Dapat mengupdate jadwal menyesuaikan kebutuhan.
#      - Pasien dapat memilih Poli dan Dokter yang diinginkan.

from datetime import datetime, time

class Dokter:
    def __init__(self, nama, spesialis):
        self.nama = nama
        self.spesialis = spesialis
    
    def __str__(self):
        return f"{self.nama}({self.spesialis})"

class Jadwal:
    def __init__(self, dokter, hari, jam_awal, jam_akhir):
        self.dokter = dokter
        self.hari = hari
        self.jam_awal = jam_awal
        self.jam_akhir = jam_akhir

    def StatusDokter(self):
        saatini = datetime.now()
        Hari_saatini = saatini.strftime("%A")
        Waktu_saatini = saatini.time()

        jam_awal = datetime.strptime(self.jam_awal, "%H:%M").time()
        jam_akhir = datetime.strptime(self.jam_akhir, "%H:%M").time()

        if Hari_saatini == self.hari and jam_awal <= Waktu_saatini <= jam_akhir:
            return "Available"
        else:
            return "Unavailable"

    def __str__(self):
        status = self.StatusDokter()
        return f"{self.dokter} -- {self.hari} ({self.jam_awal} - {self.jam_akhir}). Status : {status}"
    
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

class JadwalPoli():
    def __init__(self, nama):
        self.nama = nama
        self.daftar_poli = []

    def TambahPoli(self, poli):
        self.daftar_poli.append(poli)

    def TampilPoli(self):
        print (f"Daftar Poli :")
        for idx, poli in enumerate (self.daftar_poli, start=1):
            print(f"{idx}. {poli}")
        
    def PilihanPoli(self, pilihan):
        if 1 <= pilihan <= len(self.daftar_poli):
            return self.daftar_poli[pilihan - 1]
        else:
            return None
        







              
if __name__ == "__main__":
    dokter1 = Dokter("Dr. Asep", "Kardiolog")
    dokter2 = Dokter("Dr. Ahmad", "Oftalmolog")
    dokter3 = Dokter("Dr. Messi", "Spesialis THT-KH")
    dokter4 = Dokter("Dr. Jajang", "Neurolog")

    poli_jantung = Poli("Poli Jantung")
    poli_jantung.TambahDokter(dokter1)
    poli_jantung.TambahJadwal(Jadwal(dokter1,"Tuesday", "08:00", "12:00"))
    poli_jantung.TambahJadwal(Jadwal(dokter1, "Friday", "13:00", "18:00"))

    poli_mata = Poli("Poli Mata")
    poli_mata.TambahDokter(dokter2)
    poli_mata.TambahJadwal(Jadwal(dokter2, "Monday", "09:00", "15:00"))
    poli_mata.TambahJadwal(Jadwal(dokter2, "Thursday", "07:00", "12:00"))

    poli_THT_KL = Poli("Poli THT-KL")
    poli_THT_KL.TambahDokter(dokter3)
    poli_THT_KL.TambahJadwal(Jadwal(dokter3, "Tuesday", "11:00", "18:00"))
    poli_THT_KL.TambahJadwal(Jadwal(dokter3, "Wednesday", "18:00", "21:00"))

    poli_saraf = Poli("Poli Saraf")
    poli_saraf.TambahDokter(dokter4)
    poli_saraf.TambahJadwal(Jadwal(dokter4, "Tuesday", "08:00", "13:00"))
    poli_saraf.TambahJadwal(Jadwal(dokter4, "Sunday", "10:00", "17:00"))

    Jd_poli = JadwalPoli("Jadwal Poli")
    
    Jd_poli.TambahPoli(poli_jantung)
    Jd_poli.TambahPoli(poli_mata)
    Jd_poli.TambahPoli(poli_THT_KL)
    Jd_poli.TambahPoli(poli_saraf)

    Jd_poli.TampilPoli()

    pilihan_poli = int(input("Pilih Poli (nomor): "))
    Poli_terpilih = Jd_poli.PilihanPoli(pilihan_poli)

    if Poli_terpilih:
        while True:
            print("\nMenu")
            print("1. Tampilkan Jadwal")
            print("2. Tambah Jadwal")
            print("3. Ubah Jadwal")
            print("4. Keluar")
            pilihan_menu = int(input("Pilih Opsi (nomor): "))

            if pilihan_menu == 1:
                Poli_terpilih.TampilJadwal()
            elif pilihan_menu == 2:
                Poli_terpilih.TambahJadwalBaru()
            elif pilihan_menu == 3:
                Poli_terpilih.UpdateJadwal()
            elif pilihan_menu == 4:
                break
            else:
                print("Pilihan menu tidak valid")
    else:
        print("Pilihan Poli tidak valid")


