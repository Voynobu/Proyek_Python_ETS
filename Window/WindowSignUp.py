# WindowSignUp.py
#Nama: Rangga Muhamad Fajar
#Kelas: 1A - D4
#NIM: 241524026
#Desc: - Tampilan sign-up untuk user baru.
#      - Menyediakan form untuk input nama, email, dan password.
#      - Data user disimpan ke file 'Users.json'.

from PyQt5 import QtCore, QtGui, QtWidgets
import os

class Ui_Dialog(object):
    def setupUi(self, Dialog):
Dialog.s/*************  ✨ Codeium Command ⭐  *************/
    """
    Sets up the user interface for the sign-up dialog.

    This method configures the main dialog window for the sign-up process,
    including its size, appearance, and widgets. It sets a frameless window
    with a background image and adds input fields for the user's name, email,
    and password. There are buttons to toggle password visibility, submit the
    sign-up form, and navigate back to the previous window. Each widget's
    appearance and behavior are configured, including hover effects and event
    connections.
    """

/******  0817a1a3-115b-4878-b5ec-76f65380481a  *******/etObjectName("Dialog")
        Dialog.resize(1600, 900)
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        
        # Atur background sign-up
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(-4, 0, 1611, 901))
        self.label.setPixmap(QtGui.QPixmap("C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/LOGIN/BACKGROUND/4.png"))
        self.label.setScaledContents(True)
        
        # Field untuk Nama
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(200, 350, 521, 51))
        self.lineEdit.setStyleSheet("""
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
        self.lineEdit.setPlaceholderText("Masukkan Nama Lengkap Anda!")
        
        # Field untuk Email
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(200, 450, 521, 51))
        self.lineEdit_2.setStyleSheet("""
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
        self.lineEdit_2.setPlaceholderText("Masukkan Email Anda!")
        
        # Field untuk Password
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(200, 550, 521, 51))
        self.lineEdit_3.setStyleSheet("""
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
        self.lineEdit_3.setPlaceholderText("Masukkan Password Anda!")
        self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password)
        
        # Tombol untuk melihat password
        self.show_password_button = QtWidgets.QPushButton(Dialog)
        self.show_password_button.setGeometry(QtCore.QRect(688, 555, 40, 40))
        self.show_password_button.setStyleSheet("border: none;")
        self.show_password_button.setIcon(QtGui.QIcon("C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/BUTTON/BUTTON/EYE.png"))
        self.show_password_button.setIconSize(QtCore.QSize(30, 30))
        self.show_password_button.setCheckable(True)
        self.show_password_button.clicked.connect(self.toggle_password_visibility)
        
        # Tombol Sign Up
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(330, 620, 251, 91))
        self.pushButton.setStyleSheet("border-image: url(C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/BUTTON/BUTTON/SIGN_UP_PD.png);")
        self.add_hover_effect(self.pushButton)
        
        # Tombol Back
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 20, 111, 101))
        self.pushButton_2.setStyleSheet("border-image: url(C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/BUTTON/BUTTON/BACK.png);")
        self.add_hover_effect(self.pushButton_2)
        
        # Atur urutan tampilan widget
        self.label.raise_()
        self.pushButton.raise_()
        self.lineEdit.raise_()
        self.lineEdit_2.raise_()
        self.pushButton_2.raise_()
        self.lineEdit_3.raise_()
        self.show_password_button.raise_()
        
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Sign Up"))
    
    def toggle_password_visibility(self):
        # Ubah mode echo untuk menampilkan atau menyembunyikan password
        if self.show_password_button.isChecked():
            self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password)
    
    def add_hover_effect(self, button):
        # Tambahkan efek hover pada tombol
        effect = QtWidgets.QGraphicsOpacityEffect()
        button.setGraphicsEffect(effect)
        button.enterEvent = lambda event: effect.setOpacity(0.7)
        button.leaveEvent = lambda event: effect.setOpacity(1.0)
        
# Kelas pembungkus untuk WindowSignUp
class WindowSignUp(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        # Hubungkan tombol Back untuk kembali ke WindowWelcome
        self.ui.pushButton_2.clicked.connect(self.back_to_welcome)
        # Hubungkan tombol Sign Up untuk mendaftarkan user
        self.ui.pushButton.clicked.connect(self.register_user)
    
    def back_to_welcome(self):
        from WindowWelcome import WindowWelcome
        self.welcome = WindowWelcome()
        self.welcome.show()
        self.close()
    
    def register_user(self):
        # Ambil data input user
        name = self.ui.lineEdit.text().strip()
        email = self.ui.lineEdit_2.text().strip()
        password = self.ui.lineEdit_3.text().strip()
        if not name or not email or not password:
            QtWidgets.QMessageBox.warning(self, "Error", "Semua field harus diisi!")
            return
        # Simpan data user ke file users.txt (format: name;email;password)
        try:
            with open("users.txt", "a") as f:
                f.write(f"{name};{email};{password}\n")
            QtWidgets.QMessageBox.information(self, "Sukses", "Pendaftaran berhasil! Silakan login.")
            self.back_to_welcome()
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"Terjadi kesalahan: {str(e)}")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
