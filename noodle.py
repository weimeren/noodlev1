#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################

from PyQt5.QtCore import (QSettings,Qt,pyqtSignal,QSize,QCoreApplication)
from PyQt5.QtGui import QPixmap,QMovie,QPalette,QBrush,QCursor,QFont
from PyQt5.QtWidgets import (QApplication,QMessageBox,QLabel,QDialog,QWidget,QMenu)
import threading
import serial
import serial.tools.list_ports
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
from time import sleep
from login import Ui_Login
from set import Ui_Set
from mainform import MainForm
#####################################
#使用pyinstaller打包时总是提示找不到PyQt5.sip，在代码里面导入后打包成功from PyQt5 import sip
####################################
from PyQt5 import sip
import sys

# 主窗体
class MyMain(MainForm):
    # updata_singnal数据更新信号，剩余时间，出面碗数
    # display_singnal等待界面弹出
    # hide_singnal等待界面隐藏
    updata_singnal = pyqtSignal(int, int, int)
    display_singnal = pyqtSignal()
    hide_singnal = pyqtSignal()
    def __init__(self , parent=None):
        super(MyMain , self).__init__(parent)
        # 必须将ContextMenuPolicy设置为Qt.CustomContextMenu
        # 否则无法使用customContextMenuRequested信号
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

    # 添加右键按钮
    def showContextMenu(self):
        self.contextMenu = QMenu(self)
        self.login = self.contextMenu.addAction("login")
        self.login.triggered.connect(loginWindow.show)
        self.contextMenu.addAction(self.login)
        self.contextMenu.exec_(QCursor.pos())

    def modbus_plc(self,send_data = []):
        #初始化接受数据存储列表
        self.rcv_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # 通讯口COM1
        self.PORT = "COM1"
        try:
            # 通讯口COM1，波特率9600，8位数据位，无校验，1位停止位，无流控
            self.master = modbus_rtu.RtuMaster(
                serial.Serial(port=self.PORT, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0)
            )
            # 通讯超时时间1
            self.master.set_timeout(0.2)
            self.master.set_verbose(True)
        except Exception:
            print("没有对应串口")
            pass

        while (True):
            try:
                # Connect to the slave
                self.rcv_data = self.master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 10)
                # send some queries
                # logger.info(master.execute(1, cst.READ_COILS, 0, 10))
                # logger.info(master.execute(1, cst.READ_DISCRETE_INPUTS, 0, 8))
                # logger.info(master.execute(1, cst.READ_INPUT_REGISTERS, 100, 3))
                # logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 100, 12))
                # logger.info(master.execute(1, cst.WRITE_SINGLE_COIL, 7, output_value=1))
                # logger.info(master.execute(1, cst.WRITE_SINGLE_REGISTER, 100, output_value=54))
                # logger.info(master.execute(1, cst.WRITE_MULTIPLE_COILS, 0, output_value=[1, 1, 0, 1, 1, 0, 1, 1]))
                self.master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 10, output_value=send_data)

            except Exception:
                # logger.error("%s- Code=%d", exc, exc.get_exception_code())
                pass
            if self.rcv_data[0] >= 1:
                self.display_singnal.emit()
            else:
                self.hide_singnal.emit()
            print(self.rcv_data[1])
            self.updata_singnal.emit(self.rcv_data[1], self.rcv_data[2], self.rcv_data[3])
            print("haha")
            sleep(0.5)

# 登陆窗体类
class Mylogin(Ui_Login):

    loginsignal = pyqtSignal()
    def __init__(self,parent=None):
        super(Mylogin,self).__init__(parent)
        self.setupUi(self)
        #设置登陆窗体为模态
        self.setWindowModality(Qt.ApplicationModal)
        self.BTesc.clicked.connect(self.esc)
        self.BTlogin.clicked.connect(self.login)

    #点击登陆按钮，验证密码是否正确，正确这进入主界面，错误则弹出错误窗口
    def login(self):
        """用户名不区分大小写，密码为数字或者字母，但验证正确时弹出调试窗口"""
        setWindow.show()
        if self.LEpassword.text() == "123" and  self.LEusername.text().lower() == "admin":
            setWindow.show()
            self.done(1)
            self.loginsignal.emit()
        else:
            QMessageBox.warning(self, "警告", "密码或用户名错误，请重新输入")
    #点击退出按钮后，登陆对话框退出
    def esc(self):
        print("这是退出的按钮")
        self.done(1)

    def loginshow(self):
        self.show()


