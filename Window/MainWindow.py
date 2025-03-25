# MainWindow.py
#Nama: Rangga Muhamad Fajar
#Kelas: 1A - D4
#NIM: 241524026

from PyQt5 import QtWidgets, QtCore
import sys
from WindowSplashScreen import WindowSplashScreen

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Set judul dan ukuran window utama
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 1600, 900)
        self.initUI()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # Mulai dengan menampilkan Splash Screen
    splash = WindowSplashScreen()
    splash.show()
    sys.exit(app.exec_())
