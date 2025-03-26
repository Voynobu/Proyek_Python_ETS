# WindowLoginUser.py
# Nama: Rangga Muhamad Fajar
# Kelas: 1A - D4
# NIM: 241524026
# Desc: - Tampilan login untuk user.
#       - Memeriksa username dan password dari file 'daftarUsers.json'.
#       - Jika berhasil, membuka WindowMenuUser sebagai halaman utama user.

from PyQt5 import QtCore, QtGui, QtWidgets
from Register import Register, login_user 
import os
from WindowMenuUser import WindowMenuUser

class HoverButton(QtWidgets.QPushButton):
    def __init__(self, parent=None, image_path=""):
        super().__init__(parent)
        self.opacity_effect = QtWidgets.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_animation = QtCore.QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_animation.setDuration(200)
        self.opacity_effect.setOpacity(1.0)
        self.image_path = image_path
        if image_path:
            self.setStyleSheet(f"QPushButton {{ border-image: url('{self.image_path}'); }}")
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
        
        # Set background untuk login user
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(-4, 0, 1611, 901))
        self.label.setPixmap(QtGui.QPixmap("C:/ASSETS/BACKGROUND/3.png"))
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
        self.lineEdit.setPlaceholderText("Masukkan Username Anda!")
        
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
        self.show_password_button.setIcon(QtGui.QIcon("C:/ASSETS/BUTTON/EYE.png"))
        self.show_password_button.setIconSize(QtCore.QSize(40, 40))
        self.show_password_button.setCheckable(True)
        self.show_password_button.clicked.connect(self.toggle_password)
        
        # Tombol Login (menggunakan HoverButton)
        self.pushButton = HoverButton(Dialog, image_path="C:/ASSETS/BUTTON/LOGIN.png")
        self.pushButton.setGeometry(QtCore.QRect(330, 660, 251, 91))
        
        # Tombol Back (menggunakan HoverButton)
        self.pushButton_2 = HoverButton(Dialog, image_path="C:/ASSETS/BUTTON/BACK.png")
        self.pushButton_2.setGeometry(QtCore.QRect(10, 20, 111, 101))
        
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
            QtWidgets.QMessageBox.warning(self, "Error", "Username dan Password harus diisi!")
        elif login_user(username, password) != "Login berhasil!":
            QtWidgets.QMessageBox.warning(self, "Error", login_user(username, password))
        else:
            QtWidgets.QMessageBox.information(self, "Sukses", "Login berhasil!")
            self.menu_user = WindowMenuUser(username)
            self.menu_user.show()
            self.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
