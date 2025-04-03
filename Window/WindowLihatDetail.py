# WindowLihatDetail.py
# Nama: Rangga Muhamad Fajar & Nauval Khairiyan
# Kelas: 1A - D4
# NIM: 241524026 / 241524021
# Desc: - Program ini berfungsi untuk melihat resi hasil pendaftaran, window ini letaknya ada di WindowRiwayat.

import sys
from PyQt5 import QtCore, QtGui, QtWidgets

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
        Dialog.setObjectName("Dialog")
        Dialog.resize(1600, 900)
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # QLineEdit untuk menampilkan resi pendaftaran
        self.lineEdit_1 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_1.setGeometry(QtCore.QRect(392, 488, 399, 65))
        self.lineEdit_1.setStyleSheet(
            "QLineEdit {"
            "    background-color: white;"
            "    border-radius: 20px;"
            "    border: 4px solid #5ce1e6;"
            "    padding: 10px;"
            "    font-size: 20px;"
            "}"
        )
        self.lineEdit_1.setText("")
        self.lineEdit_1.setObjectName("lineEdit_1")
        
        # Tombol Back dengan HoverButton
        self.pushButton_4 = HoverButton(Dialog, image_path="C:/ASSETS/BUTTON/BACK.png")
        self.pushButton_4.setGeometry(QtCore.QRect(10, 20, 111, 101))
        self.pushButton_4.setText("")
        self.pushButton_4.setObjectName("pushButton_4")
        
        # Background
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(-4, 0, 1611, 901))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("C:/ASSETS/BACKGROUND/13.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(392, 614, 399, 65))
        self.lineEdit_2.setStyleSheet(
            "QLineEdit {"
            "    background-color: white;"
            "    border-radius: 20px;"
            "    border: 4px solid #5ce1e6;"
            "    padding: 10px;"
            "    font-size: 20px;"
            "}"
        )
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(392, 740, 399, 65))
        self.lineEdit_3.setStyleSheet(
            "QLineEdit {"
            "    background-color: white;"
            "    border-radius: 20px;"
            "    border: 4px solid #5ce1e6;"
            "    padding: 10px;"
            "    font-size: 20px;"
            "}"
        )
        self.lineEdit_3.setText("")
        self.lineEdit_3.setObjectName("lineEdit_3")
        
        self.lineEdit_4 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_4.setGeometry(QtCore.QRect(814, 488, 373, 317))
        self.lineEdit_4.setStyleSheet(
            "QLineEdit {"
            "    background-color: white;"
            "    border-radius: 20px;"
            "    border: 4px solid #5ce1e6;"
            "    padding: 10px;"
            "    font-size: 15px;"
            "}"
        )
        self.lineEdit_4.setText("")
        self.lineEdit_4.setObjectName("lineEdit_4")
        
        self.lineEdit_5 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_5.setGeometry(QtCore.QRect(596, 350, 391, 51))
        self.lineEdit_5.setStyleSheet(
            "QLineEdit {"
            "    color: black; "
            "    border: none; "
            "    border-bottom: 4px solid #ffbd59; "
            "    font-size: 25px;"
            "}"
            "QLineEdit:focus {"
            "    border-bottom: 4px solid #a6a6a6;"
            "}"
        )
        self.lineEdit_5.setText("")
        self.lineEdit_5.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_5.setObjectName("lineEdit_5")
        
        # Atur z-order (pastikan background di bawah)
        self.label.raise_()
        self.pushButton_4.raise_()
        self.lineEdit_1.raise_()
        self.lineEdit_2.raise_()
        self.lineEdit_3.raise_()
        self.lineEdit_4.raise_()
        self.lineEdit_5.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Lihat Detail Resi Pendaftaran"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(dialog)
    dialog.exec_()  # Gunakan exec_() agar hanya menampilkan dialog tanpa menutup aplikasi utama

