# WindowEditPoli.py
# Nama: Rangga Muhamad Fajar
# Kelas: 1A - D4
# NIM: 241524026
# Desc: Program ini menampilkan jendela untuk mengelola (menambah/hapus) data poli 
#       di aplikasi pendaftaran rumah sakit. Tabel poli bersifat read-only dan 
#       dapat diperbarui hanya melalui tombol tambah atau hapus.

import json
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class HoverButton(QtWidgets.QPushButton):
    def __init__(self, parent=None, image_path=""):
        super().__init__(parent)
        self.opacity_effect = QtWidgets.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1.0)
        self.opacity_animation = QtCore.QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_animation.setDuration(200)
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
    def __init__(self, parent_window=None):
        self.parent_window = parent_window

    def setupUi(self, Dialog):
        self.dialog = Dialog
        Dialog.setObjectName("Dialog")
        Dialog.resize(1600, 900)
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        
        # ------ Input Field ------
        self.lineEdit_1 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_1.setGeometry(QtCore.QRect(963, 430, 481, 71))
        self.lineEdit_1.setStyleSheet(
            "QLineEdit {"
            "    color: black; "
            "    border: none; "
            "    border-bottom: 4px solid #a6a6a6; "
            "    font-size: 24px;"
            "}"
            "QLineEdit:focus {"
            "    border-bottom: 4px solid #ffbd59;"
            "}"
        )
        self.lineEdit_1.setPlaceholderText("Masukkan Nama Poli! (Contoh: Umum)")
        
        # ------ BACK BUTTON ------
        self.pushButton_3 = HoverButton(Dialog, image_path="C:/ASSETS/BUTTON/BACK.png")
        self.pushButton_3.setGeometry(QtCore.QRect(10, 20, 111, 101))
        self.pushButton_3.clicked.connect(self.backToParent)
        
        # ------ BACKGROUND LABEL ------
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(-4, 0, 1611, 901))
        self.label.setPixmap(QtGui.QPixmap("C:/ASSETS/BACKGROUND/10.png"))
        self.label.setScaledContents(True)
        
        # ------ TOMBOL TAMBAH POLI ------ 
        self.pushButton_1 = HoverButton(Dialog, image_path="C:/ASSETS/BUTTON/TAMBAH_POLI.png")
        self.pushButton_1.setGeometry(QtCore.QRect(911, 547, 591, 87))
        
        # ------ TOMBOL HAPUS POLI ------ 
        self.pushButton_2 = HoverButton(Dialog, image_path="C:/ASSETS/BUTTON/HAPUS_POLI.png")
        self.pushButton_2.setGeometry(QtCore.QRect(911, 663, 591, 87))
        
        # ------ TABEL VIEW ------
        self.tableView = QtWidgets.QTableView(Dialog)
        self.tableView.setGeometry(QtCore.QRect(100, 238, 601, 571))
        self.tableView.setStyleSheet(
            """
            QTableView {
                gridline-color: gray;
                font-size: 28px;
            }
            QHeaderView::section {
                background-color: #0cc0df;
                color: white;
                padding: 8px;
                font-weight: bold;
                font-size: 28px;
            }
            """
        )
        
        # Init model dan load data
        self.initModel()
        self.loadData()
        
        # Konfigurasi tabel
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tableView.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.setShowGrid(True)

        header = self.tableView.horizontalHeader()
        header.setSectionsMovable(False)
        header.setDefaultAlignment(QtCore.Qt.AlignCenter)
        header.setFixedHeight(100)
        self.tableView.verticalHeader().setDefaultSectionSize(100)

        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        self.tableView.setColumnWidth(0, 70)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        # Z-order
        self.label.lower()
        self.lineEdit_1.raise_()
        self.pushButton_3.raise_()
        self.pushButton_1.raise_()
        self.pushButton_2.raise_()
        self.tableView.raise_()

        # Hubungkan tombol
        self.pushButton_1.clicked.connect(self.tambah_poli)
        self.pushButton_2.clicked.connect(self.hapus_poli)

    def initModel(self):
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["NO", "NAMA POLI"])
        self.tableView.setModel(self.model)

    def loadData(self):
        try:
            with open("JadwalPoli.json", "r") as file:
                data = json.load(file)
            
            self.model.setRowCount(0)
            for idx, poli in enumerate(data["daftar_poli"], start=1):
                item_no = QStandardItem(str(idx))
                item_no.setTextAlignment(QtCore.Qt.AlignCenter)
                
                item_poli = QStandardItem(poli["nama_poli"])
                item_poli.setTextAlignment(QtCore.Qt.AlignCenter)
                
                self.model.appendRow([item_no, item_poli])
                
        except Exception as e:
            print("Error membaca file JSON:", e)

    def tambah_poli(self):
        nama_poli = self.lineEdit_1.text().strip()
        
        if not nama_poli:
            QtWidgets.QMessageBox.warning(self.dialog, "Error", "Nama Poli harus diisi!")
            return
            
        try:
            with open("JadwalPoli.json", "r") as file:
                data = json.load(file)
        except:
            data = {"daftar_poli": []}
            
        # Cek apakah poli sudah ada
        for poli in data["daftar_poli"]:
            if poli["nama_poli"].lower() == nama_poli.lower():
                QtWidgets.QMessageBox.warning(self.dialog, "Error", "Poli sudah ada!")
                return
                
        # Tambahkan poli baru dengan kuota default 20
        new_poli = {
            "nama_poli": nama_poli,
            "kuota": 5,
            "dokter_list": [],
            "jadwal_list": []
        }
        data["daftar_poli"].append(new_poli)
        
        with open("JadwalPoli.json", "w") as file:
            json.dump(data, file, indent=4)
            
        QtWidgets.QMessageBox.information(self.dialog, "Sukses", "Poli berhasil ditambahkan!")
        self.loadData()
        self.lineEdit_1.clear()

    def hapus_poli(self):
        nama_poli = self.lineEdit_1.text().strip()
        
        if not nama_poli:
            QtWidgets.QMessageBox.warning(self.dialog, "Error", "Nama Poli harus diisi!")
            return
            
        try:
            with open("JadwalPoli.json", "r") as file:
                data = json.load(file)
        except:
            QtWidgets.QMessageBox.warning(self.dialog, "Error", "Data poli tidak ditemukan!")
            return
            
        # Cari dan hapus poli
        for i, poli in enumerate(data["daftar_poli"]):
            if poli["nama_poli"].lower() == nama_poli.lower():
                data["daftar_poli"].pop(i)
                with open("JadwalPoli.json", "w") as file:
                    json.dump(data, file, indent=4)
                QtWidgets.QMessageBox.information(self.dialog, "Sukses", "Poli berhasil dihapus!")
                self.loadData()
                self.lineEdit_1.clear()
                return
                
        QtWidgets.QMessageBox.warning(self.dialog, "Error", "Poli tidak ditemukan!")

    def backToParent(self):
        if self.parent_window:
            self.parent_window.show()
        self.dialog.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())