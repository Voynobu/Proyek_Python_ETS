#Nama: Rangga Muhamad Fajar
#Kelas: 1A - D4
#NIM: 241524026
# window_splash.py
#Desc: - Pembuatan splash screen sebagai tampilan awal aplikasi.
#      - Splash screen akan menampilkan gambar selama 3 detik sebelum masuk ke WindowWelcome.

from PyQt5 import QtCore, QtGui, QtWidgets
import os
from WindowWelcome import WindowWelcome

class WindowSplashScreen(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setFixedSize(1600, 900)
        
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(0, 0, 1600, 900)
        self.load_image(self.label, "C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/LOGIN/1.png")
        self.label.setScaledContents(True)
        
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.show_welcome_window)
        self.timer.start(3000)
    
    def load_image(self, widget, image_path):
        if os.path.exists(image_path):
            pixmap = QtGui.QPixmap(image_path)
            widget.setPixmap(pixmap)
            print(f"Loaded splash image: {image_path}")
        else:
            print(f"Error: Splash image not found -> {image_path}")
    
    def show_welcome_window(self):
        self.timer.stop()
        self.welcome = WindowWelcome()
        self.welcome.show()
        self.close()
