# main.py
from PyQt5 import QtWidgets, QtCore
import sys
from WindowSplashScreen import WindowSplashScreen

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 1600, 900)
        self.initUI()
    
    def initUI(self):
        label = QtWidgets.QLabel("Selamat Datang di Aplikasi!", self)
        label.setAlignment(QtCore.Qt.AlignCenter)
        self.setCentralWidget(label)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # Mulai dengan Splash Screen
    splash = WindowSplashScreen()
    splash.show()
    sys.exit(app.exec_())
