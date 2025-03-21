import sys
import json
import os
from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QCalendarWidget, QMessageBox
from pasien import simpan_data
from daftarUser import Register, load_users

BASE_DIR = Path(__file__).parent.parent  # Naik satu level ke folder ETS
USERS_FILE = BASE_DIR / "Data" / "poliklinik_data.json"

class Ui_Dialog(object):
    def setupUi(self, Dialog, username):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1600, 900)
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.label_background = QtWidgets.QLabel(Dialog)
        self.label_background.setGeometry(QtCore.QRect(0, 0, 1600, 900))
        self.label_background.setPixmap(QtGui.QPixmap("C:/Users/ivan setiawan ihsan/Downloads/TESTING/BACKGROUND.png"))
        self.label_background.setScaledContents(True)
        self.label_background.setObjectName("label_background")

        # Membuat input transparan
        self.keluhan = QtWidgets.QLineEdit(Dialog)
        self.keluhan.setGeometry(QtCore.QRect(636, 515, 377, 184))
        self.keluhan.setStyleSheet("background: transparent; border: none;")
        self.keluhan.setObjectName("keluhan")
        self.keluhan.setPlaceholderText("Masukkan Keluhan")

        self.Nama = QtWidgets.QLineEdit(Dialog)
        self.Nama.setGeometry(QtCore.QRect(92, 261, 514, 58))
        self.Nama.setStyleSheet("background: transparent; border: none;")
        self.Nama.setObjectName("Nama")
        self.Nama.setPlaceholderText("Masukkan nama lengkap")

        self.poli = QtWidgets.QComboBox(Dialog)
        self.poli.setGeometry(QtCore.QRect(91, 514, 516, 58))
        self.poli.setStyleSheet("background: transparent; border: none;")
        self.poli.setObjectName("poli")

        self.dokter = QtWidgets.QComboBox(Dialog)
        self.dokter.setGeometry(QtCore.QRect(91, 641, 514, 58))
        self.dokter.setStyleSheet("background: transparent; border: none;")
        self.dokter.setObjectName("dokter")
        self.dokter.setPlaceholderText("Pilih dokter")

        self.pilih_jadwal = QtWidgets.QComboBox(Dialog)
        self.pilih_jadwal.setGeometry(QtCore.QRect(93, 768, 514, 58))
        self.pilih_jadwal.setStyleSheet("background: transparent; border: none;")
        self.pilih_jadwal.setObjectName("pilih_jadwal")
        self.pilih_jadwal.setPlaceholderText("Pilih jadwal")

        self.tanggal_lahir = QtWidgets.QComboBox(Dialog)
        self.tanggal_lahir.setGeometry(QtCore.QRect(636, 388, 376, 58))
        self.tanggal_lahir.setStyleSheet("background: transparent; border: none;")
        self.tanggal_lahir.setObjectName("tanggal_lahir")
        self.tanggal_lahir.setPlaceholderText("Masukkan tanggal lahir")

        self.pria = QtWidgets.QRadioButton(Dialog)
        self.pria.setGeometry(QtCore.QRect(660, 279, 95, 20))
        self.pria.setStyleSheet("background: transparent; border: none;")
        self.pria.setObjectName("pria")

        self.wanita = QtWidgets.QRadioButton(Dialog)
        self.wanita.setGeometry(QtCore.QRect(831, 279, 95, 20))
        self.wanita.setStyleSheet("background: transparent; border: none;")
        self.wanita.setObjectName("wanita")

        self.jenis_layanan = QtWidgets.QComboBox(Dialog)
        self.jenis_layanan.setGeometry(QtCore.QRect(91, 387, 516, 58))
        self.jenis_layanan.setStyleSheet("background: transparent; border: none;")
        self.jenis_layanan.setObjectName("jenis_layanan")

        # Tombol Back dengan transparansi
        self.label_back = QtWidgets.QLabel(Dialog)
        self.label_back.setGeometry(QtCore.QRect(10, 20, 134, 103))
        self.label_back.setPixmap(QtGui.QPixmap("C:/Users/ivan setiawan ihsan/Downloads/TESTING/BACK.png"))
        self.label_back.setObjectName("label_back")

        self.back = QtWidgets.QPushButton(Dialog)
        self.back.setGeometry(QtCore.QRect(11, 22, 134, 103))
        self.back.setStyleSheet("background: transparent; border: none;")
        self.back.setObjectName("back")

        # Tombol Daftar dengan transparansi
        self.label_daftar = QtWidgets.QLabel(Dialog)
        self.label_daftar.setGeometry(QtCore.QRect(680, 740, 291, 91))
        self.label_daftar.setPixmap(QtGui.QPixmap("C:/Users/ivan setiawan ihsan/Downloads/TESTING/DAFTAR.png"))
        self.label_daftar.setObjectName("label_daftar")

        self.daftar = QtWidgets.QPushButton(Dialog)
        self.daftar.setGeometry(QtCore.QRect(686, 741, 282, 88))
        self.daftar.setStyleSheet("background: transparent; border: none;")
        self.daftar.setObjectName("daftar")

        self.username = username

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Splash Screen"))

    def load_poli_data(self):
        with open("poliklinik_data.json", "r", encoding="utf-8") as file:
            self.poli_data = json.load(file)["poliklinik"]
        
        self.dropdown_poli.addItems(self.poli_data.keys())
        self.update_dokter_dropdown()
        
    def update_dokter_dropdown(self):
        self.dropdown_dokter.clear()
        poli_terpilih = self.dropdown_poli.currentText()
        if poli_terpilih in self.poli_data:
            self.dropdown_dokter.addItems(self.poli_data[poli_terpilih])
    
    def daftar_pasien(self):
        if not any(user["username"] == self.username for user in load_users()):
            QMessageBox.warning(self, "Error", "Username tidak ditemukan! Silakan daftar terlebih dahulu.")
            return
        
        nama = self.input_nama.text()
        jenis_kelamin = "Pria" if self.radio_pria.isChecked() else "Wanita"
        tanggal_lahir = self.calendar_tanggal_lahir.selectedDate().toString("yyyy-MM-dd")
        poli = self.dropdown_poli.currentText()
        dokter = self.dropdown_dokter.currentText()
        tanggal_temu = self.calendar_tanggal_temu.selectedDate().toString("yyyy-MM-dd")
        keluhan = "-"  # Bisa ditambahkan input untuk keluhan
        nomor_antrian = 1  # Bisa diatur untuk sistem antrian
        
        simpan_data(nama, jenis_kelamin, tanggal_lahir, "-", "Mandiri", poli, dokter, keluhan, tanggal_temu, nomor_antrian, self.username)
        QMessageBox.information(self, "Sukses", "Pendaftaran berhasil!")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
