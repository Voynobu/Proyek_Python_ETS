import json
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class HoverOpacityFilter(QtCore.QObject):
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Enter:
            if obj.graphicsEffect():
                obj.graphicsEffect().setOpacity(0.7)
        elif event.type() == QtCore.QEvent.Leave:
            if obj.graphicsEffect():
                obj.graphicsEffect().setOpacity(1.0)
        return super().eventFilter(obj, event)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1600, 900)
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # ------ LINE EDIT (Nama Dokter) ------
        self.lineEdit_1 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_1.setGeometry(QtCore.QRect(910, 401, 608, 51))
        self.lineEdit_1.setStyleSheet(
            "QLineEdit {"
            "    color: black; "
            "    border: none; "
            "    border-bottom: 4px solid #a6a6a6; "
            "    font-size: 24px;"
            "}"
            "QLineEdit:focus {"
            "    border-bottom: 4px solid #ffbd59;"
            "}"
        )
        self.lineEdit_1.setObjectName("lineEdit_1")
        self.lineEdit_1.setPlaceholderText("Masukkan Nama Dokter!")

        # ------ LINE EDIT (Spesialisasi Dokter) ------
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(910, 501, 608, 51))
        self.lineEdit_2.setStyleSheet(
            "QLineEdit {"
            "    color: black; "
            "    border: none; "
            "    border-bottom: 4px solid #a6a6a6; "
            "    font-size: 24px;"
            "}"
            "QLineEdit:focus {"
            "    border-bottom: 4px solid #ffbd59;"
            "}"
        )
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setPlaceholderText("Masukkan Spesialisasi Dokter!")

        # ------ BACK BUTTON ------
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 20, 111, 101))
        self.pushButton_3.setStyleSheet(
            "border-image: url(C:/ASSETS/BUTTON/BACK.png);"
        )
        self.pushButton_3.setText("")
        self.pushButton_3.setObjectName("pushButton_3")

        # ------ BACKGROUND LABEL ------
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(-4, 0, 1611, 901))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("C:/ASSETS/BACKGROUND/11.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        # ------ TOMBOL TAMBAH DOKTER ------
        self.pushButton_1 = QtWidgets.QPushButton(Dialog)
        self.pushButton_1.setGeometry(QtCore.QRect(891, 593, 648, 101))
        self.pushButton_1.setStyleSheet(
            "QPushButton {"
            "    border-image: url(C:/ASSETS/BUTTON/TAMBAH_DOKTER.png);"
            "}"
        )
        self.pushButton_1.setText("")
        self.pushButton_1.setObjectName("pushButton_1")

        # ------ TOMBOL HAPUS DOKTER ------
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(891, 711, 648, 101))
        self.pushButton_2.setStyleSheet(
            "QPushButton {"
            "    border-image: url(C:/ASSETS/BUTTON/HAPUS_DOKTER.png);"
            "}"
        )
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")

        # ------ COMBOBOX (Pilih Poli) ------
        self.comboBox_2 = QtWidgets.QComboBox(Dialog)
        self.comboBox_2.setGeometry(QtCore.QRect(910, 301, 608, 51))
        self.comboBox_2.setStyleSheet(
            "QComboBox {"
            "    color: black;"
            "    border: none;"
            "    border-bottom: 4px solid #a6a6a6;"
            "    font-size: 24px;"
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
            "    image: url(C:/ASSETS/BUTTON/ARROW.png);"
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

        # ------ TABLE VIEW ------
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
        self.tableView.setObjectName("tableView")

        # Urutan tampilan: background di bawah, kemudian komponen lainnya
        self.label.raise_()
        self.lineEdit_1.raise_()
        self.lineEdit_2.raise_()
        self.pushButton_3.raise_()
        self.pushButton_1.raise_()
        self.pushButton_2.raise_()
        self.comboBox_2.raise_()
        self.tableView.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # ------ INIT MODEL & LOAD DATA ------
        self.initModel()
        self.loadData()

        # --- Nonaktifkan interaksi langsung pada tabel ---
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

        # Atur ukuran kolom: kolom pertama fixed, kolom kedua dan ketiga stretch
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        self.tableView.setColumnWidth(0, 70)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        # ---- Tambahkan efek hover pada push button ----
        self.addHoverOpacity(self.pushButton_1)
        self.addHoverOpacity(self.pushButton_2)
        self.addHoverOpacity(self.pushButton_3)

    def addHoverOpacity(self, button):
        """
        Pasang QGraphicsOpacityEffect dan event filter HoverOpacityFilter
        pada sebuah tombol, agar opasitas berubah saat mouse hover.
        """
        effect = QtWidgets.QGraphicsOpacityEffect(button)
        effect.setOpacity(1.0)
        button.setGraphicsEffect(effect)

        hoverFilter = HoverOpacityFilter(button)
        button.installEventFilter(hoverFilter)

    def initModel(self):
        # Inisialisasi model dengan 3 kolom: NO, NAMA DOKTER, SPESIALISASI
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["NO", "NAMA DOKTER", "SPESIALISASI"])
        self.tableView.setModel(self.model)

    def loadData(self):
        # Contoh: load data dari file JSON "dokter_data.json"
        # Asumsikan struktur JSON: {"dokter": {"dr.john": "Jantung", "dr.smith": "Saraf", ...}}
        file_path = "dokter_data.json"
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
            dokter_data = data.get("dokter", {})

            self.model.setRowCount(0)
            row_num = 0
            for dokter_name, spesialisasi in dokter_data.items():
                if dokter_name.strip():
                    item_no = QStandardItem(str(row_num + 1))
                    item_no.setTextAlignment(QtCore.Qt.AlignCenter)

                    item_dokter = QStandardItem(dokter_name.capitalize())
                    item_dokter.setTextAlignment(QtCore.Qt.AlignCenter)

                    item_spesialisasi = QStandardItem(str(spesialisasi))
                    item_spesialisasi.setTextAlignment(QtCore.Qt.AlignCenter)

                    self.model.appendRow([item_no, item_dokter, item_spesialisasi])
                    row_num += 1

        except Exception as e:
            print("Error membaca file JSON:", e)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Splash Screen"))
        self.lineEdit_1.setText(_translate("Dialog", ""))
        self.lineEdit_2.setText(_translate("Dialog", ""))
        self.comboBox_2.setItemText(0, _translate("Dialog", "POLI JANTUNG"))
        self.comboBox_2.setItemText(1, _translate("Dialog", "POLI MATA"))
        self.comboBox_2.setItemText(2, _translate("Dialog", "POLI THT-KL"))
        self.comboBox_2.setItemText(3, _translate("Dialog", "POLI SARAF"))
        self.comboBox_2.setItemText(4, _translate("Dialog", "POLI ANAK"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