# 设置与调试窗体
class Myset(QDialog, Ui_Set):
    def __init__(self, parent=None):
        super(Myset, self).__init__(parent)
        self.setupUi(self)
        # 用来保存时间产生的
        self.setting = QSettings("mysetting.ini", QSettings.IniFormat)
        # 连接所有信号与槽
        self.signalsolt()
        # 读取上次保存的时间参数配置ini
        self.init_setting()
        # 发送的数据
        self.send_data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]


    # 保存设置到的时间参数
    def Mysetting(self):
        self.setting.setValue("/time/heat_time", self.heat_time.value())
        self.setting.setValue("/time/water_into_time", self.water_into_time.value())
        self.setting.setValue("/time/water_out_time", self.water_out_time.value())
        self.setting.setValue("/time/open_door_time", self.open_door_time.value())
        self.setting.setValue("/time/sesame_time", self.sesame_time.value())
        self.setting.setValue("/time/sauce_time", self.sauce_time.value())
        self.setting.setValue("/time/pepper_time", self.pepper_time.value())

    # 程序开启读取ini配置，完成参数初始化
    def init_setting(self):
        time = ["0", "0", "0", "0", "0", "0", "0", "0"]
        time[0] = self.setting.value("/time/heat_time", 30.0)
        time[1] = self.setting.value("/time/water_into_time", 8.0)
        time[2] = self.setting.value("/time/water_out_time", 6.0)
        time[3] = self.setting.value("/time/open_door_time", 5.0)
        time[4] = self.setting.value("/time/sesame_time", 4.0)
        time[5] = self.setting.value("/time/sauce_time", 1.0)
        time[6] = self.setting.value("/time/pepper_time", 1.0)
        self.heat_time.setValue(float(time[0]))
        self.water_into_time.setValue(float(time[1]))
        self.water_out_time.setValue(float(time[2]))
        self.open_door_time.setValue(float(time[3]))
        self.sesame_time.setValue(float(time[4]))
        self.sauce_time.setValue(float(time[5]))
        self.pepper_time.setValue(float(time[6]))

    # 按钮的信号与槽链接
    def signalsolt(self):
        # 当改变spinbox的值后触发self.Mysetting把值写入ini配置文件
        self.heat_time.valueChanged.connect(self.Mysetting)
        self.water_into_time.valueChanged.connect(self.Mysetting)
        self.water_out_time.valueChanged.connect(self.Mysetting)
        self.open_door_time.valueChanged.connect(self.Mysetting)
        self.sesame_time.valueChanged.connect(self.Mysetting)
        self.sauce_time.valueChanged.connect(self.Mysetting)
        self.pepper_time.valueChanged.connect(self.Mysetting)
        # 把所有按钮与对应槽函数连接
        self.x_lift.toggled.connect(self.x_lift_Press)
        self.x_right.toggled.connect(self.x_right_Press)
        self.y_up.toggled.connect(self.y_up_Press)
        self.y_down.toggled.connect(self.y_down_Press)
        self.z_cw.toggled.connect(self.z_cw_Press)
        self.z_ccw.toggled.connect(self.z_ccw_Press)
        self.f_open.toggled.connect(self.f_open_Press)
        self.f_close.toggled.connect(self.f_close_Press)
        self.b_open.toggled.connect(self.b_open_Press)
        self.b_close.toggled.connect(self.b_close_Press)
        self.p_shrink.toggled.connect(self.p_shrink_Press)
        self.p_stretch.toggled.connect(self.p_stretch_Press)
        self.i_shrink.toggled.connect(self.i_shrink_Press)
        self.i_stretch.toggled.connect(self.i_stretch_Press)
        self.start.toggled.connect(self.start_Press)
        self.unlock.toggled.connect(self.unlock_Press)
        self.x_home.toggled.connect(self.x_home_Press)
        self.y_home.toggled.connect(self.y_home_Press)
        self.z_home.toggled.connect(self.z_home_Press)
        self.noodle_reset.toggled.connect(self.noodle_reset_Press)
        self.sauce_reset.toggled.connect(self.sauce_reset_Press)
        self.water_reset.toggled.connect(self.water_reset_Press)
        self.esc.clicked.connect(self.esc_Press)


    # 调试按钮按下的功能
    def x_lift_Press(self):
        if self.x_lift.isChecked():
            self.send_data[0] = 1
        else:
            self.send_data[0] = 0

    def x_right_Press(self):
        if self.x_right.isChecked():
            self.send_data[1] = 1
        else:
            self.send_data[1] = 0

    def y_up_Press(self):
        if self.y_up.isChecked():
            self.send_data[2] = 1
        else:
            self.send_data[2] = 0

    def y_down_Press(self):
        if self.y_down.isChecked():
            self.send_data[3] = 1
        else:
            self.send_data[3] = 0

    def z_cw_Press(self):
        if self.z_cw.isChecked():
            self.send_data[4] = 1
        else:
            self.send_data[4] = 0

    def z_ccw_Press(self):
        if self.z_ccw.isChecked():
            self.send_data[5] = 1
        else:
            self.send_data[5] = 0

    def f_open_Press(self):
        if self.f_open.isChecked():
            self.send_data[6] = 1
        else:
            self.send_data[6] = 0

    def f_close_Press(self):
        if self.f_close.isChecked():
            self.send_data[7] = 1
        else:
            self.send_data[7] = 0

    def b_open_Press(self):
        if self.b_open.isChecked():
            self.send_data[8] = 1
        else:
            self.send_data[8] = 0

    def b_close_Press(self):
        if self.b_close.isChecked():
            self.send_data[9] = 1
        else:
            self.send_data[9] = 0

    def i_shrink_Press(self):
        if self.i_shrink.isChecked():
            self.send_data[10] = 1
        else:
            self.send_data[10] = 0

    def i_stretch_Press(self):
        if self.i_stretch.isChecked():
            self.send_data[11] = 1
        else:
            self.send_data[11] = 0

    def p_shrink_Press(self):
        if self.p_shrink.isChecked():
            self.send_data[12] = 1
        else:
            self.send_data[12] = 0

    def p_stretch_Press(self):
        if self.p_shrink.isChecked():
            self.send_data[13] = 1
        else:
            self.send_data[13] = 0

    def start_Press(self):
        if self.start.isChecked():
            self.send_data[14] = 1
        else:
            self.send_data[14] = 0

    def unlock_Press(self):
        if self.unlock.isChecked():
            self.send_data[15] = 1
        else:
            self.send_data[15] = 0

    def x_home_Press(self):
        if self.x_home.isChecked():
            self.send_data[16] = 1
        else:
            self.send_data[16] = 0

    def y_home_Press(self):
        if self.y_home.isChecked():
            self.send_data[17] = 1
        else:
            self.send_data[17] = 0

    def z_home_Press(self):
        if self.z_home.isChecked():
            self.send_data[18] = 1
        else:
            self.send_data[18] = 0

    def noodle_reset_Press(self):
        if self.noodle_reset.isChecked():
            self.send_data[19] = 1
        else:
            self.send_data[19] = 0

    def water_reset_Press(self):
        if self.water_reset.isChecked():
            self.send_data[20] = 1
        else:
            self.send_data[20] = 0

    def sauce_reset_Press(self):
        if self.sauce_reset.isChecked():
            self.send_data[21] = 1
        else:
            self.send_data[21] = 0

    # 退出窗体
    def esc_Press(self):
        QCoreApplication.instance().quit()


# 程序入口
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 3个窗体，主窗体，登陆窗体，设置窗体
    mainWindow = MyMain()
    loginWindow = Mylogin()
    setWindow = Myset()
    # 使窗口大小和屏幕分辨率一样
    mainWindow.resize(1920, 1080)
    mainWindow.setWindowState(Qt.WindowFullScreen)
    # 创建一个子线程去进行modbus通讯
    modbus_thread = threading.Thread(target=mainWindow.modbus_plc,args=(setWindow.send_data,))
    modbus_thread.setDaemon(True)
    modbus_thread.start()
    # 进入循环
    mainWindow.show()
    sys.exit(app.exec_())
