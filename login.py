# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Login(QtWidgets.QDialog):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(400, 229)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Login.sizePolicy().hasHeightForWidth())
        Login.setSizePolicy(sizePolicy)
        self.label = QtWidgets.QLabel(Login)
        self.label.setGeometry(QtCore.QRect(30, 40, 101, 31))
        self.label.setStyleSheet("font: 16pt \"楷体\";")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Login)
        self.label_2.setGeometry(QtCore.QRect(60, 90, 81, 21))
        self.label_2.setStyleSheet("font: 16pt \"楷体\";")
        self.label_2.setObjectName("label_2")
        self.LEusername = QtWidgets.QLineEdit(Login)
        self.LEusername.setGeometry(QtCore.QRect(140, 40, 241, 31))
        self.LEusername.setObjectName("LEusername")
        self.LEpassword = QtWidgets.QLineEdit(Login)
        self.LEpassword.setGeometry(QtCore.QRect(140, 90, 241, 31))
        self.LEpassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.LEpassword.setObjectName("LEpassword")
        self.BTlogin = QtWidgets.QPushButton(Login)
        self.BTlogin.setGeometry(QtCore.QRect(30, 160, 101, 41))
        self.BTlogin.setStyleSheet("font: 12pt \"楷体\";")
        self.BTlogin.setObjectName("BTlogin")
        self.BTesc = QtWidgets.QPushButton(Login)
        self.BTesc.setGeometry(QtCore.QRect(280, 160, 101, 41))
        self.BTesc.setStyleSheet("font: 12pt \"楷体\";")
        self.BTesc.setObjectName("BTesc")
        
        

        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "欢迎登陆"))
        self.label.setText(_translate("Login", "用户名："))
        self.label_2.setText(_translate("Login", "密码："))
        self.LEusername.setPlaceholderText(_translate("Login", "Admin"))
        self.LEpassword.setPlaceholderText(_translate("Login", "\"密码只能数字和字母\""))
        self.BTlogin.setText(_translate("Login", "登陆"))
        self.BTesc.setText(_translate("Login", "退出"))

