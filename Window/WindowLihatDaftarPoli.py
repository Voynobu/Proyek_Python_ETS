#Author : Zaidan Zulkaisi Setiaji
#NIM/Kelas : 241524031/1A-D4
#Deskripsi : Window yang muncul ketika kita memilih opsi jadwal poli(versi admin)

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer
from Models import Dokter, Jadwal, Poli, JadwalPoli
import json  

# File to save and load data
DATA_FILE = "jadwal_poli_data.json"

class EditJadwalWidget(QtWidgets.QWidget):
    finished = QtCore.pyqtSignal()  

    def __init__(self, jadwal_poli, parent=None):
        super().__init__(parent)
        self.jadwal_poli = jadwal_poli
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Edit Jadwal")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QtWidgets.QVBoxLayout(self)

        self.label = QtWidgets.QLabel("Pilih Poli dan Dokter untuk Menambah/Mengedit Jadwal", self)
        self.layout.addWidget(self.label)

        self.comboPoli = QtWidgets.QComboBox(self)
        for poli in self.jadwal_poli.daftar_poli:
            self.comboPoli.addItem(poli.nama_poli)
        self.layout.addWidget(self.comboPoli)

        self.comboDokter = QtWidgets.QComboBox(self)
        self.layout.addWidget(self.comboDokter)

        self.comboPoli.currentIndexChanged.connect(self.update_dokter_list)

        self.inputHari = QtWidgets.QLineEdit(self)
        self.inputHari.setPlaceholderText("Masukkan Hari (Contoh: Monday)")
        self.layout.addWidget(self.inputHari)

        self.inputJamAwal = QtWidgets.QLineEdit(self)
        self.inputJamAwal.setPlaceholderText("Masukkan Jam Awal (Format: HH:MM)")
        self.layout.addWidget(self.inputJamAwal)

        self.inputJamAkhir = QtWidgets.QLineEdit(self)
        self.inputJamAkhir.setPlaceholderText("Masukkan Jam Akhir (Format: HH:MM)")
        self.layout.addWidget(self.inputJamAkhir)

        self.buttonTambah = QtWidgets.QPushButton("Tambah Jadwal", self)
        self.buttonTambah.clicked.connect(self.tambah_jadwal)
        self.layout.addWidget(self.buttonTambah)

        self.buttonUpdate = QtWidgets.QPushButton("Update Jadwal", self)
        self.buttonUpdate.clicked.connect(self.update_jadwal)
        self.layout.addWidget(self.buttonUpdate)

        self.buttonHapusJadwal = QtWidgets.QPushButton("Hapus Jadwal", self)
        self.buttonHapusJadwal.clicked.connect(self.hapus_jadwal)
        self.layout.addWidget(self.buttonHapusJadwal)

        self.update_dokter_list()

    def update_dokter_list(self):
        self.comboDokter.clear()
        selected_poli = self.jadwal_poli.daftar_poli[self.comboPoli.currentIndex()]
        for dokter in selected_poli.dokter_list:
            self.comboDokter.addItem(dokter.nama)

    def tambah_jadwal(self):
        selected_poli = self.jadwal_poli.daftar_poli[self.comboPoli.currentIndex()]
        selected_dokter = selected_poli.dokter_list[self.comboDokter.currentIndex()]
        hari = self.inputHari.text()
        jam_awal = self.inputJamAwal.text()
        jam_akhir = self.inputJamAkhir.text()

        if hari and jam_awal and jam_akhir:
            jadwal_baru = Jadwal(selected_dokter, hari, jam_awal, jam_akhir)
            selected_poli.TambahJadwal(jadwal_baru)
            QtWidgets.QMessageBox.information(self, "Sukses", "Jadwal berhasil ditambahkan!")
            self.finished.emit()  
            self.close()
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Semua field harus diisi!")

    def update_jadwal(self):
        selected_poli = self.jadwal_poli.daftar_poli[self.comboPoli.currentIndex()]
        selected_dokter = selected_poli.dokter_list[self.comboDokter.currentIndex()]

        
        jadwal_list = [jadwal for jadwal in selected_poli.jadwal_list if jadwal.dokter == selected_dokter]
        if not jadwal_list:
            QtWidgets.QMessageBox.warning(self, "Error", "Tidak ada jadwal untuk dokter ini.")
            return

        jadwal_items = [str(jadwal) for jadwal in jadwal_list]
        jadwal_to_update, ok = QtWidgets.QInputDialog.getItem(self, "Pilih Jadwal", "Pilih jadwal yang ingin diupdate:", jadwal_items, 0, False)

        if ok and jadwal_to_update:
            selected_jadwal = jadwal_list[jadwal_items.index(jadwal_to_update)]
            hari = self.inputHari.text()
            jam_awal = self.inputJamAwal.text()
            jam_akhir = self.inputJamAkhir.text()

            if hari and jam_awal and jam_akhir:
                selected_jadwal.hari = hari
                selected_jadwal.jam_awal = jam_awal
                selected_jadwal.jam_akhir = jam_akhir
                QtWidgets.QMessageBox.information(self, "Sukses", "Jadwal berhasil diupdate!")
                self.finished.emit() 
                self.close()
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Semua field harus diisi!")

    def hapus_jadwal(self):
        selected_poli = self.jadwal_poli.daftar_poli[self.comboPoli.currentIndex()]
        selected_dokter = selected_poli.dokter_list[self.comboDokter.currentIndex()]

       
        jadwal_list = [jadwal for jadwal in selected_poli.jadwal_list if jadwal.dokter == selected_dokter]
        if not jadwal_list:
            QtWidgets.QMessageBox.warning(self, "Error", "Tidak ada jadwal untuk dokter ini.")
            return

        jadwal_items = [str(jadwal) for jadwal in jadwal_list]
        jadwal_to_delete, ok = QtWidgets.QInputDialog.getItem(self, "Hapus Jadwal", "Pilih jadwal yang ingin dihapus:", jadwal_items, 0, False)

        if ok and jadwal_to_delete:
            selected_jadwal = jadwal_list[jadwal_items.index(jadwal_to_delete)]
            selected_poli.jadwal_list.remove(selected_jadwal)
            QtWidgets.QMessageBox.information(self, "Sukses", "Jadwal berhasil dihapus!")
            self.finished.emit()  
            self.close()


