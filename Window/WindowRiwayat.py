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
    def __init__(self, username):
        self.username = username  # Simpan username untuk digunakan nanti

    def setupUi(self, Dialog):
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

    def initModel(self):
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Jadwal Check-Up", "Nomor Antrian", "Status", "Lihat Detail"])
        self.tableView.setModel(self.model)

        # Mengatur font header kolom
        header = self.tableView.horizontalHeader()
        header.setFont(QtGui.QFont("Arial", 15, QtGui.QFont.Bold))  # Gaya font header

        # Menyesuaikan ukuran kolom agar sesuai dengan isi data
        self.tableView.resizeColumnsToContents()  # Sesuaikan lebar kolom dengan isi
    
    def loadData(self):
        file_path = "Data/riwayat.json"
        try:
            with open(file_path, "r") as file:
                data = json.load(file)

            if not isinstance(data, dict):  # Pastikan format JSON benar
                data = {}
            
            # Ambil username pengguna yang login
            username_login = self.username  

            for nama, riwayat_list in data.items():
                if nama == username_login: # Filter berdasarkan username login
                    for riwayat in riwayat_list:
                        tanggal_temu = riwayat.get("tanggal_temu", "N/A")
                        jadwal = riwayat.get("jadwal", "N/A")
                        nomor_antrian = riwayat.get("nomor antrian", "N/A")
                        status = riwayat.get("status", "N/A")

                        # Format teks dengan font tebal dan menarik
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

                        # Tambahkan baris baru tanpa menghapus data lama
                        row_index = self.model.rowCount()
                        self.model.setRowCount(row_index + 1)

                        self.model.setItem(row_index, 0, item_jadwal)
                        self.model.setItem(row_index, 1, item_antrian)
                        self.model.setItem(row_index, 2, item_status)

                        # Buat tombol "Detail"
                        btn_detail = QtWidgets.QPushButton("Detail")
                        btn_detail.setStyleSheet(
                            "QPushButton { background-color: #5ce1e6; color: black; font-weight: bold; padding: 5px; }"
                            "QPushButton:hover { background-color: #3caea3; color: white; }"
                        )
                        btn_detail.clicked.connect(lambda checked, r=riwayat: self.openDetail(r))

                        # Masukkan tombol ke dalam tabel
                        index = self.model.index(row_index, 3)
                        self.tableView.setIndexWidget(index, btn_detail)

        except Exception as e:
            print("Error membaca file JSON:", e)
            data = {}

    def openDetail(self, riwayat):
        if not riwayat:
            print("Error: Data riwayat kosong!")
            return

        try:
            # Menambahkan impor dan pembukaan window detail
            from WindowLihatDetail import Ui_Dialog as WindowLihatDetail
            self.dialogDetail = QtWidgets.QDialog()

            # Buat objek Ui_Dialog dengan username sebagai parameter
            self.uiDetail = WindowLihatDetail(self.username)  

            # Panggil setupUi TANPA username
            self.uiDetail.setupUi(self.dialogDetail)

            # Masukkan data riwayat ke dalam field di WindowLihatDetail
            self.uiDetail.lineEdit_1.setText(riwayat.get("nama", "N/A"))
            self.uiDetail.lineEdit_2.setText(riwayat.get("dokter", "N/A"))
            self.uiDetail.lineEdit_3.setText(riwayat.get("jadwal", "N/A"))
            self.uiDetail.textEdit_4.setText(riwayat.get("keluhan", "N/A"))
            self.uiDetail.lineEdit_5.setText(riwayat.get("nomor antrian", "N/A"))

            # Set lineEdit fields to read-only to prevent editing
            self.uiDetail.lineEdit_1.setReadOnly(True)
            self.uiDetail.lineEdit_2.setReadOnly(True)
            self.uiDetail.lineEdit_3.setReadOnly(True)
            self.uiDetail.textEdit_4.setReadOnly(True)
            self.uiDetail.lineEdit_5.setReadOnly(True)

            # Tambahkan fungsi untuk tombol "Back"
            self.uiDetail.pushButton_4.clicked.connect(self.closeDetail)

            # Tampilkan detail dialog
            self.dialogDetail.show()

        except ImportError as e:
            print(f"Error saat mengimpor WindowLihatDetail: {e}")
        except Exception as e:
            print(f"Error saat membuka detail riwayat: {e}")

    def closeDetail(self):
        # Menutup dialog detail dan kembali ke window sebelumnya
        self.dialogDetail.close()

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
    ui = Ui_Dialog("test")
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
