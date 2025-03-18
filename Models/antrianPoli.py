import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import datetime
import os

class NomorAntrian:
    def __init__(self):
        self.antrian = {"bpjs": {}, "mandiri": {}, "asuransi": {}}
        self.tanggal_terakhir = None
        self.nama_file = "antrianPoli.txt"  # Nama file diubah ke antrianPoli.txt
        self.load_antrian()

    def generate_nomor(self, jalur, poli):
        self.cek_reset_otomatis()  # Cek apakah perlu reset berdasarkan tanggal

        if poli not in self.antrian[jalur]:
            self.antrian[jalur][poli] = 1
        else:
            self.antrian[jalur][poli] += 1

        nomor_unik = f"{self.antrian[jalur][poli]}-{jalur}-{poli}"
        self.simpan_antrian(jalur, poli, nomor_unik)  # Simpan setiap nomor antrian
        return nomor_unik

    def simpan_antrian(self, jalur, poli, nomor_unik):
        with open(self.nama_file, "a") as file:  # Mode 'a' untuk append (tambahkan ke file)
            file.write(f"{datetime.date.today()},{jalur},{poli},{nomor_unik}\n")

    def load_antrian(self):
        if os.path.exists(self.nama_file):
            with open(self.nama_file, "r") as file:
                lines = file.readlines()
                if lines and lines[0].startswith("Tanggal:"):
                    self.tanggal_terakhir = lines[0].strip().split(":")[1]

                for line in lines[1:]:
                    parts = line.strip().split(",")
                    if len(parts) == 4:
                        tanggal, jalur, poli, nomor_unik = parts
                        nomor = int(nomor_unik.split("-")[0])  # Ambil nomor dari nomor_unik
                        if jalur not in self.antrian:
                            self.antrian[jalur] = {}
                        if poli not in self.antrian[jalur]:
                            self.antrian[jalur][poli] = nomor
                        else:
                            self.antrian[jalur][poli] = max(self.antrian[jalur][poli], nomor)

    def cek_reset_otomatis(self):
        tanggal_hari_ini = str(datetime.date.today())

        if self.tanggal_terakhir is None or self.tanggal_terakhir != tanggal_hari_ini:
            self.reset_antrian()
            self.tanggal_terakhir = tanggal_hari_ini

    def reset_antrian(self):
        self.antrian = {"bpjs": {}, "mandiri": {}, "asuransi": {}}
        # Tidak perlu menyimpan ulang file saat reset karena file sudah menyimpan semua data

class AntrianApp(QWidget):
    def __init__(self):
        super().__init__()
        self.antrian = NomorAntrian()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Sistem Antrian')
        self.resize(1000, 800)  # Perbesar ukuran window menjadi 1000x800 piksel

        # Posisikan window di tengah layar
        self.center()

        # Atur font yang lebih besar
        font = QFont()
        font.setPointSize(16)  # Ukuran font 16

        layout = QVBoxLayout()

        self.label_jalur = QLabel('Pilih Jalur:')
        self.label_jalur.setFont(font)  # Terapkan font ke label
        layout.addWidget(self.label_jalur)

        self.combo_jalur = QComboBox()
        self.combo_jalur.setFont(font)  # Terapkan font ke combo box
        self.combo_jalur.addItems(['BPJS', 'Mandiri', 'Asuransi'])
        layout.addWidget(self.combo_jalur)

        self.label_poli = QLabel('Pilih Poli:')
        self.label_poli.setFont(font)  # Terapkan font ke label
        layout.addWidget(self.label_poli)

        self.combo_poli = QComboBox()
        self.combo_poli.setFont(font)  # Terapkan font ke combo box
        self.combo_poli.addItems(['Mata', 'THT-KL', 'Saraf', 'Anak', 'Jantung'])
        layout.addWidget(self.combo_poli)

        self.btn_ambil = QPushButton('Ambil Nomor Antrian')
        self.btn_ambil.setFont(font)  # Terapkan font ke tombol
        self.btn_ambil.clicked.connect(self.ambil_nomor)
        layout.addWidget(self.btn_ambil)

        self.setLayout(layout)

    def center(self):
        # Dapatkan geometri layar
        screen_geometry = QApplication.desktop().screenGeometry()
        # Dapatkan geometri window
        window_geometry = self.frameGeometry()
        # Posisikan window di tengah layar
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

    def ambil_nomor(self):
        jalur_pilihan = self.combo_jalur.currentText().lower()
        poli_pilihan = self.combo_poli.currentText().lower()

        nomor = self.antrian.generate_nomor(jalur_pilihan, poli_pilihan)
        
        jalur_alias = {"bpjs": "bpjs", "mandiri": "mdr", "asuransi": "as"}
        nomor = nomor.replace(jalur_pilihan, jalur_alias[jalur_pilihan])

        # Buat QMessageBox dengan font yang lebih besar
        msg_box = QMessageBox()
        msg_box.setFont(QFont("Arial", 16))  # Atur font untuk QMessageBox
        msg_box.setWindowTitle('Nomor Antrian')
        msg_box.setText(f"Nomor Antrian Anda: {nomor}")
        msg_box.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AntrianApp()
    ex.show()
    sys.exit(app.exec_())