class EditDokterWidget(QtWidgets.QWidget):
    finished = QtCore.pyqtSignal() 

    def __init__(self, jadwal_poli, parent=None):
        super().__init__(parent)
        self.jadwal_poli = jadwal_poli
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Edit Dokter")
        self.setGeometry(100, 100, 400, 200)

        self.layout = QtWidgets.QVBoxLayout(self)

        self.label = QtWidgets.QLabel("Tambah atau Edit Dokter", self)
        self.layout.addWidget(self.label)

        self.comboPoli = QtWidgets.QComboBox(self)
        for poli in self.jadwal_poli.daftar_poli:
            self.comboPoli.addItem(poli.nama_poli)
        self.layout.addWidget(self.comboPoli)

        self.inputNama = QtWidgets.QLineEdit(self)
        self.inputNama.setPlaceholderText("Masukkan Nama Dokter")
        self.layout.addWidget(self.inputNama)

        self.inputSpesialis = QtWidgets.QLineEdit(self)
        self.inputSpesialis.setPlaceholderText("Masukkan Spesialisasi Dokter")
        self.layout.addWidget(self.inputSpesialis)

        self.buttonTambah = QtWidgets.QPushButton("Tambah Dokter", self)
        self.buttonTambah.clicked.connect(self.tambah_dokter)
        self.layout.addWidget(self.buttonTambah)

        self.buttonHapusDokter = QtWidgets.QPushButton("Hapus Dokter", self)
        self.buttonHapusDokter.clicked.connect(self.hapus_dokter)
        self.layout.addWidget(self.buttonHapusDokter)

    def tambah_dokter(self):
        selected_poli = self.jadwal_poli.daftar_poli[self.comboPoli.currentIndex()]
        nama = self.inputNama.text()
        spesialis = self.inputSpesialis.text()

        if nama and spesialis:
            dokter_baru = Dokter(nama, spesialis)
            selected_poli.TambahDokter(dokter_baru)
            QtWidgets.QMessageBox.information(self, "Sukses", "Dokter berhasil ditambahkan!")
            self.finished.emit()  
            self.close()
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Semua field harus diisi!")

    def hapus_dokter(self):
        selected_poli = self.jadwal_poli.daftar_poli[self.comboPoli.currentIndex()]
        if not selected_poli.dokter_list:
            QtWidgets.QMessageBox.warning(self, "Error", "Tidak ada dokter di poli ini.")
            return

        dokter_items = [str(dokter) for dokter in selected_poli.dokter_list]
        dokter_to_delete, ok = QtWidgets.QInputDialog.getItem(self, "Hapus Dokter", "Pilih dokter yang ingin dihapus:", dokter_items, 0, False)

        if ok and dokter_to_delete:
            selected_dokter = selected_poli.dokter_list[dokter_items.index(dokter_to_delete)]
            selected_poli.dokter_list.remove(selected_dokter)
            QtWidgets.QMessageBox.information(self, "Sukses", "Dokter berhasil dihapus!")
            self.finished.emit()  
            self.close()


