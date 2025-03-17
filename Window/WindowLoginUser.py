# WindowLoginUser.py
#Nama: Rangga Muhamad Fajar
#Kelas: 1A - D4
#NIM: 241524026
#Desc: - Tampilan login untuk user.
#      - Memeriksa username dan password dari file 'users.txt'.
#      - Jika berhasil, membuka MainWindow (halaman utama aplikasi).

from PyQt5 import QtCore, QtGui, QtWidgets
from daftarUser import login_user
import os

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1600, 900)
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        
        # Set background untuk login user
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(-4, 0, 1611, 901))
        self.label.setPixmap(QtGui.QPixmap("C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/LOGIN/BACKGROUND/3.png"))
        self.label.setScaledContents(True)
        
        # Field untuk Email
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
        self.lineEdit.setPlaceholderText("Masukkan Email Anda!")
        
        # Field untuk Password
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(200, 520, 521, 61))
        self.lineEdit_2.setStyleSheet("""
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
        self.lineEdit_2.setPlaceholderText("Masukkan Password Anda!")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        
        # Tombol untuk melihat password
        self.show_password_button = QtWidgets.QPushButton(Dialog)
        self.show_password_button.setGeometry(QtCore.QRect(676, 520, 61, 61))
        self.show_password_button.setStyleSheet("border: none;")
        self.show_password_button.setIcon(QtGui.QIcon("C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/BUTTON/BUTTON/EYE.png"))
        self.show_password_button.setIconSize(QtCore.QSize(40, 40))
        self.show_password_button.setCheckable(True)
        self.show_password_button.clicked.connect(self.toggle_password)
        
        # Tombol Login
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(330, 660, 251, 91))
        self.pushButton.setStyleSheet("border-image: url(C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/BUTTON/BUTTON/LOGIN.png);")
        self.add_hover_effect(self.pushButton)
        
        # Tombol Back
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 20, 111, 101))
        self.pushButton_2.setStyleSheet("border-image: url(C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/BUTTON/BUTTON/BACK.png);")
        self.add_hover_effect(self.pushButton_2)
        
        self.label.raise_()
        self.pushButton.raise_()
        self.lineEdit.raise_()
        self.lineEdit_2.raise_()
        self.show_password_button.raise_()
        self.pushButton_2.raise_()
        
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Login User"))
    
    def toggle_password(self):
        # Ubah mode tampilan password
        if self.show_password_button.isChecked():
            self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
    
    def add_hover_effect(self, button):
        # Efek hover untuk tombol
        effect = QtWidgets.QGraphicsOpacityEffect()
        button.setGraphicsEffect(effect)
        button.enterEvent = lambda event: effect.setOpacity(0.7)
        button.leaveEvent = lambda event: effect.setOpacity(1.0)

# Kelas pembungkus untuk WindowLoginUser
class WindowLoginUser(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        # Tombol Back kembali ke WindowWelcome
        self.ui.pushButton_2.clicked.connect(self.back_to_welcome)
        # Tombol Login melakukan proses verifikasi login
        self.ui.pushButton.clicked.connect(self.handle_login)
    
    def back_to_welcome(self):
        from WindowWelcome import WindowWelcome
        self.welcome = WindowWelcome()
        self.welcome.show()
        self.close()
    
    def handle_login(self):
        # Ambil input username dan password
        username = self.ui.lineEdit.text().strip()
        password = self.ui.lineEdit_2.text().strip()
        
        if not username or not password:
            QtWidgets.QMessageBox.warning(self, "Error", "Email dan Password harus diisi!")
        elif login_user(username,password) != "Login berhasil!":
            QtWidgets.QMessageBox.warning(self, "Error", login_user(username,password))
        else:
            QtWidgets.QMessageBox.information(self, "Sukses", "Login berhasil!")
            # Buka MainWindow sebagai halaman utama aplikasi
            from MainWindow import MainWindow
            self.main_win = MainWindow()
            self.main_win.show()
            self.close()    


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
