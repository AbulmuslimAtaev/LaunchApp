# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget

# класс для приветсввия образованный от .ui файла
class WelcomeFromUi(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(871, 723)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.checkBox = QtWidgets.QCheckBox(Form)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox.setFont(font)
        self.checkBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkBox.setCheckable(True)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 1, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 1, 2, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(r"pics\авы1.jpg"))
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.checkBox.setText(_translate("Form", "Больше не показывать"))
        self.pushButton.setText(_translate("Form", "OK"))


class Welcome(QWidget, WelcomeFromUi):  # наследуемый класс
    def __init__(self):
        super(Welcome, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Приветсвие")
        self.show()
        self.pushButton.clicked.connect(self.pushed)  # обращению к методу при нажатии OK

    def pushed(self):
        if self.checkBox.isChecked():  # если стоит галочка на "не показывать больше"
            with open("data/flag.txt", "w", encoding="utf-8") as f:  # то в файл записывается три точки(как флаг)
                f.write("...")
        self.hide()