class EditPoliWidget(QtWidgets.QWidget):
    finished = QtCore.pyqtSignal() 

    def __init__(self, jadwal_poli, parent=None):
        super().__init__(parent)
        self.jadwal_poli = jadwal_poli
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Edit Poli")
        self.setGeometry(100, 100, 400, 200)

        self.layout = QtWidgets.QVBoxLayout(self)

        self.label = QtWidgets.QLabel("Tambah atau Edit Poli", self)
        self.layout.addWidget(self.label)

        self.inputNamaPoli = QtWidgets.QLineEdit(self)
        self.inputNamaPoli.setPlaceholderText("Masukkan Nama Poli")
        self.layout.addWidget(self.inputNamaPoli)

        self.buttonTambah = QtWidgets.QPushButton("Tambah Poli", self)
        self.buttonTambah.clicked.connect(self.tambah_poli)
        self.layout.addWidget(self.buttonTambah)

        self.buttonHapusPoli = QtWidgets.QPushButton("Hapus Poli", self)
        self.buttonHapusPoli.clicked.connect(self.hapus_poli)
        self.layout.addWidget(self.buttonHapusPoli)

    def tambah_poli(self):
        nama_poli = self.inputNamaPoli.text()

        if nama_poli:
            poli_baru = Poli(nama_poli)
            self.jadwal_poli.TambahPoli(poli_baru)
            QtWidgets.QMessageBox.information(self, "Sukses", "Poli berhasil ditambahkan!")
            self.finished.emit()  
            self.close()
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Nama Poli harus diisi!")

    def hapus_poli(self):
        if not self.jadwal_poli.daftar_poli:
            QtWidgets.QMessageBox.warning(self, "Error", "Tidak ada poli yang tersedia.")
            return

        poli_items = [str(poli) for poli in self.jadwal_poli.daftar_poli]
        poli_to_delete, ok = QtWidgets.QInputDialog.getItem(self, "Hapus Poli", "Pilih poli yang ingin dihapus:", poli_items, 0, False)

        if ok and poli_to_delete:
            selected_poli = self.jadwal_poli.daftar_poli[poli_items.index(poli_to_delete)]
            self.jadwal_poli.daftar_poli.remove(selected_poli)
            QtWidgets.QMessageBox.information(self, "Sukses", "Poli berhasil dihapus!")
            self.finished.emit()  
            self.close()


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("JadwalPoli")
        Form.resize(800, 500)

        # Labels
        self.label1 = QtWidgets.QLabel(Form)
        self.label1.setGeometry(QtCore.QRect(30, 20, 610, 400))
        self.label1.setText("")
        self.label1.setObjectName("label1")
        self.label1.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.label2 = QtWidgets.QLabel(Form)
        self.label2.setGeometry(QtCore.QRect(30, 450, 350, 40))
        self.label2.setText("")
        self.label2.setObjectName("label2")
        self.label2.setAlignment(Qt.AlignLeft | Qt.AlignBottom)

        # Buttons
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(650, 10, 130, 75))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(650, 100, 130, 75))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(650, 190, 130, 75))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(650, 400, 130, 75))
        self.pushButton_4.setObjectName("pushButton_4")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        
        self.jadwal_poli = self.load_data() 
        if not self.jadwal_poli:
            self.jadwal_poli = JadwalPoli("Jadwal Poli")
            self.initialize_data()

        
        self.update_label1() 

        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  

        
        self.pushButton.clicked.connect(self.edit_jadwal)
        self.pushButton_2.clicked.connect(self.edit_dokter)
        self.pushButton_3.clicked.connect(self.edit_poli)
        self.pushButton_4.clicked.connect(self.kembali)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Edit Jadwal"))
        self.pushButton_2.setText(_translate("Form", "Edit Dokter"))
        self.pushButton_3.setText(_translate("Form", "Edit Poli"))
        self.pushButton_4.setText(_translate("Form", "Kembali"))

    def initialize_data(self):
      
        dokter1 = Dokter("Dr. Asep", "Kardiolog")
        dokter2 = Dokter("Dr. Ahmad", "Oftalmolog")
        dokter3 = Dokter("Dr. Messi", "Spesialis THT-KH")
        dokter4 = Dokter("Dr. Jajang", "Neurolog")

        poli_jantung = Poli("Poli Jantung")
        poli_jantung.TambahDokter(dokter1)
        poli_jantung.TambahJadwal(Jadwal(dokter1, "Tuesday", "08:00", "12:00"))
        poli_jantung.TambahJadwal(Jadwal(dokter1, "Friday", "13:00", "18:00"))

        poli_mata = Poli("Poli Mata")
        poli_mata.TambahDokter(dokter2)
        poli_mata.TambahJadwal(Jadwal(dokter2, "Monday", "09:00", "15:00"))
        poli_mata.TambahJadwal(Jadwal(dokter2, "Thursday", "07:00", "12:00"))

        poli_THT_KL = Poli("Poli THT-KL")
        poli_THT_KL.TambahDokter(dokter3)
        poli_THT_KL.TambahJadwal(Jadwal(dokter3, "Tuesday", "11:00", "18:00"))
        poli_THT_KL.TambahJadwal(Jadwal(dokter3, "Wednesday", "18:00", "21:00"))

        poli_saraf = Poli("Poli Saraf")
        poli_saraf.TambahDokter(dokter4)
        poli_saraf.TambahJadwal(Jadwal(dokter4, "Tuesday", "08:00", "13:00"))
        poli_saraf.TambahJadwal(Jadwal(dokter4, "Sunday", "10:00", "17:00"))

        self.jadwal_poli.TambahPoli(poli_jantung)
        self.jadwal_poli.TambahPoli(poli_mata)
        self.jadwal_poli.TambahPoli(poli_THT_KL)
        self.jadwal_poli.TambahPoli(poli_saraf)

        self.update_label1()

    def update_label1(self):
        # Update label1 
        text = ""
        for poli in self.jadwal_poli.daftar_poli:
            text += f"{poli.nama_poli}\n"
            for dokter in poli.dokter_list:
                text += f"  - {dokter}\n"
            for jadwal in poli.jadwal_list:
                text += f"    * {jadwal}\n"
        self.label1.setText(text)

    def update_time(self):
        # Update label2 
        current_time = QtCore.QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        self.label2.setText(f"Waktu saat ini: {current_time}")

    def edit_jadwal(self):
        self.edit_jadwal_widget = EditJadwalWidget(self.jadwal_poli)
        self.edit_jadwal_widget.finished.connect(self.update_label1)  
        self.edit_jadwal_widget.show()

    def edit_dokter(self):
        self.edit_dokter_widget = EditDokterWidget(self.jadwal_poli)
        self.edit_dokter_widget.finished.connect(self.update_label1)  
        self.edit_dokter_widget.show()

    def edit_poli(self):
        self.edit_poli_widget = EditPoliWidget(self.jadwal_poli)
        self.edit_poli_widget.finished.connect(self.update_label1) 
        self.edit_poli_widget.show()

    def kembali(self):
        # Save data before exiting
        self.save_data()
        QtWidgets.QApplication.quit()

    def save_data(self):
        # Save the JadwalPoli object to a JSON file
        data = {
            "nama": self.jadwal_poli.nama,
            "daftar_poli": [
                {
                    "nama_poli": poli.nama_poli,
                    "dokter_list": [
                        {"nama": dokter.nama, "spesialis": dokter.spesialis}
                        for dokter in poli.dokter_list
                    ],
                    "jadwal_list": [
                        {
                            "dokter": jadwal.dokter.nama,
                            "hari": jadwal.hari,
                            "jam_awal": jadwal.jam_awal,
                            "jam_akhir": jadwal.jam_akhir,
                        }
                        for jadwal in poli.jadwal_list
                    ],
                }
                for poli in self.jadwal_poli.daftar_poli
            ],
        }
        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)

    def load_data(self):
        # Load the JadwalPoli object from a JSON file
        try:
            with open(DATA_FILE, "r") as file:
                data = json.load(file)
                jadwal_poli = JadwalPoli(data["nama"])
                for poli_data in data["daftar_poli"]:
                    poli = Poli(poli_data["nama_poli"])
                    for dokter_data in poli_data["dokter_list"]:
                        dokter = Dokter(dokter_data["nama"], dokter_data["spesialis"])
                        poli.TambahDokter(dokter)
                    for jadwal_data in poli_data["jadwal_list"]:
                        dokter = next(
                            (d for d in poli.dokter_list if d.nama == jadwal_data["dokter"]),
                            None,
                        )
                        if dokter:
                            jadwal = Jadwal(dokter, jadwal_data["hari"], jadwal_data["jam_awal"], jadwal_data["jam_akhir"])
                            poli.TambahJadwal(jadwal)
                    jadwal_poli.TambahPoli(poli)
                return jadwal_poli
        except FileNotFoundError:
            return None


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())