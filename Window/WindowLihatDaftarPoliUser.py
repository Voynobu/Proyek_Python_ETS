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
import datetime
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
        self.timer.timeout.connect(self.checkFileAndTimeChanges)
        self.timer.start(1000)

    def checkFileAndTimeChanges(self):
        try:
            modified = os.path.getmtime(self.json_file)
            if modified > self.last_modified:
                self.last_modified = modified
                self.loadData()
            else:
                self.updateStatuses()
        except Exception as e:
            print(f"Error checking file changes: {e}")

    def checkScheduleStatus(self, jadwal_list):
        now = datetime.datetime.now()
        current_day = now.strftime("%A")
        current_time = now.time()
        
        status_list = []
        
        for jadwal in jadwal_list:
            schedule_day = jadwal.get("hari", "")
            
            if schedule_day.lower() != current_day.lower():
                status_list.append("UNAVAILABLE")
                continue
                
            try:
                start_time = datetime.datetime.strptime(jadwal.get("jam_awal", "00:00"), "%H:%M").time()
                end_time = datetime.datetime.strptime(jadwal.get("jam_akhir", "00:00"), "%H:%M").time()
                
                if start_time <= current_time <= end_time:
                    status_list.append("AVAILABLE")
                else:
                    status_list.append("UNAVAILABLE")
            except Exception as e:
                print(f"Error parsing time: {e}")
                status_list.append("UNAVAILABLE")
        
        return status_list

    def updateStatuses(self):
        try:
            with open(self.json_file, "r", encoding='utf-8') as file:
                data = json.load(file)
            
            row_index = 0
            for poli in data.get("daftar_poli", []):
                for dokter in poli.get("dokter_list", []):
                    nama_dokter = dokter.get("nama", "")
                    jadwal_list = []
                    
                    for jadwal in poli.get("jadwal_list", []):
                        if jadwal.get("dokter", "") == nama_dokter:
                            jadwal_list.append(jadwal)
                    
                    if jadwal_list:
                        status_list = self.checkScheduleStatus(jadwal_list)
                        status_item = QStandardItem("\n".join(status_list))
                        status_item.setTextAlignment(QtCore.Qt.AlignCenter)
                        font = QtGui.QFont()
                        font.setPointSize(14)
                        status_item.setFont(font)
                        status_item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.model.setItem(row_index, 6, status_item)
                        row_index += 1
            
        except Exception as e:
            print(f"Error updating statuses: {e}")

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
        self.tableView.setColumnWidth(0, 60)
        self.tableView.setColumnWidth(1, 200)
        self.tableView.setColumnWidth(2, 80)
        self.tableView.setColumnWidth(3, 220)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.Stretch)
    
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
                    jadwal_details = []
                    
                    for jadwal in poli.get("jadwal_list", []):
                        if jadwal.get("dokter", "") == nama_dokter:
                            jadwal_str = f"{jadwal.get('hari', '')} {jadwal.get('jam_awal', '')}-{jadwal.get('jam_akhir', '')}"
                            jadwal_list.append(jadwal)
                            jadwal_details.append(jadwal_str)
                    
                    if jadwal_list:
                        row_count += 1
                        status_list = self.checkScheduleStatus(jadwal_list)
                        self.addTableRow(
                            row_count,
                            nama_poli,
                            kuota,
                            nama_dokter,
                            spesialisasi,
                            "\n".join(jadwal_details),
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
            item.setToolTip(item.text())
            
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