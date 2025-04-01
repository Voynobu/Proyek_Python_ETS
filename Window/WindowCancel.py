# WindowCancel.py
# Nama: Rangga Muhamad Fajar
# Kelas: 1A - D4
# NIM: 241524026
# Desc: - Program ini digunakan untuk membatalkan pendaftaran pasien di rumah sakit.

# Nama : Muhamad Dino Dermawan
# NIM  : 241524015
# - Menampilkan tabel yang memungkinkan melakukan pembatalan pendaftaran
# - saat melakukan pembatalan, pendaftaran yang dari ongoing, berubah menjadi dibatalkan

# WindowCancel.py - Modified Version (Non-Interactive Table)
# WindowCancel.py - Modified Version (Non-Interactive Table)
import sys
import json
import os
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

class Ui_Dialog(object):
    def __init__(self, username):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        self.riwayat_path = os.path.join(parent_dir, "Data", "riwayat.json")
        self.username = username  # Store the username

    def setupUi(self, Dialog):
        self.dialog = Dialog
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(1598, 900)  # Window fixed size
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        
        # Tombol Back
        self.pushButton_3 = HoverButton(Dialog, image_path="C:/ASSETS/BUTTON/BACK.png")
        self.pushButton_3.setGeometry(QtCore.QRect(10, 20, 111, 101))
        self.pushButton_3.setText("")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.backToMenuUser)
        
        # Background
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(-4, 0, 1611, 901))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("C:/ASSETS/BACKGROUND/16.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        
        # Tabel dengan ukuran tepat sampai batas kanan
        self.tableView = QtWidgets.QTableView(Dialog)
        self.tableView.setGeometry(QtCore.QRect(100, 180, 1398, 650))  # Lebar 1398 untuk pas di kanan
        self.tableView.setStyleSheet("""
            QTableView {
                font-size: 12pt;
                background-color: white;
                gridline-color: #dddddd;
                border: 2px solid #0cc0df;
                selection-background-color: transparent;
                selection-color: black;
            }
            QHeaderView::section {
                background-color: #0cc0df;
                color: white;
                padding: 12px;
                font-size: 12pt;
                border: none;
            }
            QTableView::item {
                padding: 8px;
                border-right: 1px solid #dddddd;
                border-bottom: 1px solid #dddddd;
            }
            QTableView::item:selected {
                background: transparent;
                color: black;
            }
            QTableView::item:hover {
                background: #f0f0f0;
            }
        """)
        self.tableView.setObjectName("tableView")
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableView.setFixedSize(1398, 650)  # Ukuran fixed
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tableView.setFocusPolicy(QtCore.Qt.NoFocus)
        
        self.label.raise_()
        self.pushButton_3.raise_()
        self.tableView.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
        self.initTable()
        self.loadData()
        
    def initTable(self):
        self.model = QStandardItemModel()
        headers = ["NO", "NAMA", "POLI", "JENIS LAYANAN", "TANGGAL", "NO. ANTRIAN", "STATUS", "AKSI"]
        self.model.setHorizontalHeaderLabels(headers)
        self.tableView.setModel(self.model)
        
        # Lebar kolom disesuaikan untuk memenuhi lebar tabel (total 1398)
        column_widths = [60, 200, 200, 200, 150, 250, 120, 118]  # Adjusted for new STATUS column
        for i, width in enumerate(column_widths):
            self.tableView.setColumnWidth(i, width)
        
        # Tinggi baris
        self.tableView.verticalHeader().setDefaultSectionSize(45)
    
    def loadData(self):
        try:
            # Check if file exists
            if not os.path.exists(self.riwayat_path):
                QtWidgets.QMessageBox.critical(self.dialog, "Error", "File riwayat.json tidak ditemukan!")
                return
                
            # Check if username is provided
            if not self.username:
                QtWidgets.QMessageBox.warning(self.dialog, "Warning", "Username tidak terdeteksi!")
                return

            with open(self.riwayat_path, 'r') as file:
                data = json.load(file)
            
            self.model.setRowCount(0)
            row_count = 0
            
            # Check if user has records
            if self.username not in data:
                QtWidgets.QMessageBox.information(self.dialog, "Info", "Tidak ada pendaftaran untuk user ini")
                return

            for reg in data[self.username]:
                # Get status (case-insensitive check)
                status = reg.get('status', 'On going')
                normalized_status = status.lower().replace(" ", "")
                
                # Only show ongoing registrations
                if normalized_status in ['ongoing', 'on-going', 'on going']:
                    row = [
                        QStandardItem(str(row_count + 1)),
                        QStandardItem(reg['nama']),
                        QStandardItem(reg['poli']),
                        QStandardItem(reg['jenis_layanan']),
                        QStandardItem(reg['tanggal_temu']),
                        QStandardItem(reg['nomor antrian']),
                        QStandardItem(status)
                    ]
                    
                    # Set red color for cancelled status
                    if normalized_status == 'dibatalkan':
                        row[6].setForeground(QtGui.QColor(255, 0, 0))
                    
                    font = QtGui.QFont()
                    font.setPointSize(11)
                    
                    for item in row:
                        item.setTextAlignment(QtCore.Qt.AlignCenter)
                        item.setFont(font)
                        item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                    
                    self.model.appendRow(row)
                    row_count += 1
            
            self.addCancelButtons()
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Gagal memuat data: {str(e)}")

    def addCancelButtons(self):
        for row in range(self.model.rowCount()):
            status_item = self.model.item(row, 6)
            status = status_item.text().lower().replace(" ", "")
            
            btn = QtWidgets.QPushButton()
            btn.setStyleSheet("""
                QPushButton {
                    border-radius: 4px;
                    padding: 6px 10px;
                    font-weight: bold;
                    font-size: 11pt;
                    min-width: 90px;
                    border: none;
                }
            """)
            
            if status == 'dibatalkan':
                btn.setText("Dibatalkan")
                btn.setStyleSheet(btn.styleSheet() + """
                    QPushButton {
                        background-color: #cccccc;
                        color: #666666;
                    }
                """)
                btn.setEnabled(False)
            else:
                btn.setText("Batalkan")
                btn.setStyleSheet(btn.styleSheet() + """
                    QPushButton {
                        background-color: #ff5555;
                        color: white;
                    }
                    QPushButton:hover {
                        background-color: #ff3333;
                    }
                """)
                btn.clicked.connect(lambda _, r=row: self.confirmCancel(r))
            
            self.tableView.setIndexWidget(self.model.index(row, 7), btn)

    def confirmCancel(self, row):
        no_antrian = self.model.item(row, 5).text()  # NO. ANTRIAN is at index 5
        nama_pasien = self.model.item(row, 1).text()
        
        reply = QtWidgets.QMessageBox.question(
            None,
            'Konfirmasi Pembatalan',
            f'Apakah Anda yakin ingin membatalkan pendaftaran:\n\n'
            f'Atas nama: {nama_pasien}\n'
            f'Nomor antrian: {no_antrian}?',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            self.updateRegistrationStatus(row, no_antrian)

    def updateRegistrationStatus(self, row, no_antrian):
        try:
            with open(self.riwayat_path, 'r') as file:
                data = json.load(file)
            
            # Only check the current user's registrations
            if self.username in data:
                for reg in data[self.username]:
                    if reg['nomor antrian'] == no_antrian:
                        # Update status to "Dibatalkan"
                        reg['status'] = 'Dibatalkan'
                        
                        with open(self.riwayat_path, 'w') as file:
                            json.dump(data, file, indent=4)
                        
                        # Update the table view
                        self.model.item(row, 6).setText("Dibatalkan")
                        self.model.item(row, 6).setForeground(QtGui.QColor(255, 0, 0))
                        
                        # Update the cancel button
                        btn = self.tableView.indexWidget(self.model.index(row, 7))
                        btn.setText("Dibatalkan")
                        btn.setStyleSheet("""
                            QPushButton {
                                background-color: #cccccc;
                                color: #666666;
                                border-radius: 4px;
                                padding: 6px 10px;
                                font-weight: bold;
                                font-size: 11pt;
                                min-width: 90px;
                                border: none;
                            }
                        """)
                        btn.setEnabled(False)
                        
                        QtWidgets.QMessageBox.information(
                            None,
                            'Berhasil',
                            'Status pendaftaran berhasil diubah menjadi "Dibatalkan"'
                        )
                        return
            
            QtWidgets.QMessageBox.warning(
                None,
                'Data Tidak Ditemukan',
                'Nomor antrian tidak ditemukan dalam database!'
            )
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                None,
                'Error',
                f'Gagal mengubah status pendaftaran: {str(e)}'
            )

    def backToMenuUser(self):
        from WindowMenuUser import WindowMenuUser
        self.menu_user = WindowMenuUser(self.username)
        self.menu_user.show()
        self.dialog.close()
    
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Pembatalan Pendaftaran"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog("test")  # For testing, pass a sample username
    ui.setupUi(Dialog)
    Dialog.setFixedSize(1598, 900)  # Window fixed size
    Dialog.show()
    sys.exit(app.exec_())
