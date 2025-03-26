# WindowLihatDaftarPoliUser.py
# Nama: Rangga Muhamad Fajar
# Kelas: 1A - D4
# NIM: 241524026
# Desc: - Program ini digunakan untuk melihat daftar poli di rumah sakit.

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
        Dialog.resize(1598, 900)
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        
        # Tombol Back menggunakan HoverButton
        self.pushButton_3 = HoverButton(Dialog, image_path="C:/ASSETS/BUTTON/BACK.png")
        self.pushButton_3.setGeometry(QtCore.QRect(10, 20, 111, 101))
        self.pushButton_3.setText("")
        self.pushButton_3.setObjectName("pushButton_3")
        
        # Background
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(-4, 0, 1611, 901))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("C:/ASSETS/BACKGROUND/16.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        
        # Tabel untuk menampilkan data poli
        self.tableView = QtWidgets.QTableView(Dialog)
        self.tableView.setGeometry(QtCore.QRect(124, 210, 1359, 602))
        self.tableView.setStyleSheet(
            "QHeaderView::section {\n"
            "    background-color: #0cc0df; \n"
            "    color: white; \n"
            "    padding: 8px;\n"
            "}"
        )
        self.tableView.setObjectName("tableView")
        
        # Pastikan tampilan tombol dan tabel berada di atas background
        self.label.raise_()
        self.pushButton_3.raise_()
        self.tableView.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
        # Inisialisasi model tabel dan load data (misalnya, dari file JSON)
        self.initModel()
        self.loadData()
        
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
        Dialog.setWindowTitle(_translate("Dialog", "Lihat Daftar Poli"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
