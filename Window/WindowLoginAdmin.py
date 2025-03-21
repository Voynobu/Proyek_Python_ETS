# Tampilan admin (edit poli, dokter, biaya)
# WindowLoginAdmin.py
#Nama: Rangga Muhamad Fajar
#Kelas: 1A - D4
#NIM: 241524026
#Desc: - Tampilan login untuk admin.
#      - Memeriksa email dan password dan jika berhasil membuka MainWindow.

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1600, 900)
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        
        # Set background untuk login admin
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(-4, 0, 1611, 901))
        self.label.setPixmap(QtGui.QPixmap("C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/ASSETS/BACKGROUND/2.png"))
        self.label.setScaledContents(True)
        
        # Field untuk Email
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(200, 390, 521, 61))
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
        self.lineEdit.setPlaceholderText("Masukkan Username Anda!")
        
        # Field untuk Password
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(200, 520, 521, 61))
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
        self.lineEdit_2.setPlaceholderText("Masukkan Password Anda!")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        
        self.show_password_button = QtWidgets.QPushButton(Dialog)
        self.show_password_button.setGeometry(QtCore.QRect(676, 520, 61, 61))
        self.show_password_button.setStyleSheet("border: none;")
        self.show_password_button.setIcon(QtGui.QIcon("C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/BUTTON/BUTTON/EYE.png"))
        self.show_password_button.setIconSize(QtCore.QSize(40, 40))
        self.show_password_button.setCheckable(True)
        self.show_password_button.clicked.connect(self.toggle_password)
        
        # Tombol Login
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(330, 660, 251, 91))
        self.pushButton.setStyleSheet("border-image: url(C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/BUTTON/BUTTON/LOGIN.png);")
        self.add_hover_effect(self.pushButton)
        
        # Tombol Back
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 20, 111, 101))
        self.pushButton_2.setStyleSheet("border-image: url(C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/BUTTON/BUTTON/BACK.png);")
        self.add_hover_effect(self.pushButton_2)
        
        self.label.raise_()
        self.pushButton.raise_()
        self.lineEdit.raise_()
        self.lineEdit_2.raise_()
        self.show_password_button.raise_()
        self.pushButton_2.raise_()
        
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Login Admin"))
    
    def toggle_password(self):
        if self.show_password_button.isChecked():
            self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
    
    def add_hover_effect(self, button):
        effect = QtWidgets.QGraphicsOpacityEffect()
        button.setGraphicsEffect(effect)
        button.enterEvent = lambda event: effect.setOpacity(0.7)
        button.leaveEvent = lambda event: effect.setOpacity(1.0)

# Kelas pembungkus untuk WindowLoginAdmin
class WindowLoginAdmin(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        # Tombol Back kembali ke WindowWelcome
        self.ui.pushButton_2.clicked.connect(self.back_to_welcome)
    
    def back_to_welcome(self):
        from WindowWelcome import WindowWelcome
        self.welcome = WindowWelcome()
        self.welcome.show()
        self.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
