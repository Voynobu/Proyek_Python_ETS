# Tampilan admin (edit poli, dokter, biaya)
# WindowEditJadwal.py
# Nama: Rangga Muhamad Fajar
# Kelas: 1A - D4
# NIM: 241524026
# Desc: - Program ini digunakan untuk mengelola jadwal layanan poli di rumah sakit.
#       - Admin dapat menambah, mengubah, dan menghapus jadwal dokter secara interaktif.


from PyQt5 import QtCore, QtGui, QtWidgets

class HoverButton(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.effect = QtWidgets.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.effect)
        self.effect.setOpacity(1.0)  # Opasitas normal

    def enterEvent(self, event):
        self.effect.setOpacity(0.7)  # Turunkan opasitas saat hover (misal 70%)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.effect.setOpacity(1.0)  # Kembalikan opasitas normal
        super().leaveEvent(event)


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        Dialog.setObjectName("Dialog")
        Dialog.resize(1600, 900)
        
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(154, 639, 648, 51))
        self.lineEdit_2.setStyleSheet(
            "QLineEdit {"
            "    color: black; "
            "    border: none; "
            "    border-bottom: 4px solid #a6a6a6; "
            "    font-size: 20px;"
            "}"
            "QLineEdit:focus {"
            "    border-bottom: 4px solid #ffbd59;"
            "}"
        )
        self.lineEdit_2.setObjectName("lineEdit_2")
        
        self.lineEdit_1 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_1.setGeometry(QtCore.QRect(154, 554, 648, 51))
        self.lineEdit_1.setStyleSheet(
            "QLineEdit {"
            "    color: black; "
            "    border: none; "
            "    border-bottom: 4px solid #a6a6a6; "
            "    font-size: 20px;"
            "}"
            "QLineEdit:focus {"
            "    border-bottom: 4px solid #ffbd59;"
            "}"
        )
        self.lineEdit_1.setObjectName("lineEdit_1")
        
        # Gunakan HoverButton sebagai push button dengan efek hover
        self.pushButton_4 = HoverButton(Dialog)
        self.pushButton_4.setGeometry(QtCore.QRect(10, 20, 111, 101))
        self.pushButton_4.setStyleSheet(
            "border-image: url(C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/ASSETS/BUTTON/BACK.png);"
        )
        self.pushButton_4.setText("")
        self.pushButton_4.setObjectName("pushButton_4")
        
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(-4, 0, 1611, 901))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/ASSETS//BACKGROUND/9.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(154, 724, 648, 51))
        self.lineEdit_3.setStyleSheet(
            "QLineEdit {"
            "    color: black; "
            "    border: none; "
            "    border-bottom: 4px solid #a6a6a6; "
            "    font-size: 20px;"
            "}"
            "QLineEdit:focus {"
            "    border-bottom: 4px solid #ffbd59;"
            "}"
        )
        self.lineEdit_3.setObjectName("lineEdit_3")
        
        self.pushButton_1 = HoverButton(Dialog)
        self.pushButton_1.setGeometry(QtCore.QRect(848, 364, 601, 129))
        self.pushButton_1.setStyleSheet(
            "QPushButton {"
            "    border-image: url(C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/ASSETS/BUTTON/TAMBAH_JADWAL.png);"
            "}"
        )
        self.pushButton_1.setText("")
        self.pushButton_1.setObjectName("pushButton_1")
        
        self.pushButton_2 = HoverButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(848, 507, 601, 129))
        self.pushButton_2.setStyleSheet(
            "QPushButton {"
            "    border-image: url(C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/ASSETS/BUTTON/UPDATE_JADWAL.png);"
            "}"
        )
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")
        
        self.pushButton_3 = HoverButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(848, 652, 601, 129))
        self.pushButton_3.setStyleSheet(
            "QPushButton {"
            "    border-image: url(C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/ASSETS/BUTTON/HAPUS_JADWAL.png);"
            "}"
        )
        self.pushButton_3.setText("")
        self.pushButton_3.setObjectName("pushButton_3")
        
        self.comboBox_2 = QtWidgets.QComboBox(Dialog)
        self.comboBox_2.setGeometry(QtCore.QRect(154, 382, 648, 51))
        self.comboBox_2.setStyleSheet(
            "QComboBox {"
            "    color: black;"
            "    border: none;"
            "    border-bottom: 4px solid #a6a6a6;"
            "    font-size: 20px;"
            "    padding: 5px 10px;"
            "    background: transparent;"
            "    padding-right: 40px;"
            "}"
            "QComboBox:focus {"
            "    border-bottom: 4px solid #ffbd59;"
            "}"
            "QComboBox::drop-down {"
            "    border: none;"
            "    width: 30px;"
            "    subcontrol-origin: padding;"
            "    subcontrol-position: center right;"
            "}"
            "QComboBox::down-arrow {"
            "    image: url(C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/ASSETS/BUTTON/ARROW.png);"
            "    width: 50px;"
            "    height: 50px;"
            "    margin-right: 20px;"
            "}"
        )
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        
        self.comboBox_3 = QtWidgets.QComboBox(Dialog)
        self.comboBox_3.setGeometry(QtCore.QRect(154, 467, 648, 51))
        self.comboBox_3.setStyleSheet(
            "QComboBox {"
            "    color: black;"
            "    border: none;"
            "    border-bottom: 4px solid #a6a6a6;"
            "    font-size: 20px;"
            "    padding: 5px 10px;"
            "    background: transparent;"
            "    padding-right: 40px;"
            "}"
            "QComboBox:focus {"
            "    border-bottom: 4px solid #ffbd59;"
            "}"
            "QComboBox::drop-down {"
            "    border: none;"
            "    width: 30px;"
            "    subcontrol-origin: padding;"
            "    subcontrol-position: center right;"
            "}"
            "QComboBox::down-arrow {"
            "    image: url(C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/ASSETS/BUTTON/ARROW.png);"
            "    width: 50px;"
            "    height: 50px;"
            "    margin-right: 20px;"
            "}"
        )
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        
        # Atur urutan tampilan widget
        self.label.raise_()
        self.lineEdit_2.raise_()
        self.lineEdit_1.raise_()
        self.pushButton_4.raise_()
        self.lineEdit_3.raise_()
        self.pushButton_1.raise_()
        self.pushButton_2.raise_()
        self.pushButton_3.raise_()
        self.comboBox_2.raise_()
        self.comboBox_3.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Splash Screen"))
        self.lineEdit_2.setText(_translate("Dialog", "Masukkan Jam Awal (Format: HH:MM)"))
        self.lineEdit_1.setText(_translate("Dialog", "Masukkan Hari (Contoh: Monday)"))
        self.lineEdit_3.setText(_translate("Dialog", "Masukkan Jam Akhir (Format: HH:MM)"))
        self.comboBox_2.setItemText(0, _translate("Dialog", "POLI JANTUNG"))
        self.comboBox_2.setItemText(1, _translate("Dialog", "POLI MATA"))
        self.comboBox_2.setItemText(2, _translate("Dialog", "POLI THT-KL"))
        self.comboBox_2.setItemText(3, _translate("Dialog", "POLI SARAF"))
        self.comboBox_2.setItemText(4, _translate("Dialog", "POLI ANAK"))
        self.comboBox_3.setItemText(0, _translate("Dialog", "Dr. Asep (Kardiolog)"))
        self.comboBox_3.setItemText(1, _translate("Dialog", "Dr. Ahmad (Oftalmolog)"))
        self.comboBox_3.setItemText(2, _translate("Dialog", "Dr. Messi (Spesialis THT-KH)"))
        self.comboBox_3.setItemText(3, _translate("Dialog", "Dr. Jajang (Neurolog)"))
        self.comboBox_3.setItemText(4, _translate("Dialog", "Dr. Radhit (Pediatrik Gawat Darurat)"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())