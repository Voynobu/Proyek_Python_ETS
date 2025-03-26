# WindowEditDokter.py
# Nama: Rangga Muhamad Fajar
# Kelas: 1A - D4
# NIM: 241524026
# Desc: - Program ini digunakan untuk mengelola dokter yang ada di rumah sakit.
#       - Admin dapat menambah dan menghapus dokter secara interaktif.

import json
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

class Ui_WindowEditDokter(object):
    def __init__(self, parent_window=None):
        # Simpan referensi ke window sebelumnya (parent window)
        self.parent_window = parent_window

    def setupUi(self, Dialog):
        self.dialog = Dialog  # Simpan referensi dialog agar bisa ditutup nanti
        Dialog.setObjectName("Dialog")
        Dialog.resize(1600, 900)
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # ------ LINE EDIT (Nama Dokter) ------
        self.lineEdit_1 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_1.setGeometry(QtCore.QRect(910, 401, 608, 51))
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
        self.lineEdit_1.setObjectName("lineEdit_1")
        self.lineEdit_1.setPlaceholderText("Masukkan Nama Dokter!")

        # ------ LINE EDIT (Spesialisasi Dokter) ------
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(910, 501, 608, 51))
        self.lineEdit_2.setStyleSheet(
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
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setPlaceholderText("Masukkan Spesialisasi Dokter!")

        # ------ BACK BUTTON (menggunakan HoverButton) ------
        self.pushButton_3 = HoverButton(Dialog, image_path="C:/ASSETS/BUTTON/BACK.png")
        self.pushButton_3.setGeometry(QtCore.QRect(10, 20, 111, 101))
        self.pushButton_3.setText("")
        self.pushButton_3.setObjectName("pushButton_3")
        # Hubungkan tombol back dengan fungsi untuk kembali ke window sebelumnya
        self.pushButton_3.clicked.connect(self.backToJadwalPoliDokter)

        # ------ BACKGROUND LABEL ------
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(-4, 0, 1611, 901))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("C:/ASSETS/BACKGROUND/11.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        # ------ TOMBOL TAMBAH DOKTER (menggunakan HoverButton) ------
        self.pushButton_1 = HoverButton(Dialog, image_path="C:/ASSETS/BUTTON/TAMBAH_DOKTER.png")
        self.pushButton_1.setGeometry(QtCore.QRect(891, 593, 648, 101))
        self.pushButton_1.setText("")
        self.pushButton_1.setObjectName("pushButton_1")

        # ------ TOMBOL HAPUS DOKTER (menggunakan HoverButton) ------
        self.pushButton_2 = HoverButton(Dialog, image_path="C:/ASSETS/BUTTON/HAPUS_DOKTER.png")
        self.pushButton_2.setGeometry(QtCore.QRect(891, 711, 648, 101))
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")

        # ------ COMBOBOX (Pilih Poli) ------
        self.comboBox_2 = QtWidgets.QComboBox(Dialog)
        self.comboBox_2.setGeometry(QtCore.QRect(910, 301, 608, 51))
        self.comboBox_2.setStyleSheet(
            "QComboBox {"
            "    color: black;"
            "    border: none;"
            "    border-bottom: 4px solid #a6a6a6;"
            "    font-size: 24px;"
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
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")

        # ------ TABLE VIEW ------
        self.tableView = QtWidgets.QTableView(Dialog)
        self.tableView.setGeometry(QtCore.QRect(81, 182, 641, 666))
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
        self.tableView.setObjectName("tableView")

        # Urutan tampilan: background di bawah, kemudian komponen lainnya
        self.label.raise_()
        self.lineEdit_1.raise_()
        self.lineEdit_2.raise_()
        self.pushButton_3.raise_()
        self.pushButton_1.raise_()
        self.pushButton_2.raise_()
        self.comboBox_2.raise_()
        self.tableView.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # ------ INIT MODEL & LOAD DATA ------
        self.initModel()
        self.loadData()

        # --- Nonaktifkan interaksi langsung pada tabel ---
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

        # Atur ukuran kolom: kolom pertama fixed, kolom kedua dan ketiga stretch
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        self.tableView.setColumnWidth(0, 70)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

    def initModel(self):
        # Inisialisasi model dengan 3 kolom: NO, NAMA DOKTER, SPESIALISASI
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["NO", "NAMA DOKTER", "SPESIALISASI"])
        self.tableView.setModel(self.model)

    def loadData(self):
        # Contoh: load data dari file JSON "dokter_data.json"
        file_path = "dokter_data.json"
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
            dokter_data = data.get("dokter", {})

            self.model.setRowCount(0)
            row_num = 0
            for dokter_name, spesialisasi in dokter_data.items():
                if dokter_name.strip():
                    item_no = QStandardItem(str(row_num + 1))
                    item_no.setTextAlignment(QtCore.Qt.AlignCenter)

                    item_dokter = QStandardItem(dokter_name.capitalize())
                    item_dokter.setTextAlignment(QtCore.Qt.AlignCenter)

                    item_spesialisasi = QStandardItem(str(spesialisasi))
                    item_spesialisasi.setTextAlignment(QtCore.Qt.AlignCenter)

                    self.model.appendRow([item_no, item_dokter, item_spesialisasi])
                    row_num += 1

        except Exception as e:
            print("Error membaca file JSON:", e)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Edit Dokter"))
        self.lineEdit_1.setText(_translate("Dialog", ""))
        self.lineEdit_2.setText(_translate("Dialog", ""))
        self.comboBox_2.setItemText(0, _translate("Dialog", "POLI JANTUNG"))
        self.comboBox_2.setItemText(1, _translate("Dialog", "POLI MATA"))
        self.comboBox_2.setItemText(2, _translate("Dialog", "POLI THT-KL"))
        self.comboBox_2.setItemText(3, _translate("Dialog", "POLI SARAF"))
        self.comboBox_2.setItemText(4, _translate("Dialog", "POLI ANAK"))

    def backToJadwalPoliDokter(self):
        """
        Metode ini akan dipanggil ketika tombol back diklik.
        Jika ada parent window (dalam hal ini window edit jadwal poli dokter), maka tampilkan kembali.
        Setelah itu, tutup dialog window edit dokter.
        """
        if self.parent_window:
            self.parent_window.show()
        self.dialog.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    # Untuk uji, jika tidak ada parent, bisa diset ke None
    ui = Ui_WindowEditDokter(parent_window=None)
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())