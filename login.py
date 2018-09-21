# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Login(QtWidgets.QDialog):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(444, 566)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Login.sizePolicy().hasHeightForWidth())
        Login.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/user.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Login.setWindowIcon(icon)
        Login.setStyleSheet("background-image: url(:/img/login.jpg);")
        self.LEusername = QtWidgets.QLineEdit(Login)
        self.LEusername.setGeometry(QtCore.QRect(98, 222, 287, 42))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LEusername.sizePolicy().hasHeightForWidth())
        self.LEusername.setSizePolicy(sizePolicy)
        self.LEusername.setStyleSheet("font: 75 16pt \"Arial\";")
        self.LEusername.setObjectName("LEusername")
        self.LEpassword = QtWidgets.QLineEdit(Login)
        self.LEpassword.setGeometry(QtCore.QRect(98, 295, 287, 42))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LEpassword.sizePolicy().hasHeightForWidth())
        self.LEpassword.setSizePolicy(sizePolicy)
        self.LEpassword.setStyleSheet("font: 75 16pt \"Arial\";")
        self.LEpassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.LEpassword.setObjectName("LEpassword")
        self.BTlogin = QtWidgets.QPushButton(Login)
        self.BTlogin.setGeometry(QtCore.QRect(58, 413, 328, 50))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BTlogin.sizePolicy().hasHeightForWidth())
        self.BTlogin.setSizePolicy(sizePolicy)
        self.BTlogin.setStyleSheet("font: 16pt \"楷体\";\n"
"background-color: rgb(238, 238, 238);\n"
"color: rgb(34, 128, 183);")
        self.BTlogin.setObjectName("BTlogin")
        self.LBtime = QtWidgets.QLabel(Login)
        self.LBtime.setGeometry(QtCore.QRect(2, 545, 16, 16))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LBtime.sizePolicy().hasHeightForWidth())
        self.LBtime.setSizePolicy(sizePolicy)
        self.LBtime.setStyleSheet("font: 75 9pt \"Arial\";\n"
"color: rgb(255, 255, 255);")
        self.LBtime.setAlignment(QtCore.Qt.AlignCenter)
        self.LBtime.setObjectName("LBtime")
        self.checkBox = QtWidgets.QCheckBox(Login)
        self.checkBox.setGeometry(QtCore.QRect(58, 374, 18, 18))
        self.checkBox.setText("")
        self.checkBox.setObjectName("checkBox")

        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "后台管理"))
        self.BTlogin.setText(_translate("Login", "登陆"))
        self.LBtime.setText(_translate("Login", "12"))

