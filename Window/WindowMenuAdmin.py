from PyQt5 import QtCore, QtGui, QtWidgets

class WindowMenuAdmin(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # Menghilangkan border window
        self.setFixedSize(1600, 900)
        self.initUI()
        self.oldPos = None  # Untuk mendukung dragging window

    def initUI(self):
        # Background
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(-4, 0, 1611, 901))
        self.label.setPixmap(QtGui.QPixmap("C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/ASSETS/BACKGROUND/6.png"))
        self.label.setScaledContents(True)

        # Tombol-tombol dengan efek hover
        self.pushButton = self.create_button(688, 201, 870, 311, "EDIT_JADWAL_POLI.png")
        self.pushButton_3 = self.create_button(699, 528, 850, 301, "TAMBAH_ADMIN.png")
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
        """Fungsi kembali ke halaman login admin."""
        from WindowLoginAdmin import WindowLoginAdmin
        self.login_admin_win = WindowLoginAdmin()
        self.login_admin_win.show()
        self.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = WindowMenuAdmin()
    window.show()
    sys.exit(app.exec_())