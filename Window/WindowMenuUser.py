# WindowMenuUser.py
# Nama: Rangga Muhamad Fajar
# Kelas: 1A - D4
# NIM: 241524026
# Desc: - Program ini berfungsi sebagai menu utama bagi pengguna 
#         untuk mengakses fitur riwayat kunjungan, 
#         melakukan pendaftaran pasien, melihat daftar poli, dan 
#         membatalkan pendaftaran dalam sistem rumah sakit.

# WindowMenuUser.py
from PyQt5 import QtCore, QtGui, QtWidgets

class HoverButton(QtWidgets.QPushButton):
    def __init__(self, parent=None, image_path=""):
        super().__init__(parent)
        self.opacity_effect = QtWidgets.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1.0)
        self.opacity_animation = QtCore.QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_animation.setDuration(200)
        self.image_path = image_path
        if image_path:
            self.setStyleSheet(f"QPushButton {{ border-image: url({image_path}); }}")
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

class WindowMenuUser(QtWidgets.QDialog):
    def __init__(self, username):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # Hilangkan border window
        self.setFixedSize(1600, 900)
        self.username = username
        self.initUI()
        self.oldPos = None  # Untuk mendukung dragging window

    def initUI(self):
        # Background
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(-4, 0, 1611, 901))
        self.label.setPixmap(QtGui.QPixmap("C:/ASSETS/BACKGROUND/5.png"))
        self.label.setScaledContents(True)

        # Tombol-tombol dengan efek hover
        self.pushButton = self.create_button(1012, 170, 557, 328, "PENDAFTARAN.png")
        self.pushButton.clicked.connect(self.open_Pendaftaran)

        self.pushButton_3 = self.create_button(686, 171, 331, 329, "RIWAYAT.png")
        self.pushButton_3.clicked.connect(self.open_Riwayat)

        self.pushButton_4 = self.create_button(673, 514, 512, 337, "LIHAT_POLI.png")
        self.pushButton_4.clicked.connect(self.open_LihatPoli)
        
        self.pushButton_5 = self.create_button(1166, 520, 404, 329, "BATAL_DAFTAR.png")
        self.pushButton_5.clicked.connect(self.open_Cancel)
        
        self.pushButton_2 = self.create_button(10, 20, 111, 101, "BACK.png", self.back_to_login)

    def create_button(self, x, y, width, height, image_name, action=None):
        image_path = f"C:/ASSETS/BUTTON/{image_name}"
        button = HoverButton(self, image_path=image_path)
        button.setGeometry(QtCore.QRect(x, y, width, height))
        button.setText("")
        if action:
            button.clicked.connect(action)
        return button

    def back_to_login(self):
        from WindowLoginUser import WindowLoginUser
        self.login_win = WindowLoginUser()
        self.login_win.show()
        self.close()

    def open_Riwayat(self):
        from WindowRiwayat import Ui_Dialog  # Pastikan nama file dan class sesuai
        self.riwayat_dialog = QtWidgets.QDialog()
        self.ui_riwayat = Ui_Dialog()
        self.ui_riwayat.setupUi(self.riwayat_dialog)
        self.riwayat_dialog.show()
        self.close()

    def open_Pendaftaran(self):
        from WindowPendaftaranPasien import WindowPendaftaranPasien
        self.pendaftaran_window = WindowPendaftaranPasien(self.username)
        self.pendaftaran_window.show()
        self.close()

    def open_LihatPoli(self):
        from WindowLihatDaftarPoliUser import Ui_Dialog  # Pastikan nama class dan path sudah benar
        self.dialog = QtWidgets.QDialog()
        self.ui_lihat = Ui_Dialog()
        self.ui_lihat.setupUi(self.dialog)
        self.dialog.show()
        self.close()
        
    
    def open_Cancel(self):
        from WindowCancel import Ui_Dialog as CancelUi
        self.cancel_dialog = QtWidgets.QDialog()
        self.cancel_ui = CancelUi()
        self.cancel_ui.setupUi(self.cancel_dialog)
        self.cancel_dialog.show()
        self.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = WindowMenuUser("test")
    window.show()
    sys.exit(app.exec_())
