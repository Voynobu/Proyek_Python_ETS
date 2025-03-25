# WindowSplashScreen.py
# Nama: Rangga Muhamad Fajar
# Kelas: 1A - D4
# NIM: 241524026
# Desc: - Pembuatan splash screen sebagai tampilan awal aplikasi.
#       - Menampilkan gambar splash selama 3 detik sebelum beralih ke WindowWelcome.
#       - Memainkan musik saat splash screen ditampilkan.

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import os
from WindowWelcome import WindowWelcome

class WindowSplashScreen(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        
        # Hilangkan border window
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setFixedSize(1600, 900)
        
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(0, 0, 1600, 900)

        image_path = "C:/ASSETS/BACKGROUND/SPLASH.png"
        self.load_image(self.label, image_path)
        self.label.setScaledContents(True)

        self.player = QMediaPlayer()
        sound_path = "C:/ASSETS/SOUND/SOUND_SPLASHSCREEN.mp3"
        
        if os.path.exists(sound_path):
            self.player.setMedia(QMediaContent(QtCore.QUrl.fromLocalFile(sound_path)))  # ✅ Pakai setMedia()
            self.player.setVolume(100)  # Atur volume ke 50%
            QtCore.QTimer.singleShot(100, self.player.play)  # Mainkan suara setelah splash tampil
            print(f"✅ Playing sound: {sound_path}")
        else:
            print(f"❌ Error: Sound file not found -> {sound_path}")

        # Timer untuk splash screen selama 3 detik
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.show_welcome_window)
        self.timer.start(2700)

    def load_image(self, widget, image_path):
        # Periksa ketersediaan file gambar dan muat jika ada
        if os.path.exists(image_path):
            pixmap = QtGui.QPixmap(image_path)
            widget.setPixmap(pixmap)
            print(f"✅ Loaded splash image: {image_path}")
        else:
            print(f"❌ Error: Splash image not found -> {image_path}")

    def show_welcome_window(self):
        # Setelah timer habis, buka WindowWelcome dan tutup splash screen
        self.timer.stop()
        self.player.stop()  
        self.welcome = WindowWelcome()
        self.welcome.show()
        self.close()
