# WindowEditJadwalPoliDokter.py
# Nama: Rangga Muhamad Fajar
# Kelas: 1A - D4
# NIM: 241524026
# Desc: Program ini menampilkan dan mengatur jadwal layanan poli beserta dokter di rumah sakit.
#       Admin dapat melihat, menambah, mengubah, dan menghapus jadwal dokter (termasuk status dan kuota).
#       Tabel menampilkan informasi lengkap: nomor, poli, dokter (spesialisasi), jadwal, status, serta kuota.

import sys
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
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1600, 900)
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # ------ BACK BUTTON ------
        self.pushButton_4 = HoverButton(Dialog, image_path="C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/ASSETS/BUTTON/BACK.png")
        self.pushButton_4.setGeometry(QtCore.QRect(10, 20, 111, 101))
        self.pushButton_4.setText("")
        self.pushButton_4.setObjectName("pushButton_4")

        # ------ BACKGROUND LABEL ------
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(-4, 0, 1611, 901))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("C:/ASSETS/BACKGROUND/12.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        # ------ BUTTON EDIT JADWAL ------
        self.pushButton_1 = HoverButton(Dialog, image_path="C:/ASSETS/BUTTON/EDIT_JADWAL.png")
        self.pushButton_1.setGeometry(QtCore.QRect(-2, 219, 411, 201))
        self.pushButton_1.setText("")
        self.pushButton_1.setObjectName("pushButton_1")

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

        # ------ BUTTON EDIT POLI ------
        self.pushButton_2 = HoverButton(Dialog, image_path="C:/ASSETS/BUTTON/EDIT_POLI.png")
        self.pushButton_2.setGeometry(QtCore.QRect(-2, 444, 411, 201))
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")

        # ------ BUTTON EDIT DOKTER ------
        self.pushButton_3 = HoverButton(Dialog, image_path="C:/ASSETS/BUTTON/EDIT_DOK.png")
        self.pushButton_3.setGeometry(QtCore.QRect(-7, 669, 421, 201))
        self.pushButton_3.setText("")
        self.pushButton_3.setObjectName("pushButton_3")

        # ------ LABEL DATETIME (Tanpa Background) ------
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

        # Z-order: pastikan background berada di bawah
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

        # Sembunyikan header vertikal
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.setShowGrid(True)

        # Atur header & baris
        header = self.tableView.horizontalHeader()
        header.setSectionsMovable(False)
        header.setDefaultAlignment(QtCore.Qt.AlignCenter)
        header.setFixedHeight(100)
        self.tableView.verticalHeader().setDefaultSectionSize(100)

        # Ukuran kolom (6 kolom)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        self.tableView.setColumnWidth(0, 50)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)

        # Contoh data
        self.loadData()

        # Timer update waktu
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
        data_list = [
            ("1", "POLI JANTUNG", "Dr. Asep (Kardiolog)", "TUESDAY (08:00 - 12:00)\nFRIDAY (10:00 - 13:00)", "AVAILABLE", "20"),
            ("2", "POLI MATA", "Dr. Messi (Spesialis THT-KL)", "MONDAY (10:00 - 15:00)\nTHURSDAY (07:00 - 12:00)", "UNAVAILABLE", "15"),
            ("3", "POLI SARAF", "Dr. Rafi (Pediatric Gawat Darurat)", "TUESDAY (08:00 - 12:00)\nWEDNESDAY (18:00 - 20:00)", "AVAILABLE", "20"),
            ("4", "POLI ANAK", "Dr. Rehan (Spesialis Anak)", "THURSDAY (10:00 - 12:00)", "UNAVAILABLE", "20"),
        ]
        self.model.setRowCount(0)
        for row_data in data_list:
            items = []
            for value in row_data:
                item = QStandardItem(str(value))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                items.append(item)
            self.model.appendRow(items)

    def updateDateTime(self):
        now = QtCore.QDateTime.currentDateTime()
        day_of_week = now.toString("dddd").upper()      # Contoh: TUESDAY
        date_str    = now.toString("yyyy-MM-dd")         # Contoh: 2025-03-13
        time_str    = now.toString("HH:mm:ss")           # Contoh: 10:44:51
        self.label_datetime.setText(f"{day_of_week} | {date_str} | {time_str}")

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Window Edit Jadwal Poli Dokter"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
