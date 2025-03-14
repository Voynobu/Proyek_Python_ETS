# Entry point program utama 
from PyQt5 import QtWidgets
from mainWindow import Ui_MainWindow
from WindowLoginUser import Ui_windowDaftarUser
from windowLoginUser import Ui_windowLoginUser
from windowPendaftaran import Ui_MainWindow as Ui_windowPendaftaran
from daftarUser import Register, load_users, save_users, is_username_taken
import sys

class MainApplication(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_window = Ui_MainWindow()
        self.main_window.setupUi(self)
        
        # Inisialisasi window daftar user
        self.window_daftar_user = QtWidgets.QMainWindow()
        self.ui_daftar_user = Ui_windowDaftarUser()
        self.ui_daftar_user.setupUi(self.window_daftar_user)
        
        # Inisialisasi window login user
        self.window_login_user = QtWidgets.QMainWindow()
        self.ui_login_user = Ui_windowLoginUser()
        self.ui_login_user.setupUi(self.window_login_user)
        
        # Inisialisasi window pendaftaran setelah login sukses
        self.window_pendaftaran = QtWidgets.QMainWindow()
        self.ui_pendaftaran = Ui_windowPendaftaran()
        self.ui_pendaftaran.setupUi(self.window_pendaftaran)
        
        # Tambahkan label status pada window daftar user
        self.status_label_register = QtWidgets.QLabel("", self.ui_daftar_user.centralwidget)
        self.status_label_register.setGeometry(300, 420, 300, 30)
        
        # Tambahkan label status pada window login user
        self.status_label_login = QtWidgets.QLabel("", self.ui_login_user.centralwidget)
        self.status_label_login.setGeometry(300, 420, 300, 30)
        
        # Event handlers
        self.main_window.pushButton_3.clicked.connect(self.show_window_daftar_user)
        self.ui_daftar_user.pushButton.clicked.connect(self.show_main_window)
        self.ui_daftar_user.pushButton_2 = QtWidgets.QPushButton("Daftar", self.ui_daftar_user.centralwidget)
        self.ui_daftar_user.pushButton_2.setGeometry(300, 380, 100, 30)
        self.ui_daftar_user.pushButton_2.clicked.connect(self.register_user)
        
        # Event handlers untuk login user
        self.main_window.pushButton_2.clicked.connect(self.show_window_login_user)
        self.ui_login_user.pushButton.clicked.connect(self.show_main_window)
        self.ui_login_user.pushButton_2 = QtWidgets.QPushButton("Login", self.ui_login_user.centralwidget)
        self.ui_login_user.pushButton_2.setGeometry(300, 350, 100, 30)
        self.ui_login_user.pushButton_2.clicked.connect(self.login_user)
        
        # Event handler untuk kembali dari window pendaftaran ke login user
        self.ui_pendaftaran.pushButton_4.clicked.connect(self.show_window_login_user)
    
    def show_window_daftar_user(self):
        self.window_daftar_user.show()
        self.hide()
    
    def show_window_login_user(self):
        self.window_login_user.show()
        self.window_pendaftaran.hide()
        self.hide()
    
    def show_main_window(self):
        self.show()
        self.window_daftar_user.hide()
        self.window_login_user.hide()
        self.window_pendaftaran.hide()
    
    def show_window_pendaftaran(self):
        self.window_pendaftaran.show()
        self.window_login_user.hide()
    
    def register_user(self):
        username = self.ui_daftar_user.lineEdit.text().strip()
        password = self.ui_daftar_user.lineEdit_2.text().strip()
        
        if not username or not password:
            self.status_label_register.setText("Username dan password harus diisi!")
            return
        
        if is_username_taken(username):
            self.status_label_register.setText("Username sudah terdaftar!")
            return
        
        new_user = Register(username, password)
        users = load_users()
        users.append({"username": new_user.username, "password": new_user.password})
        save_users(users)
        self.status_label_register.setText("Registrasi berhasil!")
    
    def login_user(self):
        username = self.ui_login_user.lineEdit.text().strip()
        password = self.ui_login_user.lineEdit_2.text().strip()
        
        users = load_users()
        for user in users:
            if user["username"] == username:
                hashed_input = Register.hash_password(password)
                if user["password"] == hashed_input:
                    self.show_window_pendaftaran()
                    return
                else:
                    self.status_label_login.setText("Password salah!")
                    return
        
        self.status_label_login.setText("Username tidak ditemukan!")
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_app = MainApplication()
    main_app.show()
    sys.exit(app.exec_())