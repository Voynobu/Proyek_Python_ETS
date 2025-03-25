# Nama        : Ivan Setiawan Ihsan
# NIM/Kelas   : 241524012
# Kelas       : 1-A D4 Teknik Informatika
# Description : Window untuk pendaftaran pasien

import sys
import json
import os
from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QCalendarWidget, QDateEdit, QMessageBox
from PyQt5.QtCore import QDate
from Pasien import simpan_data
from Register import load_users

BASE_DIR = Path(__file__).parent.parent  # Naik satu level ke folder ETS
POLIKLINIK_FILE = BASE_DIR / "Data" / "poliklinik_data.json"

class HoverButton(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.installEventFilter(self)
        self.opacity_effect = QtWidgets.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1.0)
    
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.HoverEnter:
            self.opacity_effect.setOpacity(0.7)
        elif event.type() == QtCore.QEvent.HoverLeave:
            self.opacity_effect.setOpacity(1.0)
        return super().eventFilter(obj, event)

class WindowPendaftaranPasien(QDialog):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setupUi()
    
    def setupUi(self):
        self.setObjectName("Form")
        self.setFixedSize(1600, 900)  # Ukuran window disamakan dengan WindowMenuAdmin/User
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        
        # Label background
        self.label_background = QtWidgets.QLabel(self)
        self.label_background.setGeometry(QtCore.QRect(-4, 0, 1611, 901))
        self.label_background.setPixmap(QtGui.QPixmap("C:/ASSETS/BACKGROUND/8.png"))
        self.label_background.setScaledContents(True)
        self.label_background.lower()
        self.label_background.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        
        # Input fields
        self.keluhan = QtWidgets.QLineEdit(self)
        self.keluhan.setGeometry(QtCore.QRect(636, 515, 377, 184))
        self.keluhan.setStyleSheet("background: transparent; border: none;")
        self.keluhan.setPlaceholderText("Masukkan Keluhan")

        self.Nama = QtWidgets.QLineEdit(self)
        self.Nama.setGeometry(QtCore.QRect(92, 261, 514, 58))
        self.Nama.setStyleSheet("background: transparent; border: none;")
        self.Nama.setPlaceholderText("Masukkan nama lengkap")

        self.poli = QtWidgets.QComboBox(self)
        self.poli.setGeometry(QtCore.QRect(91, 514, 516, 58))
        self.poli.currentTextChanged.connect(self.updateDokter)

        self.dokter = QtWidgets.QComboBox(self)
        self.dokter.setGeometry(QtCore.QRect(91, 641, 514, 58))
        self.dokter.setPlaceholderText("Pilih dokter")

        self.pilih_jadwal = QDateEdit(self)
        self.pilih_jadwal.setGeometry(QtCore.QRect(93, 768, 514, 58))
        self.pilih_jadwal.setCalendarPopup(True)
        self.pilih_jadwal.setDate(QDate.currentDate())
        self.pilih_jadwal.dateChanged.connect(self.update_calendar_pilih_jadwal)

        self.calendar_tanggal_lahir = QCalendarWidget(self)
        self.calendar_tanggal_lahir.setGeometry(QtCore.QRect(636, 450, 376, 250))
        self.calendar_tanggal_lahir.hide()
        self.calendar_tanggal_lahir.clicked.connect(self.set_tanggal_lahir)

        self.calendar_pilih_jadwal = QCalendarWidget(self)
        self.calendar_pilih_jadwal.setGeometry(QtCore.QRect(93, 820, 514, 250))
        self.calendar_pilih_jadwal.hide()
        self.calendar_pilih_jadwal.clicked.connect(self.set_pilih_jadwal)

        self.tanggal_lahir = QDateEdit(self)
        self.tanggal_lahir.setGeometry(QtCore.QRect(636, 388, 376, 58))
        self.tanggal_lahir.setCalendarPopup(True)
        self.tanggal_lahir.setDate(QDate.currentDate())
        self.tanggal_lahir.dateChanged.connect(self.update_calendar_tanggal_lahir)

        self.pria = QtWidgets.QRadioButton(self)
        self.pria.setGeometry(QtCore.QRect(660, 279, 95, 20))
        self.pria.setStyleSheet("background: transparent; border: none;")

        self.wanita = QtWidgets.QRadioButton(self)
        self.wanita.setGeometry(QtCore.QRect(831, 279, 95, 20))
        self.wanita.setStyleSheet("background: transparent; border: none;")

        self.jenis_layanan = QtWidgets.QComboBox(self)
        self.jenis_layanan.setGeometry(QtCore.QRect(91, 387, 516, 58))
        self.jenis_layanan.addItems(["Mandiri", "Asuransi", "BPJS"])
        self.jenis_layanan.setStyleSheet("background: transparent; border: none;")

        # Tombol Back dengan gambar melalui styleSheet (HoverButton)
        self.back = HoverButton(self)
        self.back.setGeometry(QtCore.QRect(10, 20, 111, 101))
        self.back.setStyleSheet("border-image: url(C:/ASSETS/BUTTON/BACK.png); background: transparent; border: none;")
        self.back.clicked.connect(self.back_to_menu)

        # Tombol Daftar (Submit) dengan gambar melalui styleSheet (HoverButton)
        self.daftar = HoverButton(self)
        self.daftar.setGeometry(QtCore.QRect(686, 741, 282, 88))
        self.daftar.setStyleSheet("border-image: url(C:/ASSETS/BUTTON/SUBMIT.png); background: transparent; border: none;")
        self.daftar.clicked.connect(self.daftar_pasien)
        
        self.loadData()
    
    def loadData(self):
        """Membaca file JSON dan mengisi dropdown poliklinik."""
        with open(POLIKLINIK_FILE, "r") as file:
            data = json.load(file)
            self.poliklinik_data = data.get("poliklinik", {})
        self.poli.clear()
        self.poli.addItems(self.poliklinik_data.keys())
        self.updateDokter()
    
    def updateDokter(self):
        """Mengupdate daftar dokter berdasarkan poliklinik yang dipilih."""
        selectedPoliklinik = self.poli.currentText()
        self.dokter.clear()
        if selectedPoliklinik in self.poliklinik_data:
            self.dokter.addItems(self.poliklinik_data[selectedPoliklinik])
    
    def back_to_menu(self):
        from WindowMenuUser import WindowMenuUser
        self.menu_user = WindowMenuUser(self.username)
        self.menu_user.show()
        self.close()
    
    def update_calendar_tanggal_lahir(self, date):
        self.calendar_tanggal_lahir.setSelectedDate(date)
        self.calendar_tanggal_lahir.show()
    
    def set_tanggal_lahir(self, date):
        self.tanggal_lahir.setDate(date)
        self.calendar_tanggal_lahir.hide()
    
    def update_calendar_pilih_jadwal(self, date):
        self.calendar_pilih_jadwal.setSelectedDate(date)
        self.calendar_pilih_jadwal.show()
    
    def set_pilih_jadwal(self, date):
        self.pilih_jadwal.setDate(date)
        self.calendar_pilih_jadwal.hide()
    
    def daftar_pasien(self):
        if not any(user["username"] == self.username for user in load_users()):
            QMessageBox.warning(self, "Error", "Username tidak ditemukan! Silakan daftar terlebih dahulu.")
            return
        if self.pilih_jadwal.date() <= QDate.currentDate():
            QMessageBox.warning(self, "Peringatan", "Tanggal pendaftaran harus minimal hari esok!")
            return
        nama = self.Nama.text()
        jenis_kelamin = "Pria" if self.pria.isChecked() else "Wanita" if self.wanita.isChecked() else ""
        poli = self.poli.currentText()
        dokter = self.dokter.currentText()
        jenis_layanan = self.jenis_layanan.currentText()
        keluhan = self.keluhan.text()
        tanggal_lahir = self.tanggal_lahir.date().toString("dd-MM-yyyy")
        pilih_jadwal = self.pilih_jadwal.date().toString("dd-MM-yyyy")
        if not (nama and jenis_kelamin and poli and dokter and keluhan):
            QMessageBox.warning(self, "Peringatan", "Semua field harus diisi sebelum mendaftar!")
            return
        simpan_data(nama, jenis_kelamin, tanggal_lahir, jenis_layanan, poli, dokter, keluhan, pilih_jadwal, self.username)
        QMessageBox.information(self, "Sukses", "Pendaftaran berhasil!")
        self.close()
        self.back_to_menu()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WindowPendaftaranPasien("Guest")
    window.show()
    sys.exit(app.exec_())
