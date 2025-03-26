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
        self.lineEdit_1.setObjectName("lineEdit_1")
        self.lineEdit_1.setPlaceholderText("Masukkan Nama Poli! (Contoh: Umum)")

        # Gunakan HoverButton untuk tombol Back
        self.pushButton_3 = HoverButton(Dialog, image_path="C:/ASSETS/BUTTON/BACK.png")
        self.pushButton_3.setGeometry(QtCore.QRect(10, 20, 111, 101))
        self.pushButton_3.setText("")
        self.pushButton_3.setObjectName("pushButton_3")

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(-4, 0, 1611, 901))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("C:/ASSETS/BACKGROUND/10.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        # Gunakan HoverButton untuk tombol Tambah Poli
        self.pushButton_1 = HoverButton(Dialog, image_path="C:/ASSETS/BUTTON/TAMBAH_POLI.png")
        self.pushButton_1.setGeometry(QtCore.QRect(911, 547, 591, 87))
        self.pushButton_1.setText("")
        self.pushButton_1.setObjectName("pushButton_1")

        # Gunakan HoverButton untuk tombol Hapus Poli
        self.pushButton_2 = HoverButton(Dialog, image_path="C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/ASSETS/BUTTON/HAPUS_POLI.png")
        self.pushButton_2.setGeometry(QtCore.QRect(911, 663, 591, 87))
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")

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
        self.tableView.setObjectName("tableView")

        self.label.raise_()
        self.lineEdit_1.raise_()
        self.pushButton_3.raise_()
        self.pushButton_1.raise_()
        self.pushButton_2.raise_()
        self.tableView.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.initModel()
        self.loadData()

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

    def initModel(self):
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["NO", "NAMA POLI"])
        self.tableView.setModel(self.model)

    def loadData(self):
        file_path = "poliklinik_data.json"
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
            poliklinik_data = data.get("poliklinik", {})

            self.model.setRowCount(0)
            row_num = 0
            for poli_name in poliklinik_data.keys():
                if poli_name.strip():
                    item_no = QStandardItem(str(row_num + 1))
                    item_no.setTextAlignment(QtCore.Qt.AlignCenter)

                    item_poli = QStandardItem(poli_name.capitalize())
                    item_poli.setTextAlignment(QtCore.Qt.AlignCenter)

                    self.model.appendRow([item_no, item_poli])
                    row_num += 1

        except Exception as e:
            print("Error membaca file JSON:", e)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Splash Screen"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
