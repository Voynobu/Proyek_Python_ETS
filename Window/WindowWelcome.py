# window_welcome.py
#Nama: Rangga Muhamad Fajar
#Kelas: 1A - D4
#NIM: 241524026
# WindowWelcome.py
#Desc: - Pembuatan window welcome sebagai tampilan awal aplikasi.
#      - Terdapat 4 tombol untuk mengarah ke masing-masing window.
#      - Tombol Sign Up, Login Admin, Login User, dan Exit.

from PyQt5 import QtCore, QtGui, QtWidgets
import os

class WindowWelcome(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        self.setFixedSize(1600, 900)
        self.setupUi(self)
    
    def setupUi(self, Dialog):
        Dialog.setObjectName("WindowWelcome")
        Dialog.resize(1600, 900)
        
        # Background
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(0, 0, 1600, 900))
        self.load_image(self.label, "C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/LOGIN/BACKGROUND/1.png")
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        
        # Tombol Sign Up
        self.pushButton = self.create_button(Dialog, 210, 700, 431, 121,
                                            "C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/LOGIN/BUTTON_LOGIN/3.png")
        # Tombol Login Admin
        self.pushButton_2 = self.create_button(Dialog, 210, 550, 431, 121,
                                            "C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/LOGIN/BUTTON_LOGIN/1.png")
        # Tombol Login User (untuk membuka Main Window)
        self.pushButton_3 = self.create_button(Dialog, 210, 440, 431, 121,
                                            "C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/LOGIN/BUTTON_LOGIN/2.png")
        # Tombol Exit (X)
        self.pushButton_4 = self.create_button(Dialog, 1500, 20, 91, 101,
                                            "C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/LOGIN/BUTTON_LOGIN/4.png")
        self.pushButton_4.clicked.connect(Dialog.close)
        
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    
    def create_button(self, parent, x, y, width, height, image_path):
        button = QtWidgets.QPushButton(parent)
        button.setGeometry(QtCore.QRect(x, y, width, height))
        self.load_image(button, image_path)
        button.setObjectName("pushButton")
        
        # Efek opasitas untuk hover
        effect = QtWidgets.QGraphicsOpacityEffect()
        button.setGraphicsEffect(effect)
        button.enterEvent = lambda event: effect.setOpacity(0.7)
        button.leaveEvent = lambda event: effect.setOpacity(1.0)
        
        # Jika tombol yang memuat gambar login user, hubungkan ke fungsi open_main_window
        if "BUTTON_LOGIN/2.png" in image_path:
            button.clicked.connect(self.open_main_window)
        
        return button
    
    def load_image(self, widget, image_path):
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
    
    def open_main_window(self):
        from main import MainWindow  # Mengimpor MainWindow di sini untuk menghindari circular import
        self.main_win = MainWindow()
        self.main_win.show()
        self.close()
