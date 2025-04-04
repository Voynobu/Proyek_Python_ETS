# Author      : Nauval Khairiyan
# NIM/Kelas   : 241524021 / 1A-D4
# Description : Fungsi sound untuk resi dan interface

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl

class SoundManager:
    player = QMediaPlayer()

    # Peta nama ke path file sound
    sounds = {
        "resi": "C:/ASSETS/SOUND/SOUND_RESI.mp3",
        "interface": "C:/ASSETS/SOUND/SOUND_INTERFACE.mp3"
    }

    @classmethod
    def play(cls, sound_name):
        if sound_name in cls.sounds:
            url = QUrl.fromLocalFile(cls.sounds[sound_name])
            content = QMediaContent(url)
            cls.player.setMedia(content)
            cls.player.setVolume(50)  # kamu bisa atur volume di sini
            cls.player.play()
        else:
            print(f"[SoundManager] Sound '{sound_name}' tidak ditemukan.")
