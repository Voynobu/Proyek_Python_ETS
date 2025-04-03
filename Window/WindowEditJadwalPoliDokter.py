# WindowEditJadwalPoliDokter.py
# Nama: Rangga Muhamad Fajar
# Kelas: 1A - D4
# NIM: 241524026
# Desc: Program ini menampilkan dan mengatur jadwal layanan poli beserta dokter di rumah sakit.
#       Admin dapat melihat, menambah, mengubah, dan menghapus jadwal dokter (termasuk status dan kuota).
#       Tabel menampilkan informasi lengkap: nomor, poli, dokter (spesialisasi), jadwal, status, serta kuota maksimum.
import sys
import json
import datetime
import copy
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class HoverButton(QtWidgets.QPushButton):
    def __init__(self, parent=None, image_path=""):
        super().__init__(parent)
        self.opacity_effect = QtWidgets.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_animation = QtCore.QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_animation.setDuration(200)
        self.opacity_effect.setOpacity(1.0)
        if image_path:
            self.setStyleSheet(f"QPushButton {{ border-image: url('{image_path}'); background: transparent; border: none; }}")
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

class Ui_Dialog(object):
    def __init__(self, parent_window=None):
        self.parent_window = parent_window
        self.json_file = "JadwalPoli.json"
        self.data = self.load_json_data()

    def load_json_data(self):
        try:
            with open(self.json_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading JSON file: {e}")
            return {"nama": "Jadwal Poli", "daftar_poli": []}

    def save_json_data(self):
        try:
            with open(self.json_file, "w", encoding="utf-8") as file:
                json.dump(self.data, file, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving JSON file: {e}")
            QtWidgets.QMessageBox.critical(None, "Error", f"Gagal menyimpan data: {str(e)}")
            return False

    def update_status_in_json(self):
        """Update status in JSON data based on current time"""
        now = datetime.datetime.now()
        current_day = now.strftime("%A")
        current_time = now.time()

        for poli in self.data["daftar_poli"]:
            for jadwal in poli["jadwal_list"]:
                try:
                    if jadwal["hari"].lower() == current_day.lower():
                        start_time = datetime.datetime.strptime(jadwal["jam_awal"], "%H:%M").time()
                        end_time = datetime.datetime.strptime(jadwal["jam_akhir"], "%H:%M").time()
                        jadwal["status"] = "AVAILABLE" if start_time <= current_time <= end_time else "UNAVAILABLE"
                    else:
                        jadwal["status"] = "UNAVAILABLE"
                except Exception as e:
                    print(f"Error updating status: {e}")
                    jadwal["status"] = "UNAVAILABLE"
        
        return self.save_json_data()

    def setupUi(self, Dialog):
        self.dialog = Dialog
        Dialog.setObjectName("Dialog")
        Dialog.resize(1600, 900)
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # Back Button
        self.pushButton_4 = HoverButton(Dialog, image_path="C:/ASSETS/BUTTON/BACK.png")
        self.pushButton_4.setGeometry(QtCore.QRect(10, 20, 111, 101))
        self.pushButton_4.setText("")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.backToMenuAdmin)

        # Background Label
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(-4, 0, 1611, 901))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("C:/ASSETS/BACKGROUND/12.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        # Table View
        self.tableView = QtWidgets.QTableView(Dialog)
        self.tableView.setGeometry(QtCore.QRect(440, 170, 1131, 696))
        self.tableView.setStyleSheet("""
            QTableView {
                gridline-color: gray;
                font-size: 20px;
            }
            QHeaderView::section {
                background-color: #0cc0df; 
                color: white;
                padding: 8px;
                font-weight: bold;
                font-size: 20px;
            }
        """)
        self.tableView.setObjectName("tableView")

        # Buttons
        self.pushButton_1 = HoverButton(Dialog, image_path="C:/ASSETS/BUTTON/EDIT_JADWAL.png")
        self.pushButton_1.setGeometry(QtCore.QRect(-2, 219, 411, 201))
        self.pushButton_1.setText("")
        self.pushButton_1.setObjectName("pushButton_1")
        self.pushButton_1.clicked.connect(self.openEditJadwal)

        self.pushButton_2 = HoverButton(Dialog, image_path="C:/ASSETS/BUTTON/EDIT_POLI.png")
        self.pushButton_2.setGeometry(QtCore.QRect(-2, 444, 411, 201))
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.openEditPoli)

        self.pushButton_3 = HoverButton(Dialog, image_path="C:/ASSETS/BUTTON/EDIT_DOK.png")
        self.pushButton_3.setGeometry(QtCore.QRect(-7, 669, 421, 201))
        self.pushButton_3.setText("")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.openEditDokter)

        # Datetime Label
        self.label_datetime = QtWidgets.QLabel(Dialog)
        self.label_datetime.setGeometry(QtCore.QRect(431, 36, 691, 96))
        self.label_datetime.setAlignment(QtCore.Qt.AlignCenter)
        self.label_datetime.setStyleSheet("""
            QLabel {
                color: #12c2e8;
                font-size: 30px;
                font-weight: bold;
            }
        """)
        self.label_datetime.setObjectName("label_datetime")

        # Z-order
        self.label.raise_()
        self.pushButton_4.raise_()
        self.pushButton_1.raise_()
        self.tableView.raise_()
        self.pushButton_2.raise_()
        self.pushButton_3.raise_()
        self.label_datetime.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # Initialize table
        self.initTable()
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tableView.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.setShowGrid(True)

        header = self.tableView.horizontalHeader()
        header.setSectionsMovable(False)
        header.setDefaultAlignment(QtCore.Qt.AlignCenter)

        # Header height (untuk baris header saja)
        header.setFixedHeight(100)

        # KOMENTAR atau HAPUS setDefaultSectionSize agar stretch benar-benar berfungsi
        # self.tableView.verticalHeader().setDefaultSectionSize(100)

        # -- Inilah kunci agar baris mengisi area tabel secara dinamis --
        self.tableView.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Set column widths
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)   # NO
        self.tableView.setColumnWidth(0, 50)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch) # POLI
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch) # DOKTER
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch) # JADWAL

        # STATUS (4) dan KUOTA (5) dipertahankan fixed
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Fixed)
        self.tableView.setColumnWidth(4, 150)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Fixed)
        self.tableView.setColumnWidth(5, 120)

        # Load data awal
        self.loadData()

        # Timer untuk update date/time + status
        self.timer = QtCore.QTimer(Dialog)
        self.timer.timeout.connect(self.updateDateTimeAndStatus)
        self.timer.start(1000)
        self.updateDateTimeAndStatus()

    def initTable(self):
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels([
            "NO", "POLI", "DOKTER", "JADWAL", "STATUS", "KUOTA"
        ])
        self.tableView.setModel(self.model)

    def checkScheduleStatus(self, jadwal_list):
        now = datetime.datetime.now()
        current_day = now.strftime("%A")
        current_time = now.time()
        
        status_list = []
        
        for jadwal in jadwal_list:
            schedule_day = jadwal.get("hari", "")
            
            if schedule_day.lower() != current_day.lower():
                status_list.append("UNAVAILABLE")
                continue
                
            try:
                start_time = datetime.datetime.strptime(jadwal.get("jam_awal", "00:00"), "%H:%M").time()
                end_time = datetime.datetime.strptime(jadwal.get("jam_akhir", "00:00"), "%H:%M").time()
                
                if start_time <= current_time <= end_time:
                    status_list.append("AVAILABLE")
                else:
                    status_list.append("UNAVAILABLE")
            except Exception as e:
                print(f"Error parsing time: {e}")
                status_list.append("UNAVAILABLE")
        
        return status_list

    def loadData(self):
        try:
            self.data = self.load_json_data()
            self.model.setRowCount(0)
            
            for idx, poli in enumerate(self.data["daftar_poli"], start=1):
                nama_poli = poli.get("nama_poli", "").upper()
                kuota = str(poli.get("kuota", "N/A"))
                
                # Format doctors
                dokter_str = "\n".join([
                    f"{dokter.get('nama', '')} ({dokter.get('spesialis', '')})" 
                    for dokter in poli.get("dokter_list", [])
                ])
                
                # Format schedules and get current statuses
                jadwal_entries = []
                status_list = self.checkScheduleStatus(poli.get("jadwal_list", []))
                
                for jadwal, status in zip(poli.get("jadwal_list", []), status_list):
                    hari = jadwal.get("hari", "").upper()
                    jam = f"{jadwal.get('jam_awal', '')} - {jadwal.get('jam_akhir', '')}"
                    jadwal_entries.append(f"{hari} ({jam})")
                
                jadwal_str = "\n".join(jadwal_entries)
                status_str = "\n".join(status_list)
                
                # Add row to table
                row_data = [
                    str(idx), 
                    nama_poli, 
                    dokter_str, 
                    jadwal_str, 
                    status_str, 
                    kuota
                ]
                
                items = []
                for value in row_data:
                    item = QStandardItem(str(value))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    items.append(item)
                self.model.appendRow(items)
                
        except Exception as e:
            print(f"Error loading data: {e}")
            self.loadFallbackData()

    def loadFallbackData(self):
        fallback_data = [
            ("1", "POLI MATA", "Dr. Ahmad (Oftalmolog)", "THURSDAY (07:00 - 12:00)", "UNAVAILABLE", "5"),
            ("2", "POLI THT-KL", "Dr. Messi (Spesialis THT-KH)", "TUESDAY (11:00 - 18:00)\nWEDNESDAY (18:00 - 21:00)", "UNAVAILABLE\nUNAVAILABLE", "5"),
            ("3", "POLI SARAF", "Dr. Jajang (Neurolog)", "TUESDAY (08:00 - 13:00)\nSUNDAY (10:00 - 17:00)", "UNAVAILABLE\nUNAVAILABLE", "5"),
            ("4", "POLI ANAK", "Dr.Radhit (Pediatrik Gawat Darurat)", "THURSDAY (10:00 - 17:00)", "UNAVAILABLE", "5"),
            ("5", "POLI GIGI", "Dr. Sarifudin (Gigi)", "WEDNESDAY (08:00 - 20:00)", "UNAVAILABLE", "5")
        ]
        self.model.setRowCount(0)
        for row_data in fallback_data:
            items = []
            for value in row_data:
                item = QStandardItem(str(value))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                items.append(item)
            self.model.appendRow(items)

    def updateDateTimeAndStatus(self):
        # Update datetime display
        now = QtCore.QDateTime.currentDateTime()
        day_of_week = now.toString("dddd").upper()
        date_str = now.toString("yyyy-MM-dd")
        time_str = now.toString("HH:mm:ss")
        self.label_datetime.setText(f"{day_of_week} | {date_str} | {time_str}")
        
        # Update status in JSON and reload data
        if self.update_status_in_json():
            self.loadData()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Window Edit Jadwal Poli Dokter"))

    def backToMenuAdmin(self):
        if self.parent_window:
            self.parent_window.show()
        self.dialog.close()

    def openEditJadwal(self):
        self.dialog.hide()
        from WindowEditJadwal import Ui_Dialog as Ui_WindowEditJadwal
        self.edit_jadwal_dialog = QtWidgets.QDialog()
        self.ui_edit_jadwal = Ui_WindowEditJadwal(parent_window=self.dialog, json_data=copy.deepcopy(self.data))
        self.ui_edit_jadwal.setupUi(self.edit_jadwal_dialog)
        
        def on_dialog_finished():
            if hasattr(self.ui_edit_jadwal, 'data_updated') and self.ui_edit_jadwal.data_updated:
                self.data = copy.deepcopy(self.ui_edit_jadwal.updated_data)
                if self.save_json_data():
                    self.loadData()
            self.dialog.show()
            
        self.edit_jadwal_dialog.finished.connect(on_dialog_finished)
        self.edit_jadwal_dialog.show()

    def openEditPoli(self):
        self.dialog.hide()
        from WindowEditPoli import Ui_Dialog as Ui_WindowEditPoli
        self.edit_poli_dialog = QtWidgets.QDialog()
        self.ui_edit_poli = Ui_WindowEditPoli(parent_window=self.dialog, json_data=copy.deepcopy(self.data))
        self.ui_edit_poli.setupUi(self.edit_poli_dialog)
        
        def on_dialog_finished():
            if hasattr(self.ui_edit_poli, 'data_updated') and self.ui_edit_poli.data_updated:
                self.data = copy.deepcopy(self.ui_edit_poli.updated_data)
                if self.save_json_data():
                    self.loadData()
            self.dialog.show()
            
        self.edit_poli_dialog.finished.connect(on_dialog_finished)
        self.edit_poli_dialog.show()

    def openEditDokter(self):
        self.dialog.hide()
        from WindowEditDokter import Ui_WindowEditDokter
        self.edit_dokter_dialog = QtWidgets.QDialog()
        self.ui_edit_dokter = Ui_WindowEditDokter(parent_window=self.dialog, json_data=copy.deepcopy(self.data))
        self.ui_edit_dokter.setupUi(self.edit_dokter_dialog)
        
        def on_dialog_finished():
            if hasattr(self.ui_edit_dokter, 'data_updated') and self.ui_edit_dokter.data_updated:
                self.data = copy.deepcopy(self.ui_edit_dokter.updated_data)
                if self.save_json_data():
                    self.loadData()
            self.dialog.show()
            
        self.edit_dokter_dialog.finished.connect(on_dialog_finished)
        self.edit_dokter_dialog.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog(parent_window=None)
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())