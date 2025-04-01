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
from Antrian import ambil_nomor_antrian, is_antrian_penuh

BASE_DIR = Path(__file__).parent.parent  # Naik satu level ke folder ETS
POLIKLINIK_FILE = BASE_DIR / "Data" / "jadwalPoli.json"
with open(POLIKLINIK_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)

def get_poli_list():
        return [poli["nama_poli"] for poli in data["daftar_poli"]]

def get_doctor_list(poli_name):
    for poli in data["daftar_poli"]:
        if poli["nama_poli"] == poli_name:
            return [dokter["nama"] for dokter in poli["dokter_list"]]
    return []

def get_schedule(doctor_name, selected_date):
    selected_day = selected_date.toString("dddd")
    for poli in data["daftar_poli"]:
        for jadwal in poli["jadwal_list"]:
            if jadwal["dokter"] == doctor_name and jadwal["hari"] == selected_day:
                if jadwal["status"] == "UNAVAILABLE":
                    return ["Tidak Tersedia"]
                return [f"{jadwal['jam_awal']} - {jadwal['jam_akhir']}"]
    return ["Tidak Tersedia"]

class HoverButton(QtWidgets.QPushButton):
    def __init__(self, parent=None, image_path=""):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.opacity_effect = QtWidgets.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_animation = QtCore.QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_animation.setDuration(200)
        self.opacity_effect.setOpacity(1.0)
        self.image_path = image_path
        if image_path:
            self.setStyleSheet(f"QPushButton {{ border-image: url('{image_path}'); background: transparent; border: none; }}")
    
    def enterEvent(self, event):
        self.opacity_animation.stop()
        self.opacity_animation.setStartValue(self.opacity_effect.opacity())
        self.opacity_animation.setEndValue(0.7)
        self.opacity_animation.start()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self.opacity_animation.stop()
        self.opacity_animation.setStartValue(self.opacity_effect.opacity())
        self.opacity_animation.setEndValue(1.0)
        self.opacity_animation.start()
        super().leaveEvent(event)

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
        self.poli.setGeometry(QtCore.QRect(100, 516, 500, 55))
        self.poli.addItems(get_poli_list())
        self.poli.currentTextChanged.connect(self.update_doctor_list)
        self.poli.setStyleSheet("""
            QComboBox {
                background: transparent;
                color: black; /* Atur warna teks agar tetap terlihat */
                border: none;
            }
            QComboBox QAbstractItemView {
                background: white; /* Latar belakang dropdown tetap terlihat */
                color: black; /* Warna teks item dropdown */
                selection-background-color: gray; /* Warna saat item dipilih */
            }
        """)

        self.dokter = QtWidgets.QComboBox(self)
        self.dokter.setGeometry(QtCore.QRect(100, 643, 500, 55))
        self.dokter.currentTextChanged.connect(self.update_schedule)
        self.dokter.setStyleSheet("""
            QComboBox {
                background: transparent;
                color: black; /* Atur warna teks agar tetap terlihat */
                border: none;
            }
            QComboBox QAbstractItemView {
                background: white; /* Latar belakang dropdown tetap terlihat */
                color: black; /* Warna teks item dropdown */
                selection-background-color: gray; /* Warna saat item dipilih */
            }
        """)

        self.pilih_jadwal = QtWidgets.QComboBox(self)
        self.pilih_jadwal.setGeometry(QtCore.QRect(100, 770, 499, 55))
        self.pilih_jadwal.setPlaceholderText("Pilih jadwal")
        self.pilih_jadwal.setStyleSheet("""
            QComboBox {
                background: transparent;
                color: black; /* Atur warna teks agar tetap terlihat */
                border: none;
            }
            QComboBox QAbstractItemView {
                background: white; /* Latar belakang dropdown tetap terlihat */
                color: black; /* Warna teks item dropdown */
                selection-background-color: gray; /* Warna saat item dipilih */
            }
        """)

        self.calendar_tanggal_temu = QCalendarWidget(self)
        self.calendar_tanggal_temu.setGeometry(QtCore.QRect(636, 450, 376, 250))
        self.calendar_tanggal_temu.hide()
        self.calendar_tanggal_temu.clicked.connect(self.set_tanggal_temu)

        self.tanggal_temu = QDateEdit(self)
        self.tanggal_temu.setGeometry(QtCore.QRect(642, 389, 364, 55))
        self.tanggal_temu.setCalendarPopup(True)
        self.tanggal_temu.setDate(QDate.currentDate())
        self.tanggal_temu.dateChanged.connect(self.update_schedule)

        self.pria = QtWidgets.QRadioButton(self)
        self.pria.setGeometry(QtCore.QRect(660, 279, 95, 20))
        self.pria.setStyleSheet("background: transparent; border: none;")

        self.wanita = QtWidgets.QRadioButton(self)
        self.wanita.setGeometry(QtCore.QRect(831, 279, 95, 20))
        self.wanita.setStyleSheet("background: transparent; border: none;")

        self.jenis_layanan = QtWidgets.QComboBox(self)
        self.jenis_layanan.setGeometry(QtCore.QRect(100, 389, 500, 55))
        self.jenis_layanan.addItems(["Mandiri", "Asuransi", "BPJS"])
        self.jenis_layanan.setStyleSheet("""
            QComboBox {
                background: transparent;
                color: black; /* Atur warna teks agar tetap terlihat */
                border: none;
            }
            QComboBox QAbstractItemView {
                background: white; /* Latar belakang dropdown tetap terlihat */
                color: black; /* Warna teks item dropdown */
                selection-background-color: gray; /* Warna saat item dipilih */
            }
        """)

        # Tombol Back dengan gambar melalui HoverButton
        self.back = HoverButton(self, image_path="C:/ASSETS/BUTTON/BACK.png")
        self.back.setGeometry(QtCore.QRect(10, 20, 111, 101))
        self.back.clicked.connect(self.back_to_menu)

        # Tombol Daftar (Submit) dengan gambar melalui HoverButton
        self.daftar = HoverButton(self, image_path="C:/ASSETS/BUTTON/SUBMIT.png")
        self.daftar.setGeometry(QtCore.QRect(686, 741, 282, 88))
        self.daftar.clicked.connect(self.daftar_pasien)
        
        self.update_doctor_list()
    

    def update_doctor_list(self):
        self.dokter.clear()
        poli_name = self.poli.currentText()
        self.dokter.addItems(get_doctor_list(poli_name))
        self.update_schedule()
    
    def update_schedule(self):
        self.pilih_jadwal.clear()
        doctor_name = self.dokter.currentText()
        selected_date = self.tanggal_temu.date()
        self.pilih_jadwal.addItems(get_schedule(doctor_name, selected_date))
    
    def back_to_menu(self):
        from WindowMenuUser import WindowMenuUser
        self.menu_user = WindowMenuUser(self.username)
        self.menu_user.show()
        self.close()
    
    def update_calendar_tanggal_temu(self, date):
        self.calendar_tanggal_temu.setSelectedDate(date)
        self.calendar_tanggal_temu.show()
    
    def set_tanggal_temu(self, date):
        self.tanggal_temu.setDate(date)
        self.calendar_tanggal_temu.hide()
    
    def daftar_pasien(self):
        if not any(user["username"] == self.username for user in load_users()):
            QMessageBox.warning(self, "Error", "Username tidak ditemukan! Silakan daftar terlebih dahulu.")
            return
        if self.tanggal_temu.date() <= QDate.currentDate():
            QMessageBox.warning(self, "Peringatan", "Tanggal pendaftaran harus minimal hari esok!")
            return
        if self.pilih_jadwal.currentText() == "Tidak Tersedia":
            QMessageBox.warning(self, "Peringatan", "Jadwal yang dipilih tidak tersedia.")
            return
        nama = self.Nama.text()
        jenis_kelamin = "Pria" if self.pria.isChecked() else "Wanita" if self.wanita.isChecked() else ""
        poli = self.poli.currentText()
        dokter = self.dokter.currentText()
        jenis_layanan = self.jenis_layanan.currentText()
        keluhan = self.keluhan.text()
        tanggal_temu = self.tanggal_temu.date().toString("dd-MM-yyyy")
        pilih_jadwal = self.pilih_jadwal.currentText()
        if not (nama and jenis_kelamin and poli and dokter and pilih_jadwal and keluhan):
            QMessageBox.warning(self, "Peringatan", "Semua field harus diisi sebelum mendaftar!")
            return
        if is_antrian_penuh(tanggal_temu, jenis_layanan, poli):
            QMessageBox.warning(self, "Peringatan", f"Antrian poli {poli} pada layanan {jenis_layanan} penuh")
            return
        nomor_antrian = ambil_nomor_antrian(tanggal_temu, jenis_layanan, poli)
        simpan_data(nama, jenis_kelamin, tanggal_temu, jenis_layanan, poli, dokter, keluhan, pilih_jadwal, self.username, nomor_antrian)
        QMessageBox.information(self, "Sukses", "Pendaftaran berhasil!. Lihat menu riwayat untuk melihat detail pendaftaran. ")
        self.close()
        self.back_to_menu()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WindowPendaftaranPasien("Guest")
    window.show()
    sys.exit(app.exec_())
