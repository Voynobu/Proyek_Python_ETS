# WindowEditJadwalPoliDokter.py
# Nama: Rangga Muhamad Fajar
# Kelas: 1A - D4
# NIM: 241524026
# Desc: Program ini menampilkan dan mengatur jadwal layanan poli beserta dokter di rumah sakit.
#       Admin dapat melihat, menambah, mengubah, dan menghapus jadwal dokter (termasuk status dan kuota).
#       Tabel menampilkan informasi lengkap: nomor, poli, dokter (spesialisasi), jadwal, status, serta kuota.

import sys
import json
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
            self.setStyleSheet(f"QPushButton {{ border-image: url('{image_path}'); background: transparent; border: none; }}")
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
        self.dialog = Dialog  # Simpan referensi dialog
        Dialog.setObjectName("Dialog")
        Dialog.resize(1600, 900)
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # ------ BACK BUTTON ------
        self.pushButton_4 = HoverButton(Dialog, image_path="C:/ASSETS/BUTTON/BACK.png")
        self.pushButton_4.setGeometry(QtCore.QRect(10, 20, 111, 101))
        self.pushButton_4.setText("")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.backToMenuAdmin)

        # ------ BACKGROUND LABEL ------
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(-4, 0, 1611, 901))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("C:/ASSETS/BACKGROUND/12.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        # ------ TABLE VIEW ------
        self.tableView = QtWidgets.QTableView(Dialog)
        self.tableView.setGeometry(QtCore.QRect(440, 170, 1131, 696))
        self.tableView.setStyleSheet(
            """
            QTableView {
                gridline-color: gray;
                font-size: 20px;
            }
            QHeaderView::section {
                background-color: #0cc0df; 
                color: white;
                padding: 8px;
                font-weight: bold;
                font-size: 20px;
            }
            """
        )
        self.tableView.setObjectName("tableView")

        # ------ BUTTON EDIT JADWAL ------
        self.pushButton_1 = HoverButton(Dialog, image_path="C:/ASSETS/BUTTON/EDIT_JADWAL.png")
        self.pushButton_1.setGeometry(QtCore.QRect(-2, 219, 411, 201))
        self.pushButton_1.setText("")
        self.pushButton_1.setObjectName("pushButton_1")
        self.pushButton_1.clicked.connect(self.openEditJadwal)

        # ------ BUTTON EDIT POLI ------
        self.pushButton_2 = HoverButton(Dialog, image_path="C:/ASSETS/BUTTON/EDIT_POLI.png")
        self.pushButton_2.setGeometry(QtCore.QRect(-2, 444, 411, 201))
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.openEditPoli)

        # ------ BUTTON EDIT DOKTER ------
        self.pushButton_3 = HoverButton(Dialog, image_path="C:/ASSETS/BUTTON/EDIT_DOK.png")
        self.pushButton_3.setGeometry(QtCore.QRect(-7, 669, 421, 201))
        self.pushButton_3.setText("")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.openEditDokter)

        # ------ LABEL DATETIME ------
        self.label_datetime = QtWidgets.QLabel(Dialog)
        self.label_datetime.setGeometry(QtCore.QRect(431, 36, 691, 96))
        self.label_datetime.setAlignment(QtCore.Qt.AlignCenter)
        self.label_datetime.setStyleSheet(
            """
            QLabel {
                color: #12c2e8;
                font-size: 30px;
                font-weight: bold;
            }
            """
        )
        self.label_datetime.setObjectName("label_datetime")

        # Z-order: pastikan background di bawah
        self.label.raise_()
        self.pushButton_4.raise_()
        self.pushButton_1.raise_()
        self.tableView.raise_()
        self.pushButton_2.raise_()
        self.pushButton_3.raise_()
        self.label_datetime.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # ------ INIT TABEL ------
        self.initTable()

        # Nonaktifkan interaksi tabel
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
        self.tableView.setColumnWidth(0, 50)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)

        self.loadData()

        self.timer = QtCore.QTimer(Dialog)
        self.timer.timeout.connect(self.updateDateTime)
        self.timer.start(1000)
        self.updateDateTime()

    def initTable(self):
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels([
            "NO", "POLI", "DOKTER", "JADWAL", "STATUS", "KUOTA"
        ])
        self.tableView.setModel(self.model)

    def loadData(self):
        try:
            with open("JadwalPoli.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                self.model.setRowCount(0)
                
                for idx, poli in enumerate(data["daftar_poli"], start=1):
                    nama_poli = poli["nama_poli"].upper()
                    kuota = str(poli.get("kuota", "N/A"))
                    
                    # Format dokter
                    dokter_str = "\n".join([
                        f"{dokter['nama']} ({dokter['spesialis']})" 
                        for dokter in poli["dokter_list"]
                    ])
                    
                    # Format jadwal dan status
                    jadwal_entries = []
                    status_entries = []
                    for jadwal in poli["jadwal_list"]:
                        hari = jadwal["hari"].upper()
                        jam = f"{jadwal['jam_awal']} - {jadwal['jam_akhir']}"
                        jadwal_entries.append(f"{hari} ({jam})")
                        status_entries.append(jadwal.get("status", "N/A").upper())
                    
                    jadwal_str = "\n".join(jadwal_entries)
                    status_str = "\n".join(status_entries)
                    
                    # Tambahkan baris ke tabel
                    row_data = [
                        str(idx), 
                        nama_poli, 
                        dokter_str, 
                        jadwal_str, 
                        status_str, 
                        kuota
                    ]
                    
                    items = []
                    for value in row_data:
                        item = QStandardItem(str(value))
                        item.setTextAlignment(QtCore.Qt.AlignCenter)
                        items.append(item)
                    self.model.appendRow(items)
                    
        except Exception as e:
            print(f"Error loading JSON data: {e}")
            # Fallback data jika file tidak ditemukan
            self.loadFallbackData()

    def loadFallbackData(self):
        fallback_data = [
            ("1", "POLI JANTUNG", "Dr. Asep (Kardiolog)", "TUESDAY (08:00 - 12:00)\nFRIDAY (13:00 - 18:00)", "AVAILABLE\nAVAILABLE", "20"),
            ("2", "POLI MATA", "Dr. Ahmad (Oftalmolog)", "MONDAY (09:00 - 15:00)\nTHURSDAY (07:00 - 12:00)", "AVAILABLE\nUNAVAILABLE", "15"),
            ("3", "POLI THT-KL", "Dr. Messi (Spesialis THT-KH)", "TUESDAY (11:00 - 18:00)\nWEDNESDAY (18:00 - 21:00)", "AVAILABLE\nAVAILABLE", "25"),
            ("4", "POLI SARAF", "Dr. Jajang (Neurolog)", "TUESDAY (08:00 - 13:00)\nSUNDAY (10:00 - 17:00)", "AVAILABLE\nUNAVAILABLE", "18"),
            ("5", "POLI ANAK", "Dr.Radhit (Pediatrik Gawat Darurat)", "THURSDAY (10:00 - 17:00)", "AVAILABLE", "30")
        ]
        self.model.setRowCount(0)
        for row_data in fallback_data:
            items = []
            for value in row_data:
                item = QStandardItem(str(value))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                items.append(item)
            self.model.appendRow(items)

    def updateDateTime(self):
        now = QtCore.QDateTime.currentDateTime()
        day_of_week = now.toString("dddd").upper()
        date_str    = now.toString("yyyy-MM-dd")
        time_str    = now.toString("HH:mm:ss")
        self.label_datetime.setText(f"{day_of_week} | {date_str} | {time_str}")

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Window Edit Jadwal Poli Dokter"))

    def openEditJadwal(self):
        self.dialog.hide()
        from WindowEditJadwal import Ui_Dialog as Ui_WindowEditJadwal
        self.edit_jadwal_dialog = QtWidgets.QDialog()
        self.ui_edit_jadwal = Ui_WindowEditJadwal(parent_window=self.dialog)
        self.ui_edit_jadwal.setupUi(self.edit_jadwal_dialog)
        self.edit_jadwal_dialog.show()

    def openEditPoli(self):
        self.dialog.hide()
        from WindowEditPoli import Ui_Dialog as Ui_WindowEditPoli
        self.edit_poli_dialog = QtWidgets.QDialog()
        self.ui_edit_poli = Ui_WindowEditPoli(parent_window=self.dialog)
        self.ui_edit_poli.setupUi(self.edit_poli_dialog)
        self.edit_poli_dialog.show()

    def openEditDokter(self):
        self.dialog.hide()
        from WindowEditDokter import Ui_WindowEditDokter
        self.edit_dokter_dialog = QtWidgets.QDialog()
        self.ui_edit_dokter = Ui_WindowEditDokter(parent_window=self.dialog)
        self.ui_edit_dokter.setupUi(self.edit_dokter_dialog)
        self.edit_dokter_dialog.show()

    def backToMenuAdmin(self):
        if self.parent_window:
            self.parent_window.show()
        self.dialog.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    # Untuk uji, jika tidak ada parent, bisa diset ke None
    ui = Ui_Dialog(parent_window=None)
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())