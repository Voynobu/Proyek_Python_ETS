# WindowLihatDaftarPoliUser.py
# Nama: Rangga Muhamad Fajar
# Kelas: 1A - D4
# NIM: 241524026
# Desc: - Program ini digunakan untuk melihat daftar poli di rumah sakit.

# Nama : Muhamad Dino Dermawan
# Nim  : 241524015
# - Menghubungkan dengan file JadwalPoli.json kemudian menampilkannya menjadi tabel
# - Auto refresh system, memantau perubahan file Jadwalpoli.json agar merubah isi tabel seusai dengan perubahan isi file

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
        self.json_file = "JadwalPoli.json"
        self.last_modified = 0
        self.setupAutoRefresh()

    def setupAutoRefresh(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.checkFileChanges)
        self.timer.start(1000)

    def checkFileChanges(self):
        try:
            modified = os.path.getmtime(self.json_file)
            if modified > self.last_modified:
                self.last_modified = modified
                self.loadData()
        except Exception as e:
            print(f"Error checking file changes: {e}")

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1600, 900)
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # Tombol Kembali
        self.pushButton_3 = HoverButton(Dialog, image_path="C:/ASSETS/BUTTON/BACK.png")
        self.pushButton_3.setGeometry(QtCore.QRect(10, 20, 111, 101))
        self.pushButton_3.setText("")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.backToMenu)
        
        # Background
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(-4, 0, 1611, 901))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("C:/ASSETS/BACKGROUND/14.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        
        # Tabel View dengan pengaturan untuk teks lengkap
        self.tableView = QtWidgets.QTableView(Dialog)
        self.tableView.setGeometry(QtCore.QRect(30, 120, 1540, 740))
        self.tableView.setStyleSheet(
            """
            QTableView {
                gridline-color: gray;
                font-size: 16px;
                background-color: white;
                border: 2px solid #0cc0df;
            }
            QHeaderView::section {
                background-color: #0cc0df; 
                color: white; 
                padding: 12px;
                font-weight: bold;
                font-size: 18px;
                border: none;
            }
            QTableView::item {
                padding: 8px;
            }
            """
        )
        self.tableView.setObjectName("tableView")
        
        # Pengaturan untuk mencegah teks terpotong
        self.tableView.setWordWrap(True)
        self.tableView.setTextElideMode(QtCore.Qt.ElideNone)
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.verticalHeader().setDefaultSectionSize(60)
        
        # Konfigurasi tabel
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tableView.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tableView.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)
        self.tableView.setShowGrid(True)
        
        self.label.raise_()
        self.pushButton_3.raise_()
        self.tableView.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.initModel()
        self.loadData()
        
    def backToMenu(self):
        from WindowMenuUser import WindowMenuUser
        self.menu = WindowMenuUser("test")
        self.menu.show()
        self.dialog = self.pushButton_3.parent()
        self.dialog.close()
        self.timer.stop()
        
    def initModel(self):
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels([
            "NO", 
            "NAMA POLI", 
            "KUOTA", 
            "DOKTER", 
            "SPESIALISASI", 
            "JADWAL PRAKTEK", 
            "STATUS"
        ])
        self.tableView.setModel(self.model)
        
        # Atur lebar kolom dan resize mode
        header = self.tableView.horizontalHeader()
        self.tableView.setColumnWidth(0, 60)    # NO
        self.tableView.setColumnWidth(1, 200)   # NAMA POLI
        self.tableView.setColumnWidth(2, 80)    # KUOTA
        self.tableView.setColumnWidth(3, 220)   # DOKTER
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)  # SPESIALISASI
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)  # JADWAL PRAKTEK
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.Stretch)  # STATUS
    
    def loadData(self):
        try:
            with open(self.json_file, "r", encoding='utf-8') as file:
                data = json.load(file)
            
            self.model.setRowCount(0)
            row_count = 0
            
            for poli in data.get("daftar_poli", []):
                nama_poli = poli.get("nama_poli", "")
                kuota = str(poli.get("kuota", ""))
                
                for dokter in poli.get("dokter_list", []):
                    nama_dokter = dokter.get("nama", "")
                    spesialisasi = dokter.get("spesialis", "")
                    
                    # Kumpulkan semua jadwal
                    jadwal_list = []
                    status_list = []
                    
                    for jadwal in poli.get("jadwal_list", []):
                        if jadwal.get("dokter", "") == nama_dokter:
                            jadwal_str = f"{jadwal.get('hari', '')} {jadwal.get('jam_awal', '')}-{jadwal.get('jam_akhir', '')}"
                            jadwal_list.append(jadwal_str)
                            status_list.append(jadwal.get("status", ""))
                    
                    if jadwal_list:
                        row_count += 1
                        self.addTableRow(
                            row_count,
                            nama_poli,
                            kuota,
                            nama_dokter,
                            spesialisasi,
                            "\n".join(jadwal_list),
                            "\n".join(status_list)
                        )
            
            # Sesuaikan tinggi baris
            self.adjustRowHeights()
            self.last_modified = os.path.getmtime(self.json_file)
            
        except Exception as e:
            print(f"Error loading data: {e}")
            QtWidgets.QMessageBox.critical(None, "Error", f"Gagal memuat data: {str(e)}")

    def adjustRowHeights(self):
        for row in range(self.model.rowCount()):
            self.tableView.resizeRowToContents(row)
    
    def addTableRow(self, no, poli, kuota, dokter, spesialis, jadwal, status):
        items = [
            QStandardItem(str(no)),
            QStandardItem(poli),
            QStandardItem(kuota),
            QStandardItem(dokter),
            QStandardItem(spesialis),
            QStandardItem(jadwal),
            QStandardItem(status)
        ]
        
        for item in items:
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            font = QtGui.QFont()
            font.setPointSize(14)
            item.setFont(font)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            item.setToolTip(item.text())  # Tooltip untuk teks lengkap
            
        self.model.appendRow(items)
    
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Lihat Daftar Poli (Tampilan Lengkap)"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
