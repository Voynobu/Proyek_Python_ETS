# WindowSignUp.py
#Nama: Rangga Muhamad Fajar
#Kelas: 1A - D4
#NIM: 241524026
#Desc: - Tampilan sign-up untuk user baru.
#      - Menyediakan form untuk input nama, email, dan password.
#      - Data user disimpan ke file 'users.txt'.

from PyQt5 import QtCore, QtGui, QtWidgets
from Register import register_user 
import os

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1600, 900)
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        
        # Atur background sign-up
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(-4, 0, 1611, 901))
        self.label.setPixmap(QtGui.QPixmap("C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/ASSETS/BACKGROUND/4.png"))
        self.label.setScaledContents(True)
        
        # Field untuk Nama
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(200, 390, 521, 61))
        self.lineEdit.setStyleSheet("""
            QLineEdit {
                color: black;
                border: none;
                border-bottom: 4px solid #a6a6a6;
                font-size: 20px;
            }
            QLineEdit:focus {   
                border-bottom: 4px solid #ffbd59;
            }
        """)
        self.lineEdit.setPlaceholderText("Masukkan Username Anda!")

        
        # Field untuk Password
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(200, 520, 521, 61))
        self.lineEdit_3.setStyleSheet("""
            QLineEdit {
                color: black;
                border: none;
                border-bottom: 4px solid #a6a6a6;
                font-size: 20px;
            }
            QLineEdit:focus {
                border-bottom: 4px solid #ffbd59;
            }
        """)
        self.lineEdit_3.setPlaceholderText("Masukkan Password Anda!")
        self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password)
        
        # Tombol untuk melihat password
        self.show_password_button = QtWidgets.QPushButton(Dialog)
        self.show_password_button.setGeometry(QtCore.QRect(676, 520, 61, 61))
        self.show_password_button.setStyleSheet("border: none;")
        self.show_password_button.setIcon(QtGui.QIcon("C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/BUTTON/BUTTON/EYE.png"))
        self.show_password_button.setIconSize(QtCore.QSize(30, 30))
        self.show_password_button.setCheckable(True)
        self.show_password_button.clicked.connect(self.toggle_password_visibility)
        
        # Tombol Sign Up
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(330, 620, 251, 91))
        self.pushButton.setStyleSheet("border-image: url(C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/BUTTON/BUTTON/SIGN_UP_PD.png);")
        self.add_hover_effect(self.pushButton)
        
        # Tombol Back
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 20, 111, 101))
        self.pushButton_2.setStyleSheet("border-image: url(C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/BUTTON/BUTTON/BACK.png);")
        self.add_hover_effect(self.pushButton_2)
        
        # Atur urutan tampilan widget
        self.label.raise_()
        self.pushButton.raise_()
        self.pushButton_2.raise_()
        self.lineEdit.raise_()
        self.lineEdit_3.raise_()
        self.show_password_button.raise_()
        
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Sign Up"))
    
    def toggle_password_visibility(self):
        # Ubah mode echo untuk menampilkan atau menyembunyikan password
        if self.show_password_button.isChecked():
            self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password)
    
    def add_hover_effect(self, button):
        # Tambahkan efek hover pada tombol
        button.enterEvent = lambda event: self.set_button_opacity(button, 0.7)
        button.leaveEvent = lambda event: self.set_button_opacity(button, 1.0)

    def set_button_opacity(self, button, opacity):
        # Terapkan efek opacity pada tombol
        effect = QtWidgets.QGraphicsOpacityEffect(button)
        effect.setOpacity(opacity)
        button.setGraphicsEffect(effect)
# Kelas pembungkus untuk WindowSignUp
class WindowSignUp(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        # Hubungkan tombol Back untuk kembali ke WindowWelcome
        self.ui.pushButton_2.clicked.connect(self.back_to_welcome)
        # Hubungkan tombol Sign Up untuk mendaftarkan user
        self.ui.pushButton.clicked.connect(self.handle_register)
    
    def back_to_welcome(self):
        from WindowWelcome import WindowWelcome
        self.welcome = WindowWelcome()
        self.welcome.show()
        self.close()
    
    def handle_register(self):
        # Ambil data input user
        name = self.ui.lineEdit.text().strip()
        password = self.ui.lineEdit_3.text().strip()

        if not name or not password:
            QtWidgets.QMessageBox.warning(self, "Error", "Semua field harus diisi!")
        elif register_user(name, password) != "Registrasi berhasil!":
            QtWidgets.QMessageBox.warning(self, "Error", register_user(name, password))
        else:
            QtWidgets.QMessageBox.information(self, "Sukses", "Pendaftaran berhasil! Silakan login.")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())