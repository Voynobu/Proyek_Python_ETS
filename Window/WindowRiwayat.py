# WindowRiwayat.py
# Nama: Rangga Muhamad Fajar dan Nauval Khairiyan
# Kelas: 1A - D4
# NIM: 241524026 dan 241524021
# Desc: - Program ini digunakan untuk melihat detail riwayat pendaftaran pasien di rumah sakit.

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
    def __init__(self, username):
        self.username = username  # Simpan username untuk digunakan nanti

    def setupUi(self, Dialog):
        self.dialog = Dialog
        Dialog.setObjectName("Dialog")
        Dialog.resize(1598, 900)
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # Tombol Back
        self.pushButton_3 = HoverButton(Dialog, image_path="C:/ASSETS/BUTTON/BACK.png")
        self.pushButton_3.setGeometry(QtCore.QRect(10, 20, 111, 101))
        self.pushButton_3.setText("")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.backToMenu)
        
        # Background label
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(-4, 0, 1611, 901))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("C:/ASSETS/BACKGROUND/15.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        
        # Tabel untuk menampilkan data riwayat (fixed size seperti semula)
        self.tableView = QtWidgets.QTableView(Dialog)
        self.tableView.setGeometry(QtCore.QRect(236, 210, 1110, 601))
        self.tableView.setStyleSheet("""
            QTableView {
                font-size: 12pt;
                background-color: white;
                gridline-color: #dddddd;
                border: 2px solid #ffbd59;
                selection-background-color: transparent;
                selection-color: black;
            }
            QHeaderView::section {
                background-color: #ffbd59;
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
            QTableView::item:selected {
                background: transparent;
                color: black;
            }
            QTableView::item:hover {
                background: #f0f0f0;
            }
        """)
        self.tableView.setObjectName("tableView")
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableView.verticalHeader().setVisible(False)
        font = QtGui.QFont("Garet", 12, QtGui.QFont.Bold)
        self.tableView.horizontalHeader().setFont(font)
        self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tableView.setFocusPolicy(QtCore.Qt.NoFocus)
        
        # Gunakan default row height (tidak dinamis)
        self.tableView.verticalHeader().setDefaultSectionSize(45)
        
        # Pastikan background berada di bawah, lalu tombol dan tabel
        self.label.raise_()
        self.pushButton_3.raise_()
        self.tableView.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
        self.initTable()
        self.loadData()

    def initTable(self):
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["JADWAL CHECK-UP", "NOMOR ANTRIAN", "STATUS", "LIHAT DETAIL"])
        self.tableView.setModel(self.model)

        header = self.tableView.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Fixed)  # Pastikan pakai ukuran tetap

        # Atur ukuran kolom secara manual
        self.tableView.setColumnWidth(0, 366)  # JADWAL CHECK-UP diperbesar
        self.tableView.setColumnWidth(1, 310)  # NOMOR ANTRIAN default
        self.tableView.setColumnWidth(2, 180)  # STATUS diperkecil
        self.tableView.setColumnWidth(3, 250)  # LIHAT DETAIL

        # Tambahan biar user nggak resize kolom sendiri
        header.setSectionsMovable(False)
        header.setStretchLastSection(False)

    def loadData(self):
        file_path = "Data/riwayat.json"
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
            
            if not isinstance(data, dict):
                data = {}
            
            username_login = self.username  
            self.model.setRowCount(0)
            
            if username_login not in data:
                QtWidgets.QMessageBox.information(self.dialog, "Info", "Tidak ada pendaftaran untuk user ini")
                return

            for riwayat in data[username_login]:
                tanggal_temu = riwayat.get("tanggal_temu", "N/A")
                jadwal = riwayat.get("jadwal", "N/A")
                nomor_antrian = riwayat.get("nomor antrian", "N/A")
                status = riwayat.get("status", "N/A")
                
                item_jadwal = QStandardItem(f"{tanggal_temu} - {jadwal}")
                item_jadwal.setTextAlignment(QtCore.Qt.AlignCenter)
                item_jadwal.setFont(QtGui.QFont("Arial", 8))
                item_jadwal.setFlags(item_jadwal.flags() & ~QtCore.Qt.ItemIsEditable)
                
                item_antrian = QStandardItem(nomor_antrian)
                item_antrian.setTextAlignment(QtCore.Qt.AlignCenter)
                item_antrian.setFont(QtGui.QFont("Verdana", 8, QtGui.QFont.Bold))
                item_antrian.setFlags(item_antrian.flags() & ~QtCore.Qt.ItemIsEditable)
                
                item_status = QStandardItem(status)
                item_status.setTextAlignment(QtCore.Qt.AlignCenter)
                item_status.setFont(QtGui.QFont("Roboto", 10))
                item_status.setFlags(item_status.flags() & ~QtCore.Qt.ItemIsEditable)
                
                row_index = self.model.rowCount()
                self.model.setRowCount(row_index + 1)
                self.model.setItem(row_index, 0, item_jadwal)
                self.model.setItem(row_index, 1, item_antrian)
                self.model.setItem(row_index, 2, item_status)
                
                # Buat tombol "Detail" untuk masing-masing baris
                btn_detail = QtWidgets.QPushButton("Detail")
                btn_detail.setStyleSheet(
                    "QPushButton {"
                    "    border-radius: 4px;"
                    "    padding: 6px 10px;"
                    "    font-weight: bold;"
                    "    font-size: 8pt;"
                    "    min-width: 90px;"
                    "    border: none;"
                    "    background-color: #0cc0df;"
                    "    color: white;"
                    "}"
                    "QPushButton:hover {"
                    "    background-color: #5ce1e6;"
                    "}"
                )
                btn_detail.clicked.connect(lambda checked, r=riwayat: self.openDetail(r))
                index = self.model.index(row_index, 3)
                self.tableView.setIndexWidget(index, btn_detail)
                
        except Exception as e:
            print("Error membaca file JSON:", e)
            QtWidgets.QMessageBox.critical(self.dialog, "Error", f"Gagal memuat data: {str(e)}")
    
    def openDetail(self, riwayat):
        if not riwayat:
            print("Error: Data riwayat kosong!")
            return
        try:
            from WindowLihatDetail import Ui_Dialog as WindowLihatDetail
            self.dialogDetail = QtWidgets.QDialog()
            self.uiDetail = WindowLihatDetail(self.username)
            self.uiDetail.setupUi(self.dialogDetail)
            
            self.uiDetail.lineEdit_1.setText(riwayat.get("nama", "N/A"))
            self.uiDetail.lineEdit_2.setText(riwayat.get("dokter", "N/A"))
            self.uiDetail.lineEdit_3.setText(riwayat.get("jadwal", "N/A"))
            self.uiDetail.textEdit_4.setText(riwayat.get("keluhan", "N/A"))
            self.uiDetail.lineEdit_5.setText(riwayat.get("nomor antrian", "N/A"))
            
            self.uiDetail.lineEdit_1.setReadOnly(True)
            self.uiDetail.lineEdit_2.setReadOnly(True)
            self.uiDetail.lineEdit_3.setReadOnly(True)
            self.uiDetail.textEdit_4.setReadOnly(True)
            self.uiDetail.lineEdit_5.setReadOnly(True)
            
            self.uiDetail.pushButton_4.clicked.connect(self.closeDetail)
            
            self.dialogDetail.show()
        except Exception as e:
            print(f"Error saat membuka detail riwayat: {e}")
    
    def closeDetail(self):
        self.dialogDetail.close()
    
    def backToMenu(self):
        from WindowMenuUser import WindowMenuUser
        self.menu = WindowMenuUser(self.username)
        self.menu.show()
        self.dialog.close()
    
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Lihat Riwayat"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog("test")
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
