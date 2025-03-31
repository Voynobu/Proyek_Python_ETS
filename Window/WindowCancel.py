# WindowCancel.py
# Nama: Rangga Muhamad Fajar
# Kelas: 1A - D4
# NIM: 241524026
# Desc: - Program ini digunakan untuk membatalkan pendaftaran pasien di rumah sakit.

# Nama : Muhamad Dino Dermawan
# NIM  : 241524015
# - Menampilkan tabel yang memungkinkan melakukan pembatalan pendaftaran
# - saat melakukan pembatalan, pendaftaran akan terhapus dari database

import sys
import json
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem

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
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        self.riwayat_path = os.path.join(parent_dir, "Data", "riwayat.json")

    def setupUi(self, Dialog):
        self.dialog = Dialog
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(1598, 900)  # Window fixed size
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        
        # Tombol Back
        self.pushButton_3 = HoverButton(Dialog, image_path="C:/ASSETS/BUTTON/BACK.png")
        self.pushButton_3.setGeometry(QtCore.QRect(10, 20, 111, 101))
        self.pushButton_3.setText("")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.backToMenuUser)
        
        # Background
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(-4, 0, 1611, 901))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("C:/ASSETS/BACKGROUND/16.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        
        # Tabel dengan ukuran tepat sampai batas kanan
        self.tableView = QtWidgets.QTableView(Dialog)
        self.tableView.setGeometry(QtCore.QRect(100, 180, 1398, 650))  # Lebar 1398 untuk pas di kanan
        self.tableView.setStyleSheet("""
            QTableView {
                font-size: 12pt;
                background-color: white;
                gridline-color: #dddddd;
                border: 2px solid #0cc0df;
            }
            QHeaderView::section {
                background-color: #0cc0df;
                color: white;
                padding: 12px;
                font-size: 12pt;
                border: none;
            }
            QTableView::item {
                padding: 8px;
                border-right: 1px solid #dddddd;
                border-bottom: 1px solid #dddddd;
            }
        """)
        self.tableView.setObjectName("tableView")
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.tableView.setFixedSize(1398, 650)  # Ukuran fixed
        
        self.label.raise_()
        self.pushButton_3.raise_()
        self.tableView.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
        self.initTable()
        self.loadData()
        
    def initTable(self):
        self.model = QStandardItemModel()
        headers = ["NO", "NAMA", "POLI", "JENIS LAYANAN", "TANGGAL", "NO. ANTRIAN", "AKSI"]
        self.model.setHorizontalHeaderLabels(headers)
        self.tableView.setModel(self.model)
        
        # Lebar kolom disesuaikan untuk memenuhi lebar tabel (total 1398)
        column_widths = [70, 250, 250, 220, 180, 308, 120]  # Total: 70+250+250+220+180+308+120=1398
        for i, width in enumerate(column_widths):
            self.tableView.setColumnWidth(i, width)
        
        # Tinggi baris
        self.tableView.verticalHeader().setDefaultSectionSize(45)
    
    def loadData(self):
        try:
            with open(self.riwayat_path, 'r') as file:
                data = json.load(file)
            
            self.model.setRowCount(0)
            row_count = 0
            
            for username, registrations in data.items():
                for reg in registrations:
                    # Format data sesuai contoh
                    row = [
                        QStandardItem(str(row_count + 1)),
                        QStandardItem(reg['nama'].lower()),  # Nama lowercase seperti contoh
                        QStandardItem(reg['poli']),
                        QStandardItem(reg['jenis_layanan']),
                        QStandardItem(reg['tanggal_temu']),
                        QStandardItem(reg['nomor antrian'])
                    ]
                    
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    
                    for item in row:
                        item.setTextAlignment(QtCore.Qt.AlignCenter)
                        item.setFont(font)
                        item.setForeground(QtGui.QColor(50, 50, 50))
                        item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                    
                    self.model.appendRow(row)
                    row_count += 1
            
            self.addCancelButtons()
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Gagal memuat data: {str(e)}")

    def addCancelButtons(self):
        for row in range(self.model.rowCount()):
            btn = QtWidgets.QPushButton("Batalkan")
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #ff5555;
                    color: white;
                    border-radius: 4px;
                    padding: 6px 10px;
                    font-weight: bold;
                    font-size: 11pt;
                    min-width: 90px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #ff3333;
                }
            """)
            btn.clicked.connect(lambda _, r=row: self.confirmCancel(r))
            self.tableView.setIndexWidget(self.model.index(row, 6), btn)

    def confirmCancel(self, row):
        no_antrian = self.model.item(row, 5).text()
        
        reply = QtWidgets.QMessageBox.question(
            None,
            'Konfirmasi Pembatalan',
            f'Apakah Anda yakin ingin membatalkan pendaftaran dengan nomor antrian:\n{no_antrian}?',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            self.cancelRegistration(no_antrian)

    def cancelRegistration(self, no_antrian):
        try:
            with open(self.riwayat_path, 'r') as file:
                data = json.load(file)
            
            for username in list(data.keys()):
                for i, reg in enumerate(data[username]):
                    if reg['nomor antrian'] == no_antrian:
                        data[username].pop(i)
                        
                        if not data[username]:
                            del data[username]
                        
                        with open(self.riwayat_path, 'w') as file:
                            json.dump(data, file, indent=4)
                        
                        self.loadData()
                        QtWidgets.QMessageBox.information(None, 'Berhasil', 'Pendaftaran berhasil dibatalkan!')
                        return
            
            QtWidgets.QMessageBox.warning(None, 'Data Tidak Ditemukan', 'Nomor antrian tidak ditemukan!')
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, 'Error', f'Gagal membatalkan pendaftaran: {str(e)}')

    def backToMenuUser(self):
        from WindowMenuUser import WindowMenuUser
        self.menu_user = WindowMenuUser("test")
        self.menu_user.show()
        self.dialog.close()
    
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Pembatalan Pendaftaran"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.setFixedSize(1598, 900)  # Window fixed size
    Dialog.show()
    sys.exit(app.exec_())
