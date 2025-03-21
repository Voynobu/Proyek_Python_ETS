# WindowMenuAdmin.py
# Nama: Rangga Muhamad Fajar
# Kelas: 1A - D4
# NIM: 241524026
# Desc: - Tampilan menu utama bagi admin setelah berhasil login.
#       - Menampilkan tombol untuk mengedit poli dan dokter.

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
        button = QtWidgets.QPushButton(self)
        button.setGeometry(QtCore.QRect(x, y, width, height))
        button.setStyleSheet(f"border-image: url(C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/ASSETS/BUTTON/{image_name});")
        button.setText("")

        # Tambahkan efek hover dengan mengubah transparansi
        effect = QtWidgets.QGraphicsOpacityEffect()
        button.setGraphicsEffect(effect)

        def on_enter(event):
            effect.setOpacity(0.7)  # Kurangi opacity saat hover
        def on_leave(event):
            effect.setOpacity(1.0)  # Kembalikan opacity saat tidak hover

        button.enterEvent = on_enter
        button.leaveEvent = on_leave

        if action:
            button.clicked.connect(action)

        return button

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
