# WindowLoginAdmin.py
# Nama: Rangga Muhamad Fajar
# Kelas: 1A - D4
# NIM: 241524026
# Desc: - Tampilan login untuk admin.
#       - Memeriksa email dan password dan jika berhasil membuka MainWindow.
#
# Nama : Muhamad Dino Dermawan
# Nim : 241524015
# Desc :  - Menghubungkan ke WindowMenuAdmin 
#         - Validasi username & password

from PyQt5 import QtCore, QtGui, QtWidgets
import json
import os
import sys
from WindowMenuAdmin import Ui_WindowMenuAdmin
from Utils.SoundManager import SoundManager
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
    def setupUi(self, windowLoginAdmin):
        SoundManager.play("interface")
        windowLoginAdmin.setObjectName("windowLoginAdmin")
        windowLoginAdmin.resize(1600, 900)
        windowLoginAdmin.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # Background
        self.label = QtWidgets.QLabel(windowLoginAdmin)
        self.label.setGeometry(QtCore.QRect(-4, 0, 1611, 901))
        self.label.setPixmap(QtGui.QPixmap("C:/ASSETS/BACKGROUND/2.png"))
        self.label.setScaledContents(True)

        # Username field
        self.lineEdit = QtWidgets.QLineEdit(windowLoginAdmin)
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
        self.lineEdit.setPlaceholderText("Masukkan Username!")

        # Password field
        self.lineEdit_2 = QtWidgets.QLineEdit(windowLoginAdmin)
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

        # Show password button
        self.show_password_button = QtWidgets.QPushButton(windowLoginAdmin)
        self.show_password_button.setGeometry(QtCore.QRect(676, 520, 61, 61))
        self.show_password_button.setStyleSheet("border: none;")
        self.show_password_button.setIcon(QtGui.QIcon("C:/ASSETS/BUTTON/EYE.png"))
        self.show_password_button.setIconSize(QtCore.QSize(40, 40))
        self.show_password_button.setCheckable(True)
        self.show_password_button.clicked.connect(self.toggle_password)

        # Login Button (menggunakan HoverButton)
        self.pushButton = HoverButton(windowLoginAdmin, image_path="C:/ASSETS/BUTTON/LOGIN.png")
        self.pushButton.setGeometry(QtCore.QRect(330, 660, 251, 91))
        self.pushButton.clicked.connect(lambda: self.login(windowLoginAdmin))

        # Back Button (menggunakan HoverButton)
        self.pushButton_2 = HoverButton(windowLoginAdmin, image_path="C:/ASSETS/BUTTON/BACK.png")
        self.pushButton_2.setGeometry(QtCore.QRect(10, 20, 111, 101))
        self.pushButton_2.clicked.connect(windowLoginAdmin.close)

        # Raise all elements
        self.label.raise_()
        self.pushButton.raise_()
        self.lineEdit.raise_()
        self.lineEdit_2.raise_()
        self.show_password_button.raise_()
        self.pushButton_2.raise_()

        self.retranslateUi(windowLoginAdmin)
        QtCore.QMetaObject.connectSlotsByName(windowLoginAdmin)

    def retranslateUi(self, windowLoginAdmin):
        _translate = QtCore.QCoreApplication.translate
        windowLoginAdmin.setWindowTitle(_translate("windowLoginAdmin", "Login Admin"))

    def toggle_password(self):
        if self.show_password_button.isChecked():
            self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)

    def login(self, window):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()

        if self.cek_login(username, password):
            self.open_window_menu_admin(window)
        else:
            QtWidgets.QMessageBox.warning(None, "Login Gagal", "Username atau password salah.")

    def cek_login(self, username, password):
        if not os.path.exists("admins.json"):
            data = {"admins": [{"username": "AdminRumahSakit", "password": "RumahAdminSakit"}]}
            with open("admins.json", "w") as file:
                json.dump(data, file)

        with open("admins.json", "r") as file:
            data = json.load(file)

        for admin in data["admins"]:
            if admin["username"] == username and admin["password"] == password:
                return True
        return False

    def open_window_menu_admin(self, current_window):
        try:
            # Hide the current login window
            current_window.hide()
            
            # Create and show the menu admin window
            self.menu_admin_window = QtWidgets.QMainWindow()
            self.ui_menu_admin = Ui_WindowMenuAdmin()
            self.ui_menu_admin.setupUi(self.menu_admin_window)
            self.menu_admin_window.show()
            
        except Exception as e:
            print(f"Error: {e}")
            # If error occurs, show the login window again
            current_window.show()

class WindowLoginAdmin(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        from WindowWelcome import WindowWelcome
        self.ui.pushButton_2.clicked.connect(self.back_to_welcome)
    
    def back_to_welcome(self):
        from WindowWelcome import WindowWelcome
        self.welcome = WindowWelcome()
        self.welcome.show()
        self.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_Dialog()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
