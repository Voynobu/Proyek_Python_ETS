# WindowRiwayat.py
# Nama: Rangga Muhamad Fajar dan Nauval Khairiyan
# Kelas: 1A - D4
# NIM: 241524026 dan 241524021
# Desc: - Program ini digunakan untuk melihat detail riwayat pendaftaran pasien di rumah sakit.

# WindowRiwayat.py
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
    def setupUi(self, Dialog, username):
        self.dialog = Dialog  # simpan referensi dialog untuk nanti digunakan di method backToMenu
        Dialog.setObjectName("Dialog")
        Dialog.resize(1598, 900)
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        
        # Tombol Back menggunakan HoverButton
        self.pushButton_3 = HoverButton(Dialog, image_path="C:/ASSETS/BUTTON/BACK.png")
        self.pushButton_3.setGeometry(QtCore.QRect(10, 20, 111, 101))
        self.pushButton_3.setText("")
        self.pushButton_3.setObjectName("pushButton_3")
        # Hubungkan tombol back ke method backToMenu
        self.pushButton_3.clicked.connect(self.backToMenu)
        
        # Background label
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(-4, 0, 1611, 901))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("C:/ASSETS/BACKGROUND/15.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        
        # Tabel untuk menampilkan data riwayat
        self.tableView = QtWidgets.QTableView(Dialog)
        self.tableView.setGeometry(QtCore.QRect(236, 210, 1110, 601))
        self.tableView.setStyleSheet(
            "QHeaderView::section {\n"
            "    background-color: #0cc0df; \n"
            "    color: white; \n"
            "    padding: 8px;\n"
            "}\n"
        )
        self.tableView.setObjectName("tableView")
        
        # Pastikan label (background) berada di bawah, kemudian tombol dan tabel
        self.label.raise_()
        self.pushButton_3.raise_()
        self.tableView.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
        # Inisialisasi model tabel dan load data (sesuaikan dengan kebutuhan Anda)
        self.initModel()
        self.loadData()
        self.username = username

    def initModel(self):
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["NAMA PASIEN", "POLI", "DOKTER", "JADWAL", "TANGGAL TEMU", "STATUS"])
        self.tableView.setModel(self.model)
    
    def loadData(self):
        file_path = "data/riwayat.json"
    
        try:
            with open(file_path, "r") as file:
                riwayat_data = json.load(file)

            today = QtCore.QDate.currentDate()
            self.model.setRowCount(0)

            for username, records in riwayat_data.items():
                for entry in records:
                    nama = entry.get("nama", "Unknown")
                    poli = entry.get("poli", "Unknown")
                    dokter = entry.get("dokter", "Unknown")
                    jadwal = entry.get("jadwal", "Unknown")
                    tanggal_temu = entry.get("tanggal_temu", "Unknown")
                    status = entry.get("status", "Ongoing")  # Default: Ongoing

                    # Hitung status berdasarkan tanggal temu
                    try:
                        temu_date = QtCore.QDate.fromString(tanggal_temu, "dd-MM-yyyy")
                        if temu_date.isValid():
                            if temu_date < today:
                                status = "Finished"
                            elif temu_date > today:
                                status = "On going"
                        else:
                            status = "Invalid Date"
                    except ValueError:
                        status = "Invalid Date"

                    # Simpan status terbaru ke riwayat.json
                    entry["status"] = status

                    # Buat item tabel
                    item_nama = QStandardItem(nama)
                    item_poli = QStandardItem(poli)
                    item_dokter = QStandardItem(dokter)
                    item_jadwal = QStandardItem(jadwal)
                    item_tanggal = QStandardItem(tanggal_temu)
                    item_status = QStandardItem(status)

                    # Tambahkan ke model tabel
                    self.model.appendRow([item_nama, item_poli, item_dokter, item_jadwal, item_tanggal, item_status])

                    # Simpan perubahan status ke riwayat.json
                    with open(file_path, "w") as file:
                        json.dump(riwayat_data, file, indent=4)

        except Exception as e:
            print("Error membaca file JSON:", e)

    
    def backToMenu(self):
        # Import dan buka WindowMenuUser ketika tombol back diklik
        from WindowMenuUser import WindowMenuUser
        self.menu = WindowMenuUser(self.username)  # Anda dapat mengganti "test" dengan username yang sesuai
        self.menu.show()
        self.dialog.close()
    
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Lihat Riwayat"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog, "test")
    Dialog.show()
    sys.exit(app.exec_())
