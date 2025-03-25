# WindowMenuAdmin.py
# Nama: Rangga Muhamad Fajar
# Kelas: 1A - D4
# NIM: 241524026
# Desc: - Program ini merupakan antarmuka utama menu admin untuk sistem pendaftaran rumah sakit.
#       - Program menampilkan tombol-tombol interaktif untuk mengelola jadwal, poli, dokter dan data admin.

#Nama : Muhamad Dino Dermawan
#Nim  : 241524015
#Desc : 

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from PyQt5.QtCore import QPropertyAnimation
from WindowTambahAdmin import Ui_WindowTambahAdmin

class Ui_WindowMenuAdmin(object):
    def setupUi(self, windowMenuAdmin):
        self.windowMenuAdmin = windowMenuAdmin
        windowMenuAdmin.setObjectName("windowMenuAdmin")
        windowMenuAdmin.resize(1600, 900)
        windowMenuAdmin.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)

        self.centralwidget = QtWidgets.QWidget(windowMenuAdmin)
        self.centralwidget.setObjectName("centralwidget")

        # Background
        self.background = QtWidgets.QLabel(self.centralwidget)
        self.background.setGeometry(QtCore.QRect(0, 0, 1600, 900))
        self.background.setPixmap(QtGui.QPixmap(
            "C:/ASSETS/BACKGROUND/6.png"))
        self.background.setScaledContents(True)

        # Tombol Edit Poli
        self.menu1_btn = QtWidgets.QPushButton(self.centralwidget)
        self.menu1_btn.setGeometry(QtCore.QRect(688, 201, 870, 311))
        self.menu1_btn.setStyleSheet("border-image: url(C:/ASSETS/BUTTON/EDIT_JADWAL_POLI.png);")
        self.menu1_btn.setText("")

        # Tombol Tambah Admin
        self.menu2_btn = QtWidgets.QPushButton(self.centralwidget)
        self.menu2_btn.setGeometry(QtCore.QRect(699, 528, 850, 301))
        self.menu2_btn.setStyleSheet("border-image: url(C:/ASSETS/BUTTON/TAMBAH_ADMIN.png);")
        self.menu2_btn.setText("")
        self.menu2_btn.clicked.connect(self.bukaWindowTambahAdmin)

        # Tombol Kembali
        self.btn_kembali = QtWidgets.QPushButton(self.centralwidget)
        self.btn_kembali.setGeometry(QtCore.QRect(10, 20, 111, 101))
        self.btn_kembali.setStyleSheet("border: none; background: transparent;")
        icon_back = QtGui.QIcon("C:/ASSETS/BUTTON/BACK.png")
        self.btn_kembali.setIcon(icon_back)
        self.btn_kembali.setIconSize(QtCore.QSize(111, 101))
        self.btn_kembali.clicked.connect(self.kembali_ke_login)

        windowMenuAdmin.setCentralWidget(self.centralwidget)
        self.retranslateUi(windowMenuAdmin)
        QtCore.QMetaObject.connectSlotsByName(windowMenuAdmin)

        # Fade Animation
        self.fade_effect = QGraphicsOpacityEffect()
        windowMenuAdmin.setGraphicsEffect(self.fade_effect)
        self.fade_animation = QPropertyAnimation(self.fade_effect, b"opacity")
        self.fade_animation.setDuration(600)
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.start()

    def retranslateUi(self, windowMenuAdmin):
        _translate = QtCore.QCoreApplication.translate
        windowMenuAdmin.setWindowTitle(_translate("windowMenuAdmin", "Menu Admin"))

    def bukaWindowTambahAdmin(self):
        # Hide the current window
        self.windowMenuAdmin.hide()
        
        # Create and show the tambah admin window
        self.windowTambahAdmin = QtWidgets.QMainWindow()
        self.ui_tambah = Ui_WindowTambahAdmin(parent_window=self)
        self.ui_tambah.setupUi(self.windowTambahAdmin)
        self.windowTambahAdmin.show()

    def enableWindow(self):
        self.windowMenuAdmin.show()

    def kembali_ke_login(self):
        from WindowLoginAdmin import WindowLoginAdmin
        self.windowLoginAdmin = WindowLoginAdmin()
        self.windowLoginAdmin.show()
        self.windowMenuAdmin.close()


class WindowMenuAdmin(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_WindowMenuAdmin()
        self.ui.setupUi(self)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    windowMenuAdmin = QtWidgets.QMainWindow()
    ui = Ui_WindowMenuAdmin()
    ui.setupUi(windowMenuAdmin)
    windowMenuAdmin.show()
    sys.exit(app.exec_())
