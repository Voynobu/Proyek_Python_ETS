# WindowEditPoli.py
# Nama: Rangga Muhamad Fajar
# Kelas: 1A - D4
# NIM: 241524026
# Desc: - 
#       - 


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1600, 900)
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.lineEdit_1 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_1.setGeometry(QtCore.QRect(963, 430, 481, 71))
        self.lineEdit_1.setStyleSheet("QLineEdit {\n"
"                color: black; \n"
"                border: none; \n"
"                border-bottom: 4px solid #a6a6a6; \n"
"                font-size: 28px;\n"
"            }\n"
"            QLineEdit:focus {\n"
"                border-bottom: 4px solid #ffbd59;\n"
"            }")
        self.lineEdit_1.setObjectName("lineEdit_1")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 20, 111, 101))
        self.pushButton_3.setStyleSheet("border-image: url(C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/ASSETS/BUTTON/BACK.png);")
        self.pushButton_3.setText("")
        self.pushButton_3.setObjectName("pushButton_3")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(-4, 0, 1611, 901))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../ASSETS/RESULT/EDIT_POLI.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.pushButton_1 = QtWidgets.QPushButton(Dialog)
        self.pushButton_1.setGeometry(QtCore.QRect(911, 547, 591, 87))
        self.pushButton_1.setStyleSheet("QPushButton{\n"
"    border-image: url(C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/ASSETS/BUTTON/TAMBAH_POLI.png);\n"
"}")
        self.pushButton_1.setText("")
        self.pushButton_1.setObjectName("pushButton_1")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(911, 663, 591, 87))
        self.pushButton_2.setStyleSheet("QPushButton{\n"
"    border-image: url(C:/Users/Rangga/Documents/KULIAH/SEMESTER 2/PROYEK 1/TUBES PRA ETS/ASSETS/BUTTON/HAPUS_POLI.png);\n"
"}")
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(100, 238, 601, 571))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.tableWidget.setFont(font)
        self.tableWidget.setStyleSheet("QHeaderView::section {\n"
"    background-color: #00A9E0; /* Biru */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    font-size: 14px;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QTableWidget {\n"
"    gridline-color: gray;\n"
"    border: 1px solid gray;\n"
"}\n"
"QTableWidget::item {\n"
"    padding: 10px;\n"
"}\n"
"\n"
"")
        self.tableWidget.setLineWidth(1)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setAutoScrollMargin(15)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setRowCount(5)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        item.setFont(font)
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        item.setFont(font)
        self.tableWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(2, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(3, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(4, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(4, 1, item)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(300)
        self.tableWidget.horizontalHeader().setHighlightSections(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(109)
        self.tableWidget.verticalHeader().setMinimumSectionSize(18)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.label.raise_()
        self.lineEdit_1.raise_()
        self.pushButton_3.raise_()
        self.pushButton_1.raise_()
        self.pushButton_2.raise_()
        self.tableWidget.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Splash Screen"))
        self.lineEdit_1.setText(_translate("Dialog", "Masukkan Nama Poli!"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "NO"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "POLI"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item.setText(_translate("Dialog", "1"))
        item = self.tableWidget.item(0, 1)
        item.setText(_translate("Dialog", "POLI JANTUNG"))
        item = self.tableWidget.item(1, 0)
        item.setText(_translate("Dialog", "2"))
        item = self.tableWidget.item(1, 1)
        item.setText(_translate("Dialog", "POLI ANAK"))
        item = self.tableWidget.item(2, 0)
        item.setText(_translate("Dialog", "3"))
        item = self.tableWidget.item(2, 1)
        item.setText(_translate("Dialog", "POLI GIGI"))
        item = self.tableWidget.item(3, 0)
        item.setText(_translate("Dialog", "4"))
        item = self.tableWidget.item(3, 1)
        item.setText(_translate("Dialog", "POLI MATA"))
        item = self.tableWidget.item(4, 0)
        item.setText(_translate("Dialog", "5"))
        item = self.tableWidget.item(4, 1)
        item.setText(_translate("Dialog", "POLI THT"))
        self.tableWidget.setSortingEnabled(__sortingEnabled)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
