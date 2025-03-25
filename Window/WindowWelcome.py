# WindowWelcome.py
#Nama: Rangga Muhamad Fajar
#Kelas: 1A - D4
#NIM: 241524026
#Desc: - Pembuatan window welcome sebagai tampilan awal aplikasi.
#      - Menampilkan 4 tombol untuk mengarahkan ke window Sign Up, Login Admin, Login User, dan Exit.

from PyQt5 import QtCore, QtGui, QtWidgets
import os

class HoverButton(QtWidgets.QPushButton):
    def __init__(self, parent=None, image_path=""):
        super().__init__(parent)
        self.effect = QtWidgets.QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.effect)
        self.effect.setOpacity(1.0)  # default opacity
        self.image_path = image_path
        self.setStyleSheet(f"QPushButton {{ border-image: url('{self.image_path}'); }}")
        self.setMouseTracking(True)  # aktifkan mouse tracking agar enterEvent berfungsi

    def enterEvent(self, event):
        self.effect.setOpacity(0.7)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.effect.setOpacity(1.0)
        super().leaveEvent(event)


class WindowWelcome(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        # Hilangkan frame window untuk tampilan custom
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        self.setFixedSize(1600, 900)
        self.setupUi(self)
    
    def setupUi(self, Dialog):
        Dialog.setObjectName("WindowWelcome")
        Dialog.resize(1600, 900)
        
        # Set background window welcome
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(0, 0, 1600, 900))
        self.load_image(self.label, "C:/ASSETS/BACKGROUND/1.png")
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        
        # Tombol Sign Up (gambar BUTTON_LOGIN/3.png)
        self.pushButton = self.create_button(Dialog, 210, 700, 431, 121,
                                            "C:/ASSETS/BUTTON/SIGN_UP_PJ.png")
        # Tombol Login Admin (gambar BUTTON_LOGIN/2.png)
        self.pushButton_2 = self.create_button(Dialog, 210, 550, 431, 121,
                                            "C:/ASSETS/BUTTON/LOGIN_AS_ADMIN.png")
        # Tombol Login User (gambar BUTTON_LOGIN/1.png)
        self.pushButton_3 = self.create_button(Dialog, 210, 440, 431, 121,
                                            "C:/ASSETS/BUTTON/LOGIN_AS_USER.png")
        # Tombol Exit
        self.pushButton_4 = self.create_button(Dialog, 1500, 20, 91, 101,
                                            "C:/ASSETS/BUTTON/CLOSEAPP.png")
        self.pushButton_4.clicked.connect(Dialog.close)
        
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    
    def create_button(self, parent, x, y, width, height, image_path):
        button = HoverButton(parent, image_path=image_path)
        button.setGeometry(QtCore.QRect(x, y, width, height))
        
        # Tentukan fungsi klik berdasarkan gambar tombol
        if "BUTTON/LOGIN_AS_USER.png" in image_path:
            button.clicked.connect(self.open_login_user)
        elif "BUTTON/LOGIN_AS_ADMIN.png" in image_path:
            button.clicked.connect(self.open_login_admin)
        elif "BUTTON/SIGN_UP_PJ.png" in image_path:
            button.clicked.connect(self.open_sign_up_window)
        
        return button

    
    def load_image(self, widget, image_path):
        # Muat gambar jika file ditemukan, atur style untuk tombol jika bukan label
        if os.path.exists(image_path):
            pixmap = QtGui.QPixmap(image_path)
            if isinstance(widget, QtWidgets.QLabel):
                widget.setPixmap(pixmap)
            else:
                widget.setStyleSheet(f"QPushButton {{ border-image: url('{image_path}'); }}")
            print(f"Loaded image: {image_path}")
        else:
            print(f"Error: Image not found -> {image_path}")
    
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("WindowWelcome", "Login"))
    
    def open_login_admin(self):
        from WindowLoginAdmin import WindowLoginAdmin
        self.login_admin_win = WindowLoginAdmin()
        self.login_admin_win.show()
        self.close()
    
    def open_login_user(self):
        from WindowLoginUser import WindowLoginUser
        self.login_user_win = WindowLoginUser()
        self.login_user_win.show()
        self.close()
    
    def open_sign_up_window(self):
        from WindowSignUp import WindowSignUp
        self.sign_up_win = WindowSignUp()
        self.sign_up_win.show()
        self.close()
