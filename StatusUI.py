# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/StatusUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 157)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        Form.setFont(font)
        Form.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        Form.setStyleSheet("background-color: rgb(24, 25, 28);")
        self.label_playing = QtWidgets.QLabel(Form)
        self.label_playing.setGeometry(QtCore.QRect(10, 10, 151, 16))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(7)
        font.setBold(True)
        font.setWeight(75)
        self.label_playing.setFont(font)
        self.label_playing.setStyleSheet("color: rgb(185, 187, 190);")
        self.label_playing.setObjectName("label_playing")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 40, 100, 100))
        self.label.setStyleSheet("border: 2px solid gray;\n"
"border-radius: 5px;")
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/discord/discord_icon"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(140, 40, 221, 91))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_playing_2 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(7)
        font.setBold(True)
        font.setWeight(75)
        self.label_playing_2.setFont(font)
        self.label_playing_2.setStyleSheet("color: rgb(185, 187, 190);")
        self.label_playing_2.setObjectName("label_playing_2")
        self.verticalLayout.addWidget(self.label_playing_2)
        self.le_details = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(7)
        font.setBold(False)
        font.setWeight(50)
        self.le_details.setFont(font)
        self.le_details.setStyleSheet("color: rgb(185, 187, 190);")
        self.le_details.setText("")
        self.le_details.setObjectName("le_details")
        self.verticalLayout.addWidget(self.le_details)
        self.le_state = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(7)
        font.setBold(False)
        font.setWeight(50)
        self.le_state.setFont(font)
        self.le_state.setStyleSheet("color: rgb(185, 187, 190);")
        self.le_state.setText("")
        self.le_state.setObjectName("le_state")
        self.verticalLayout.addWidget(self.le_state)
        self.le_timestamp = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(7)
        font.setBold(False)
        font.setWeight(50)
        self.le_timestamp.setFont(font)
        self.le_timestamp.setStyleSheet("color: rgb(185, 187, 190);")
        self.le_timestamp.setText("")
        self.le_timestamp.setObjectName("le_timestamp")
        self.verticalLayout.addWidget(self.le_timestamp)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_playing.setText(_translate("Form", "PLAYING A GAME"))
        self.label_playing_2.setText(_translate("Form", "Playstation 5"))
