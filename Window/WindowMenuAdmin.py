# WindowMenuAdmin.py
# Nama: Rangga Muhamad Fajar
# Kelas: 1A - D4
# NIM: 241524026
# Desc: - Program ini merupakan antarmuka utama menu admin untuk sistem pendaftaran rumah sakit.
#       - Program menampilkan tombol-tombol interaktif untuk mengelola jadwal, poli, dokter dan data admin.

#Nama : Muhamad Dino Dermawan
#Nim  : 241524015
#Desc : 

# WindowMenuAdmin.py
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from PyQt5.QtCore import QPropertyAnimation
from WindowTambahAdmin import Ui_WindowTambahAdmin

class HoverButton(QtWidgets.QPushButton):
    def __init__(self, parent=None, image_path=""):
        super().__init__(parent)
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1.0)
        self.opacity_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_animation.setDuration(200)
        if image_path:
            self.setStyleSheet(f"QPushButton {{ border-image: url('{image_path}'); background: transparent; border: none; }}")
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
        self.background.setPixmap(QtGui.QPixmap("C:/ASSETS/BACKGROUND/6.png"))
        self.background.setScaledContents(True)

        # Tombol Edit Jadwal Poli (Menggunakan HoverButton)
        self.menu1_btn = HoverButton(self.centralwidget, image_path="C:/ASSETS/BUTTON/EDIT_JADWAL_POLI.png")
        self.menu1_btn.setGeometry(QtCore.QRect(688, 201, 860, 311))
        self.menu1_btn.setText("")
        self.menu1_btn.clicked.connect(self.openEditJadwalPoliDokter)

        # Tombol Tambah Admin (Menggunakan HoverButton)
        self.menu2_btn = HoverButton(self.centralwidget, image_path="C:/ASSETS/BUTTON/TAMBAH_ADMIN.png")
        self.menu2_btn.setGeometry(QtCore.QRect(699, 528, 840, 301))
        self.menu2_btn.setText("")
        self.menu2_btn.clicked.connect(self.bukaWindowTambahAdmin)

        # Tombol Kembali (Menggunakan HoverButton)
        self.btn_kembali = HoverButton(self.centralwidget, image_path="C:/ASSETS/BUTTON/BACK.png")
        self.btn_kembali.setGeometry(QtCore.QRect(10, 20, 111, 101))
        self.btn_kembali.setIconSize(QtCore.QSize(111, 101))
        self.btn_kembali.clicked.connect(self.kembali_ke_login)

        windowMenuAdmin.setCentralWidget(self.centralwidget)
        self.retranslateUi(windowMenuAdmin)
        QtCore.QMetaObject.connectSlotsByName(windowMenuAdmin)

    def retranslateUi(self, windowMenuAdmin):
        _translate = QtCore.QCoreApplication.translate
        windowMenuAdmin.setWindowTitle(_translate("windowMenuAdmin", "Menu Admin"))

    def bukaWindowTambahAdmin(self):
        self.windowMenuAdmin.hide()
        from WindowTambahAdmin import Ui_WindowTambahAdmin
        self.windowTambahAdmin = QtWidgets.QMainWindow()
        self.ui_tambah = Ui_WindowTambahAdmin(parent_window=self.windowMenuAdmin)
        self.ui_tambah.setupUi(self.windowTambahAdmin)
        self.windowTambahAdmin.show()

    def openEditJadwalPoliDokter(self):
        self.windowMenuAdmin.hide()
        from WindowEditJadwalPoliDokter import Ui_Dialog
        self.edit_jadwal_dialog = QtWidgets.QDialog()
        # Kirim parent_window sebagai self.windowMenuAdmin agar nanti bisa kembali ke menu admin
        self.ui_edit = Ui_Dialog(parent_window=self.windowMenuAdmin)
        self.ui_edit.setupUi(self.edit_jadwal_dialog)
        self.edit_jadwal_dialog.show()

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
    def enableWindow(self):
        self.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    windowMenuAdmin = WindowMenuAdmin()
    windowMenuAdmin.show()
    sys.exit(app.exec_())
