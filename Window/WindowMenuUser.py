from PyQt5 import QtCore, QtGui, QtWidgets

class WindowMenuUser(QtWidgets.QDialog):
    def __init__(self, username):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # Menghilangkan border window
        self.setFixedSize(1600, 900)
        self.initUI()
        self.oldPos = None  # Untuk mendukung dragging window
        self.username = username

    def initUI(self):
        # Background
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(-4, 0, 1611, 901))
        self.label.setPixmap(QtGui.QPixmap("C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/LOGIN/BACKGROUND/5.png"))
        self.label.setScaledContents(True)

        # Tombol-tombol dengan efek hover
        self.pushButton = self.create_button(1012, 170, 557, 328, "PENDAFTARAN.png")
        self.pushButton.clicked.connect(self.open_pendaftaran)
        self.pushButton_3 = self.create_button(686, 171, 331, 329, "RIWAYAT.png")
        self.pushButton_4 = self.create_button(673, 514, 512, 337, "LIHAT_POLI.png")
        self.pushButton_5 = self.create_button(1166, 520, 404, 329, "BATAL_DAFTAR.png")
        self.pushButton_2 = self.create_button(10, 20, 111, 101, "BACK.png", self.back_to_login)

    def create_button(self, x, y, width, height, image_name, action=None):
        """
        Membuat tombol dengan efek hover.
        """
        button = QtWidgets.QPushButton(self)
        button.setGeometry(QtCore.QRect(x, y, width, height))
        button.setStyleSheet(f"border-image: url(C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/ASSETS/BUTTON/{image_name});")
        button.setText("")

        # Tambahkan efek hover
        self.add_hover_effect(button)

        if action:
            button.clicked.connect(action)

        return button

    def add_hover_effect(self, button):
        """
        Menambahkan efek hover pada tombol.
        """
        button.enterEvent = lambda event: self.set_button_opacity(button, 0.7)  # Saat cursor masuk
        button.leaveEvent = lambda event: self.set_button_opacity(button, 1.0)  # Saat cursor keluar

    def set_button_opacity(self, button, opacity):
        """
        Mengatur opacity tombol.
        """
        effect = QtWidgets.QGraphicsOpacityEffect(button)
        effect.setOpacity(opacity)
        button.setGraphicsEffect(effect)

    def back_to_login(self):
        """Fungsi kembali ke halaman login user."""
        from WindowLoginUser import WindowLoginUser
        self.login_win = WindowLoginUser()
        self.login_win.show()
        self.close()

    def open_pendaftaran(self):
        from WindowPendaftaranPasien import WindowPendaftaranPasien
        self.pendaftaran_window = WindowPendaftaranPasien(self.username)
        self.pendaftaran_window.show()
        self.close()
        
    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = WindowMenuUser("test")
    window.show()
    sys.exit(app.exec_())