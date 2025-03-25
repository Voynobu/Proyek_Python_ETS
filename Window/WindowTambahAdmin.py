# WindowTambahAdmin.py
# Nama: Rangga Muhamad Fajar
# Kelas: 1A - D4
# NIM: 241524026
# Desc: - Tampilan login untuk user.
#       - Memeriksa username dan password dari file 'daftarUsers.json'.
#       - Jika berhasil, membuka WindowMenuUser sebagai halaman utama user.

#Nama : Muhamad Dino Dermawan
#Nim  : 241526015

from PyQt5 import QtCore, QtGui, QtWidgets
import json
import os

class Ui_WindowTambahAdmin(object):
    def __init__(self, parent_window=None):
        self.parent_window = parent_window

    def setupUi(self, windowTambahAdmin):
        self.windowTambahAdmin = windowTambahAdmin
        windowTambahAdmin.setObjectName("windowTambahAdmin")
        windowTambahAdmin.resize(1600, 900)
        windowTambahAdmin.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.centralwidget = QtWidgets.QWidget(windowTambahAdmin)

        # Background
        self.bg = QtWidgets.QLabel(self.centralwidget)
        self.bg.setGeometry(QtCore.QRect(0, 0, 1600, 900))
        self.bg.setPixmap(QtGui.QPixmap("C:/ASSETS/BACKGROUND/7.png"))
        self.bg.setScaledContents(True)

        # Input Username
        self.input_username = QtWidgets.QLineEdit(self.centralwidget)
        self.input_username.setGeometry(QtCore.QRect(200, 390, 521, 61))
        self.input_username.setPlaceholderText("Masukkan Username")
        self.input_username.setStyleSheet("""
            QLineEdit {
                color: black;
                border: none;
                border-bottom: 4px solid #a6a6a6;
                font-size: 20px;
            }
            QLineEdit:focus {
                border-bottom: 4px solid #ffbd59;
            }
        """)

        # Input Password
        self.input_password = QtWidgets.QLineEdit(self.centralwidget)
        self.input_password.setGeometry(QtCore.QRect(200, 520, 521, 61))
        self.input_password.setPlaceholderText("Masukkan Password")
        self.input_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.input_password.setStyleSheet("""
            QLineEdit {
                color: black;
                border: none;
                border-bottom: 4px solid #a6a6a6;
                font-size: 20px;
            }
            QLineEdit:focus {
                border-bottom: 4px solid #ffbd59;
            }
        """)

        # Show/Hide Password Button
        self.btn_show_password = QtWidgets.QPushButton(self.centralwidget)
        self.btn_show_password.setGeometry(QtCore.QRect(676, 520, 61, 61))
        self.btn_show_password.setStyleSheet("border: none;")
        self.btn_show_password.setIcon(QtGui.QIcon("C:/ASSETS/BUTTON/EYE.png"))
        self.btn_show_password.setIconSize(QtCore.QSize(40, 40))
        self.btn_show_password.setCheckable(True)
        self.btn_show_password.clicked.connect(self.toggle_password)

        # Save Admin Button
        self.btn_simpan = QtWidgets.QPushButton(self.centralwidget)
        self.btn_simpan.setGeometry(QtCore.QRect(330, 660, 251, 91))
        self.btn_simpan.setStyleSheet("border-image: url(C:/ASSETS/BUTTON/LOGIN.png);")
        self.add_hover_effect(self.btn_simpan)
        self.btn_simpan.clicked.connect(self.simpanAdmin)

        # Back Button
        self.btn_kembali = QtWidgets.QPushButton(self.centralwidget)
        self.btn_kembali.setGeometry(QtCore.QRect(10, 20, 111, 101))
        self.btn_kembali.setStyleSheet("border-image: url(C:/ASSETS/BUTTON/BACK.png);")
        self.add_hover_effect(self.btn_kembali)
        self.btn_kembali.clicked.connect(self.kembali)

        windowTambahAdmin.setCentralWidget(self.centralwidget)

    def toggle_password(self):
        if self.btn_show_password.isChecked():
            self.input_password.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.input_password.setEchoMode(QtWidgets.QLineEdit.Password)

    def add_hover_effect(self, button):
        effect = QtWidgets.QGraphicsOpacityEffect(button)
        button.setGraphicsEffect(effect)
        button.enterEvent = lambda event: effect.setOpacity(0.7)
        button.leaveEvent = lambda event: effect.setOpacity(1.0)

    def simpanAdmin(self):
        username = self.input_username.text().strip()
        password = self.input_password.text().strip()

        if not username or not password:
            QtWidgets.QMessageBox.warning(None, "Gagal", "Username dan password tidak boleh kosong.")
            return

        if self.username_sudah_ada(username):
            QtWidgets.QMessageBox.warning(None, "Gagal", "Username sudah ada.")
            return

        self.simpan_ke_json(username, password)
        QtWidgets.QMessageBox.information(None, "Sukses", "Admin baru berhasil ditambahkan.")
        self.input_username.clear()
        self.input_password.clear()

    def username_sudah_ada(self, username):
        if not os.path.exists("admins.json"):
            return False

        with open("admins.json", "r") as file:
            data = json.load(file)

        return any(admin["username"] == username for admin in data.get("admins", []))

    def simpan_ke_json(self, username, password):
        try:
            if not os.path.exists("admins.json"):
                data = {"admins": []}
            else:
                with open("admins.json", "r") as file:
                    data = json.load(file)

            data["admins"].append({"username": username, "password": password})

            with open("admins.json", "w") as file:
                json.dump(data, file, indent=4)

        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Gagal menyimpan data: {e}")

    def kembali(self):
        self.windowTambahAdmin.close()
        if self.parent_window:
            self.parent_window.enableWindow()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    windowTambahAdmin = QtWidgets.QMainWindow()
    ui = Ui_WindowTambahAdmin()
    ui.setupUi(windowTambahAdmin)
    windowTambahAdmin.show()
    sys.exit(app.exec_())
