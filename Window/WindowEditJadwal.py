# WindowEditJadwal.py
# Nama: Rangga Muhamad Fajar
# Kelas: 1A - D4
# NIM: 241524026
# Desc: Program untuk mengelola jadwal layanan poli di rumah sakit

import os
import sys
import json
import datetime
import copy
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from Utils.SoundManager import SoundManager
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class HoverButton(QtWidgets.QPushButton):
    def __init__(self, parent=None, image_path=""):
        super().__init__(parent)
        self.opacity_effect = QtWidgets.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_animation = QtCore.QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_animation.setDuration(200)
        self.opacity_effect.setOpacity(1.0)
        if image_path:
            self.setStyleSheet(
                f"QPushButton {{ border-image: url('{image_path}'); background: transparent; border: none; }}"
            )
        self.setMouseTracking(True)

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

class Ui_Dialog(object):
    def __init__(self, parent_window=None, json_data=None):
        self.parent_window = parent_window
        self.original_data = json_data if json_data else self.load_data()
        self.updated_data = copy.deepcopy(self.original_data)
        self.data_updated = False
        self.selected_poli_index = -1
        self.selected_jadwal_index = -1

    def setupUi(self, Dialog):
        SoundManager.play("interface")
        self.dialog = Dialog
        Dialog.setObjectName("Dialog")
        Dialog.resize(1600, 900)
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        
        # ------ Input Field: Masukkan Hari ------
        self.lineEdit_1 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_1.setGeometry(QtCore.QRect(154, 554, 648, 51))
        self.lineEdit_1.setStyleSheet(
            "QLineEdit {"
            "    color: black; "
            "    border: none; "
            "    border-bottom: 4px solid #a6a6a6; "
            "    font-size: 20px;"
            "}"
            "QLineEdit:focus {"
            "    border-bottom: 4px solid #ffbd59;"
            "}"
        )
        self.lineEdit_1.setObjectName("lineEdit_1")
        self.lineEdit_1.setPlaceholderText("Masukkan Hari (Contoh: Monday)")
        
        # ------ Input Field: Masukkan Jam Awal ------
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(154, 639, 648, 51))
        self.lineEdit_2.setStyleSheet(
            "QLineEdit {"
            "    color: black; "
            "    border: none; "
            "    border-bottom: 4px solid #a6a6a6; "
            "    font-size: 20px;"
            "}"
            "QLineEdit:focus {"
            "    border-bottom: 4px solid #ffbd59;"
            "}"
        )
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setPlaceholderText("Masukkan Jam Awal (Format: HH:MM)")
        
        # ------ Input Field: Masukkan Jam Akhir ------
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(154, 724, 648, 51))
        self.lineEdit_3.setStyleSheet(
            "QLineEdit {"
            "    color: black; "
            "    border: none; "
            "    border-bottom: 4px solid #a6a6a6; "
            "    font-size: 20px;"
            "}"
            "QLineEdit:focus {"
            "    border-bottom: 4px solid #ffbd59;"
            "}"
        )
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setPlaceholderText("Masukkan Jam Akhir (Format: HH:MM)")
        
        # ------ BACK BUTTON ------
        self.pushButton_4 = HoverButton(Dialog, image_path="C:/ASSETS/BUTTON/BACK.png")
        self.pushButton_4.setGeometry(QtCore.QRect(10, 20, 111, 101))
        self.pushButton_4.setText("")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.backToParent)
        
        # ------ BACKGROUND LABEL ------
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(-4, 0, 1611, 901))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("C:/ASSETS/BACKGROUND/9.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        
        # ------ TOMBOL TAMBAH JADWAL ------
        self.pushButton_1 = HoverButton(Dialog, image_path="C:/ASSETS/BUTTON/TAMBAH_JADWAL.png")
        self.pushButton_1.setGeometry(QtCore.QRect(848, 364, 601, 129))
        self.pushButton_1.setText("")
        self.pushButton_1.setObjectName("pushButton_1")
        self.pushButton_1.clicked.connect(self.tambah_jadwal)
        
        # ------ TOMBOL UPDATE JADWAL ------
        self.pushButton_2 = HoverButton(Dialog, image_path="C:/ASSETS/BUTTON/UPDATE_JADWAL.png")
        self.pushButton_2.setGeometry(QtCore.QRect(848, 507, 601, 129))
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.update_jadwal)
        
        # ------ TOMBOL HAPUS JADWAL ------
        self.pushButton_3 = HoverButton(Dialog, image_path="C:/ASSETS/BUTTON/HAPUS_JADWAL.png")
        self.pushButton_3.setGeometry(QtCore.QRect(848, 652, 601, 129))
        self.pushButton_3.setText("")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.hapus_jadwal)
        
        # ------ COMBOBOX (Pilih Poli) ------
        self.comboBox_2 = QtWidgets.QComboBox(Dialog)
        self.comboBox_2.setGeometry(QtCore.QRect(154, 382, 648, 51))
        self.comboBox_2.setStyleSheet(
            "QComboBox {"
            "    color: black;"
            "    border: none;"
            "    border-bottom: 4px solid #a6a6a6;"
            "    font-size: 20px;"
            "    padding: 5px 10px;"
            "    background: transparent;"
            "    padding-right: 40px;"
            "}"
            "QComboBox:focus {"
            "    border-bottom: 4px solid #ffbd59;"
            "}"
            "QComboBox::drop-down {"
            "    border: none;"
            "    width: 30px;"
            "    subcontrol-origin: padding;"
            "    subcontrol-position: center right;"
            "}"
            "QComboBox::down-arrow {"
            "    image: url(C:/ASSETS/BUTTON/ARROW.png);"
            "    width: 50px;"
            "    height: 50px;"
            "    margin-right: 20px;"
            "}"
        )
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("Pilih Poli")
        self.comboBox_2.model().item(0).setEnabled(False)
        
        # Load poli data from JSON
        for poli in self.updated_data["daftar_poli"]:
            self.comboBox_2.addItem(poli["nama_poli"])
        
        self.comboBox_2.currentIndexChanged.connect(self.update_dokter_combo)
        
        # ------ COMBOBOX (Pilih Dokter) ------
        self.comboBox_3 = QtWidgets.QComboBox(Dialog)
        self.comboBox_3.setGeometry(QtCore.QRect(154, 467, 648, 51))
        self.comboBox_3.setStyleSheet(
            "QComboBox {"
            "    color: black;"
            "    border: none;"
            "    border-bottom: 4px solid #a6a6a6;"
            "    font-size: 20px;"
            "    padding: 5px 10px;"
            "    background: transparent;"
            "    padding-right: 40px;"
            "}"
            "QComboBox:focus {"
            "    border-bottom: 4px solid #ffbd59;"
            "}"
            "QComboBox::drop-down {"
            "    border: none;"
            "    width: 30px;"
            "    subcontrol-origin: padding;"
            "    subcontrol-position: center right;"
            "}"
            "QComboBox::down-arrow {"
            "    image: url(C:/ASSETS/BUTTON/ARROW.png);"
            "    width: 50px;"
            "    height: 50px;"
            "    margin-right: 20px;"
            "}"
        )
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("Pilih Dokter")
        self.comboBox_3.model().item(0).setEnabled(False)
        
        # Atur urutan tampilan widget
        self.label.raise_()
        self.lineEdit_1.raise_()
        self.lineEdit_2.raise_()
        self.pushButton_4.raise_()
        self.lineEdit_3.raise_()
        self.pushButton_1.raise_()
        self.pushButton_2.raise_()
        self.pushButton_3.raise_()
        self.comboBox_2.raise_()
        self.comboBox_3.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Window Edit Jadwal"))
    
    def load_data(self):
        try:
            with open("JadwalPoli.json", "r", encoding="utf-8") as file:
                return json.load(file)
        except:
            return {
                "daftar_poli": [
                    {
                        "nama_poli": "POLI JANTUNG",
                        "dokter_list": [{"nama": "Dr. Asep", "spesialis": "Kardiolog"}],
                        "jadwal_list": [],
                        "kuota": 5
                    },
                    {
                        "nama_poli": "POLI MATA",
                        "dokter_list": [{"nama": "Dr. Ahmad", "spesialis": "Oftalmolog"}],
                        "jadwal_list": [],
                        "kuota": 5
                    },
                    {
                        "nama_poli": "POLI THT-KL",
                        "dokter_list": [{"nama": "Dr. Messi", "spesialis": "Spesialis THT-KH"}],
                        "jadwal_list": [],
                        "kuota": 5
                    },
                    {
                        "nama_poli": "POLI SARAF",
                        "dokter_list": [{"nama": "Dr. Jajang", "spesialis": "Neurolog"}],
                        "jadwal_list": [],
                        "kuota": 5
                    },
                    {
                        "nama_poli": "POLI ANAK",
                        "dokter_list": [{"nama": "Dr. Radhit", "spesialis": "Pediatrik Gawat Darurat"}],
                        "jadwal_list": [],
                        "kuota": 5
                    }
                ]
            }

    def save_data(self):
        try:
            with open("JadwalPoli.json", "w", encoding="utf-8") as file:
                json.dump(self.updated_data, file, indent=4)
            self.data_updated = True
            return True
        except Exception as e:
            QMessageBox.critical(self.dialog, "Error", f"Gagal menyimpan data: {str(e)}")
            return False

    def update_dokter_combo(self):
        self.comboBox_3.clear()
        self.comboBox_3.addItem("Pilih Dokter")
        self.comboBox_3.model().item(0).setEnabled(False)
        
        poli_index = self.comboBox_2.currentIndex() - 1
        if 0 <= poli_index < len(self.updated_data["daftar_poli"]):
            selected_poli = self.updated_data["daftar_poli"][poli_index]
            for dokter in selected_poli["dokter_list"]:
                self.comboBox_3.addItem(f"{dokter['nama']} ({dokter['spesialis']})")

    def validate_input(self):
        if self.comboBox_2.currentIndex() == 0:
            QMessageBox.warning(self.dialog, "Peringatan", "Pilih poli terlebih dahulu!")
            return False
        
        if self.comboBox_3.currentIndex() == 0:
            QMessageBox.warning(self.dialog, "Peringatan", "Pilih dokter terlebih dahulu!")
            return False
        
        if not self.lineEdit_1.text().strip():
            QMessageBox.warning(self.dialog, "Peringatan", "Masukkan hari terlebih dahulu!")
            return False
            
        if not self.lineEdit_2.text().strip():
            QMessageBox.warning(self.dialog, "Peringatan", "Masukkan jam awal terlebih dahulu!")
            return False
            
        if not self.lineEdit_3.text().strip():
            QMessageBox.warning(self.dialog, "Peringatan", "Masukkan jam akhir terlebih dahulu!")
            return False
            
        if not self.validate_time_format(self.lineEdit_2.text()):
            QMessageBox.warning(self.dialog, "Peringatan", "Format jam awal tidak valid! Gunakan HH:MM")
            return False
            
        if not self.validate_time_format(self.lineEdit_3.text()):
            QMessageBox.warning(self.dialog, "Peringatan", "Format jam akhir tidak valid! Gunakan HH:MM")
            return False
            
        return True

    def validate_time_format(self, time_str):
        try:
            hours, minutes = map(int, time_str.split(':'))
            return 0 <= hours < 24 and 0 <= minutes < 60
        except:
            return False

    def find_poli_index(self, poli_name):
        for index, poli in enumerate(self.updated_data["daftar_poli"]):
            if poli["nama_poli"] == poli_name:
                return index
        return -1

    def clear_input_fields(self):
        self.lineEdit_1.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()

    def get_dokter_name(self):
        dokter_text = self.comboBox_3.currentText()
        return dokter_text.split(" (")[0] if " (" in dokter_text else dokter_text

    def get_jadwal_status(self, hari, jam_awal, jam_akhir):
        try:
            now = datetime.datetime.now()
            current_day = now.strftime("%A")
            current_time = now.time()
            
            start = datetime.datetime.strptime(jam_awal, "%H:%M").time()
            end = datetime.datetime.strptime(jam_akhir, "%H:%M").time()
            
            if current_day.upper() == hari.upper() and start <= current_time <= end:
                return "AVAILABLE"
            return "UNAVAILABLE"
        except:
            return "UNAVAILABLE"

    def tambah_jadwal(self):
        if not self.validate_input():
            return

        poli_index = self.comboBox_2.currentIndex() - 1
        if poli_index < 0:
            return

        hari = self.lineEdit_1.text()
        jam_awal = self.lineEdit_2.text()
        jam_akhir = self.lineEdit_3.text()

        new_jadwal = {
            "dokter": self.get_dokter_name(),
            "hari": hari,
            "jam_awal": jam_awal,
            "jam_akhir": jam_akhir,
            "status": self.get_jadwal_status(hari, jam_awal, jam_akhir)
        }

        self.updated_data["daftar_poli"][poli_index]["jadwal_list"].append(new_jadwal)
        if self.save_data():
            QMessageBox.information(self.dialog, "Sukses", "Jadwal berhasil ditambahkan!")
            self.clear_input_fields()

    def update_jadwal(self):
        if not self.validate_input():
            return

        poli_index = self.comboBox_2.currentIndex() - 1
        if poli_index < 0:
            return

        if self.selected_jadwal_index == -1:
            jadwal_items = [
                f"{j['hari']} ({j['jam_awal']}-{j['jam_akhir']}) - {j.get('status', 'Available')}"
                for j in self.updated_data["daftar_poli"][poli_index]["jadwal_list"]
            ]
            
            if not jadwal_items:
                QMessageBox.warning(self.dialog, "Peringatan", "Tidak ada jadwal untuk diupdate!")
                return
                
            item, ok = QtWidgets.QInputDialog.getItem(
                self.dialog, "Pilih Jadwal", "Pilih jadwal yang akan diupdate:", 
                jadwal_items, 0, False
            )
            
            if not ok:
                return
                
            self.selected_jadwal_index = jadwal_items.index(item)

        hari = self.lineEdit_1.text()
        jam_awal = self.lineEdit_2.text()
        jam_akhir = self.lineEdit_3.text()

        self.updated_data["daftar_poli"][poli_index]["jadwal_list"][self.selected_jadwal_index] = {
            "dokter": self.get_dokter_name(),
            "hari": hari,
            "jam_awal": jam_awal,
            "jam_akhir": jam_akhir,
            "status": self.get_jadwal_status(hari, jam_awal, jam_akhir)
        }

        if self.save_data():
            QMessageBox.information(self.dialog, "Sukses", "Jadwal berhasil diupdate!")
            self.clear_input_fields()
            self.selected_jadwal_index = -1

    def hapus_jadwal(self):
        poli_index = self.comboBox_2.currentIndex() - 1
        if poli_index < 0:
            QMessageBox.warning(self.dialog, "Peringatan", "Pilih poli terlebih dahulu!")
            return

        if self.selected_jadwal_index == -1:
            jadwal_items = [
                f"{j['hari']} ({j['jam_awal']}-{j['jam_akhir']})"
                for j in self.updated_data["daftar_poli"][poli_index]["jadwal_list"]
            ]
            
            if not jadwal_items:
                QMessageBox.warning(self.dialog, "Peringatan", "Tidak ada jadwal untuk dihapus!")
                return
                
            item, ok = QtWidgets.QInputDialog.getItem(
                self.dialog, "Hapus Jadwal", "Pilih jadwal yang akan dihapus:", 
                jadwal_items, 0, False
            )
            
            if not ok:
                return
                
            self.selected_jadwal_index = jadwal_items.index(item)

        reply = QMessageBox.question(
            self.dialog, 'Konfirmasi',
            'Yakin ingin menghapus jadwal ini?', 
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.updated_data["daftar_poli"][poli_index]["jadwal_list"].pop(self.selected_jadwal_index)
            if self.save_data():
                QMessageBox.information(self.dialog, "Sukses", "Jadwal berhasil dihapus!")
                self.clear_input_fields()
                self.selected_jadwal_index = -1

    def backToParent(self):
        if self.parent_window:
            if hasattr(self.parent_window, 'ui') and self.data_updated:
                self.parent_window.ui.data = self.updated_data
                self.parent_window.ui.loadData()
            self.parent_window.show()
        self.dialog.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog(parent_window=Dialog)
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())