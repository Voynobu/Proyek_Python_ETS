# WindowEditDokter.py
# Nama: Rangga Muhamad Fajar
# Kelas: 1A - D4
# NIM: 241524026
# Desc: - Program ini digunakan untuk mengelola dokter yang ada di rumah sakit.
#       - Admin dapat menambah dan menghapus dokter secara interaktif.
import json
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class HoverButton(QtWidgets.QPushButton):
    def __init__(self, parent=None, image_path=""):
        super().__init__(parent)
        self.opacity_effect = QtWidgets.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1.0)
        self.opacity_animation = QtCore.QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_animation.setDuration(200)
        if image_path:
            self.setStyleSheet(
                f"QPushButton {{ border-image: url('{image_path}'); background: transparent; border: none; }}"
            )
        self.setMouseTracking(True)

    def enterEvent(self, event):
        self.opacity_animation.stop()
        self.opacity_animation.setStartValue(self.opacity_effect.opacity())
        self.opacity_animation.setEndValue(0.7)
        self.opacity_animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.opacity_animation.stop()
        self.opacity_animation.setStartValue(self.opacity_effect.opacity())
        self.opacity_animation.setEndValue(1.0)
        self.opacity_animation.start()
        super().leaveEvent(event)

class Ui_WindowEditDokter(object):
    def __init__(self, parent_window=None, json_data=None):
        self.parent_window = parent_window
        self.json_data = json_data if json_data else self.load_data()
        self.data_updated = False
        self.updated_data = None

    def load_data(self):
        try:
            with open("JadwalPoli.json", "r") as file:
                return json.load(file)
        except:
            return {"daftar_poli": []}

    def setupUi(self, Dialog):
        self.dialog = Dialog
        Dialog.setObjectName("Dialog")
        Dialog.resize(1600, 900)
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        
        # ------ Input Fields ------
        self.lineEdit_1 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_1.setGeometry(QtCore.QRect(910, 401, 608, 51))
        self.lineEdit_1.setPlaceholderText("Masukkan Nama Dokter!")
        
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(910, 501, 608, 51))
        self.lineEdit_2.setPlaceholderText("Masukkan Spesialisasi Dokter!")
        
        # ------ BACK BUTTON ------
        self.pushButton_3 = HoverButton(Dialog, image_path="C:/ASSETS/BUTTON/BACK.png")
        self.pushButton_3.setGeometry(QtCore.QRect(10, 20, 111, 101))
        
        # ------ BACKGROUND LABEL ------
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(-4, 0, 1611, 901))
        self.label.setPixmap(QtGui.QPixmap("C:/ASSETS/BACKGROUND/11.png"))
        self.label.setScaledContents(True)
        
        # ------ TOMBOL TAMBAH DOKTER ------
        self.pushButton_1 = HoverButton(Dialog, image_path="C:/ASSETS/BUTTON/TAMBAH_DOKTER.png")
        self.pushButton_1.setGeometry(QtCore.QRect(891, 593, 648, 101))
        
        # ------ TOMBOL HAPUS DOKTER ------
        self.pushButton_2 = HoverButton(Dialog, image_path="C:/ASSETS/BUTTON/HAPUS_DOKTER.png")
        self.pushButton_2.setGeometry(QtCore.QRect(891, 711, 648, 101))
        
        # ------ COMBOBOX POLI ------
        self.comboBox_2 = QtWidgets.QComboBox(Dialog)
        self.comboBox_2.setGeometry(QtCore.QRect(910, 301, 608, 51))
        
        # ------ TABEL VIEW ------
        self.tableView = QtWidgets.QTableView(Dialog)
        self.tableView.setGeometry(QtCore.QRect(81, 182, 641, 666))
        self.tableView.setStyleSheet(
            """
            QTableView {
                gridline-color: gray;
                font-size: 28px;
            }
            QHeaderView::section {
                background-color: #0cc0df;
                color: white;
                padding: 8px;
                font-weight: bold;
                font-size: 28px;
            }
            """
        )
        
        # Init model dan load data
        self.initModel()
        self.loadData()
        self.loadComboData()
        
        # Konfigurasi tabel
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tableView.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.setShowGrid(True)

        header = self.tableView.horizontalHeader()
        header.setSectionsMovable(False)
        header.setDefaultAlignment(QtCore.Qt.AlignCenter)
        header.setFixedHeight(100)
        self.tableView.verticalHeader().setDefaultSectionSize(100)

        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        self.tableView.setColumnWidth(0, 70)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

        # Z-order
        self.label.lower()
        self.lineEdit_1.raise_()
        self.lineEdit_2.raise_()
        self.pushButton_3.raise_()
        self.pushButton_1.raise_()
        self.pushButton_2.raise_()
        self.comboBox_2.raise_()
        self.tableView.raise_()

        # Hubungkan tombol
        self.pushButton_1.clicked.connect(self.tambah_dokter)
        self.pushButton_2.clicked.connect(self.hapus_dokter)
        self.pushButton_3.clicked.connect(self.backToJadwalPoliDokter)

    def initModel(self):
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["NO", "NAMA DOKTER", "SPESIALISASI", "POLI"])
        self.tableView.setModel(self.model)

    def loadData(self):
        try:
            self.model.setRowCount(0)
            row_num = 0
            for poli in self.json_data["daftar_poli"]:
                for dokter in poli["dokter_list"]:
                    item_no = QStandardItem(str(row_num + 1))
                    item_no.setTextAlignment(QtCore.Qt.AlignCenter)
                    
                    item_dokter = QStandardItem(dokter["nama"])
                    item_dokter.setTextAlignment(QtCore.Qt.AlignCenter)
                    
                    item_spesialis = QStandardItem(dokter["spesialis"])
                    item_spesialis.setTextAlignment(QtCore.Qt.AlignCenter)
                    
                    item_poli = QStandardItem(poli["nama_poli"])
                    item_poli.setTextAlignment(QtCore.Qt.AlignCenter)
                    
                    self.model.appendRow([item_no, item_dokter, item_spesialis, item_poli])
                    row_num += 1
                    
        except Exception as e:
            print("Error membaca data:", e)

    def loadComboData(self):
        try:
            self.comboBox_2.clear()
            for poli in self.json_data["daftar_poli"]:
                self.comboBox_2.addItem(poli["nama_poli"])
                
        except Exception as e:
            print("Error loading combo data:", e)

    def tambah_dokter(self):
        nama_poli = self.comboBox_2.currentText()
        nama_dokter = self.lineEdit_1.text().strip()
        spesialis = self.lineEdit_2.text().strip()
        
        if not all([nama_poli, nama_dokter, spesialis]):
            QtWidgets.QMessageBox.warning(self.dialog, "Error", "Semua field harus diisi!")
            return
            
        # Cari poli dan tambahkan dokter
        for poli in self.json_data["daftar_poli"]:
            if poli["nama_poli"] == nama_poli:
                # Cek apakah dokter sudah ada
                for dokter in poli["dokter_list"]:
                    if dokter["nama"].lower() == nama_dokter.lower():
                        QtWidgets.QMessageBox.warning(self.dialog, "Error", "Dokter sudah ada di poli ini!")
                        return
                        
                # Tambahkan dokter baru
                poli["dokter_list"].append({
                    "nama": nama_dokter,
                    "spesialis": spesialis
                })
                
                self.data_updated = True
                self.updated_data = self.json_data
                
                QtWidgets.QMessageBox.information(self.dialog, "Sukses", "Dokter berhasil ditambahkan!")
                self.loadData()
                self.lineEdit_1.clear()
                self.lineEdit_2.clear()
                return
                
        QtWidgets.QMessageBox.warning(self.dialog, "Error", "Poli tidak ditemukan!")

    def hapus_dokter(self):
        nama_dokter = self.lineEdit_1.text().strip()
        
        if not nama_dokter:
            QtWidgets.QMessageBox.warning(self.dialog, "Error", "Nama Dokter harus diisi!")
            return
            
        # Cari dan hapus dokter
        for poli in self.json_data["daftar_poli"]:
            for i, dokter in enumerate(poli["dokter_list"]):
                if dokter["nama"].lower() == nama_dokter.lower():
                    poli["dokter_list"].pop(i)
                    
                    self.data_updated = True
                    self.updated_data = self.json_data
                    
                    QtWidgets.QMessageBox.information(self.dialog, "Sukses", "Dokter berhasil dihapus!")
                    self.loadData()
                    self.lineEdit_1.clear()
                    return
                    
        QtWidgets.QMessageBox.warning(self.dialog, "Error", "Dokter tidak ditemukan!")

    def backToJadwalPoliDokter(self):
        if self.parent_window:
            if hasattr(self.parent_window, 'ui'):
                if self.data_updated:
                    self.parent_window.ui.data = self.updated_data
                    self.parent_window.ui.loadData()
            self.parent_window.show()
        self.dialog.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_WindowEditDokter()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())