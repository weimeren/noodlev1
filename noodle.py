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

from PyQt5.QtCore import (QSettings,Qt,pyqtSignal,QSize,QCoreApplication,QTimer,QDateTime)
from PyQt5.QtGui import QPixmap,QMovie,QPalette,QBrush,QCursor,QFont
from PyQt5.QtWidgets import (QApplication,QMessageBox,QLabel,QDialog,QWidget,QMenu,QStyleFactory)
import threading
import serial
import serial.tools.list_ports
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
from time import sleep
from login import Ui_Login
from set import Ui_Set
from mainform import MainForm
import MySqlHelper
import hashlib
#####################################
#使用pyinstaller打包时总是提示找不到PyQt5.sip，在代码里面导入后打包成功from PyQt5 import sip
#或者在打包完成后，对应目录下添加PyQt5.sip.pyd文件也可以运行
####################################
from PyQt5 import sip
import sys

# 主窗体
class MyMain(MainForm):
    # updata_singnal数据更新信号，剩余时间，出面碗数
    updata_singnal = pyqtSignal(int, int, int, int)

    def __init__(self , parent=None):
        super(MyMain , self).__init__(parent)
        # 必须将ContextMenuPolicy设置为Qt.CustomContextMenu
        # 否则无法使用customContextMenuRequested信号
        # self.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.customContextMenuRequested.connect(self.showContextMenu)
        #更新倒计时时间
        self.updata_singnal.connect(self.update_display)


    def update_display(self,time,noodle,water,sauce):
        self.Mytime.setText(str(time))
        setWindow.noodle_num.setText(str(noodle))
        setWindow.water_num.setText(str(water))
        setWindow.sauce_num.setText(str(sauce))


    def wait_display(self):
        self.MyWait.setVisible(True)
        self.Mytime.setVisible(True)


    def wait_hide(self):
        self.MyWait.setVisible(False)
        self.Mytime.setVisible(False)

    # 添加右键按钮
    # def showContextMenu(self):
    #     self.contextMenu = QMenu(self)
    #     self.login = self.contextMenu.addAction("login")
    #     self.login.triggered.connect(loginWindow.show)
    #     self.contextMenu.addAction(self.login)
    #     self.contextMenu.exec_(QCursor.pos())


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
                self.wait_display()
            else:
                self.wait_hide()
            print(self.rcv_data[1])
            self.updata_singnal.emit(self.rcv_data[1], self.rcv_data[2], self.rcv_data[3], self.rcv_data[4])
            print("haha")
            sleep(0.2)


# 登陆窗体类
class Mylogin(Ui_Login):

    loginsignal = pyqtSignal()
    def __init__(self,parent=None):
        super(Mylogin,self).__init__(parent)
        self.setupUi(self)
        #设置登陆窗体为模态
        self.setWindowModality(Qt.ApplicationModal)
        self.BTlogin.clicked.connect(self.login)
        #设置窗体样式
        MyPalette = QPalette()
        data = "./img/login.jpg"
        MyPalette.setBrush(self.backgroundRole(), QBrush(QPixmap(data)))  # 设置背景图片
        self.setPalette(MyPalette)
        #设置倒计时，20s后未登陆则进入主界面
        self.stopwatch = QTimer(self)
        self.stopwatch.timeout.connect(self.showtime)
        self.stopwatch.start(1000)
        self.second = 20
        #开机时间记录到mysql
        self.get_now_time()
        #创建一个1min计时器，每分钟更新机器状态数据到数据库
        self.updateTimer = QTimer(self)
        self.updateTimer.timeout.connect(self.update_machine)
        self.updateTimer.start(10000)
        #连接状态status一分钟变化一次心跳
        self.connect_status = True
    #每分钟更新程序状态数据到数据库
    def update_machine(self):
        if self.connect_status ==True:
            self.connect_status=False
        else:
            self.connect_status=True
        update_data = [int(setWindow.sauce_num.text()),
                       self.connect_status,
                       int(setWindow.noodle_num.text()),
                       int(setWindow.water_num.text()),
                       setWindow.heat_time.value(),
                       setWindow.water_into_time.value()
                       ]
        update_data_sql = "update machines set state=%s, conn=%s, noodlenum=%s,waternum=%s,heattime=%s,injectwatertime=%s where sn='30038935'"
        self.sqlhelp.cud(update_data_sql,update_data)
    #每次程序启动把启动时间写到数据库
    def get_now_time(self):
        # 连接阿里云mysql数据库，公网IP为47.96.104.151，端口3306，数据库noodle,表user
        # 表user-->>id，username,password,loigntime,idDelete
        self.sqlhelp = MySqlHelper.MySqlHelper('47.96.104.151', 3306, 'root', 'mysql', 'noodle')
        machinesql = "select * from machines where sn='30038935'"
        machinelist = self.sqlhelp.get(machinesql, [])
        starttime = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        starttimesql = "update machines set starttime=%s where sn='30038935'"
        self.sqlhelp.cud(starttimesql,[starttime])
        print(starttime)

    #点击登陆按钮，验证密码是否正确，正确这进入主界面，错误则弹出错误窗口
    def login(self):
        """用户名不区分大小写，密码为数字或者字母，但验证正确时弹出调试窗口"""
        # setWindow.show()
        #使用shal加密，占用40个字符
        shal = hashlib.sha1()
        username = self.LEusername.text()
        password = self.LEpassword.text()
        shal.update(password.encode('utf-8'))
        passwordshal = shal.hexdigest()
        #登陆用的sql语句
        loginsql = "select * from user where username = %s "
        list= self.sqlhelp.get(loginsql,[username])
        if not list :
            QMessageBox.warning(self, "警告", "用户名错误，请重新输入")
        elif list[0][2]!=passwordshal:
            QMessageBox.warning(self, "警告", "密码错误，请重新输入")
        else:
            setWindow.show()
            self.stopwatch.timeout.disconnect(self.showtime)
            self.LEpassword.clear()
            self.done(1)
    #时间到达后未登陆则进入主界面
    def showtime(self):
        self.second = self.second-1
        self.LBtime.setText(str(self.second))
        if self.second ==0:
            self.second = 20
            self.done(1)
            mainWindow.show()
            self.stopwatch.timeout.disconnect(self.showtime)





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
        self.setStyle(QStyleFactory.create("Fusion"))

    #显示当前时间
    def showtime(self):
        self.LBbottom.setText(QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss"))
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
        self.x_lift.pressed.connect(self.x_lift_Press)
        self.x_right.pressed.connect(self.x_right_Press)
        self.y_up.pressed.connect(self.y_up_Press)
        self.y_down.pressed.connect(self.y_down_Press)
        self.z_cw.pressed.connect(self.z_cw_Press)
        self.z_ccw.pressed.connect(self.z_ccw_Press)
        self.f_open.pressed.connect(self.f_open_Press)
        self.f_close.pressed.connect(self.f_close_Press)
        self.b_open.pressed.connect(self.b_open_Press)
        self.b_close.pressed.connect(self.b_close_Press)
        self.p_shrink.pressed.connect(self.p_shrink_Press)
        self.p_stretch.pressed.connect(self.p_stretch_Press)
        self.i_shrink.pressed.connect(self.i_shrink_Press)
        self.i_stretch.pressed.connect(self.i_stretch_Press)
        self.start.pressed.connect(self.start_Press)
        self.unlock.pressed.connect(self.unlock_Press)
        self.x_home.pressed.connect(self.x_home_Press)
        self.y_home.pressed.connect(self.y_home_Press)
        self.z_home.pressed.connect(self.z_home_Press)
        self.noodle_reset.pressed.connect(self.noodle_reset_Press)
        self.sauce_reset.pressed.connect(self.sauce_reset_Press)
        self.water_reset.pressed.connect(self.water_reset_Press)
        #按钮被释放
        self.x_lift.released.connect(self.x_lift_release)
        self.x_right.released.connect(self.x_right_release)
        self.y_up.released.connect(self.y_up_release)
        self.y_down.released.connect(self.y_down_release)
        self.z_cw.released.connect(self.z_cw_release)
        self.z_ccw.released.connect(self.z_ccw_release)
        self.f_open.released.connect(self.f_open_release)
        self.f_close.released.connect(self.f_close_release)
        self.b_open.released.connect(self.b_open_release)
        self.b_close.released.connect(self.b_close_release)
        self.p_shrink.released.connect(self.p_shrink_release)
        self.p_stretch.released.connect(self.p_stretch_release)
        self.i_shrink.released.connect(self.i_shrink_release)
        self.i_stretch.released.connect(self.i_stretch_release)
        self.start.released.connect(self.start_release)
        self.unlock.released.connect(self.unlock_release)
        self.x_home.released.connect(self.x_home_release)
        self.y_home.released.connect(self.y_home_release)
        self.z_home.released.connect(self.z_home_release)
        self.noodle_reset.released.connect(self.noodle_reset_release)
        self.sauce_reset.released.connect(self.sauce_reset_release)
        self.water_reset.released.connect(self.water_reset_release)

        #退出按钮
        self.esc.clicked.connect(self.esc_Press)


    # 调试按钮按下的功能
    def x_lift_Press(self):
            self.send_data[0] = 1

    def x_right_Press(self):
            self.send_data[1] = 1

    def y_up_Press(self):
            self.send_data[2] = 1

    def y_down_Press(self):
            self.send_data[3] = 1

    def z_cw_Press(self):
            self.send_data[4] = 1

    def z_ccw_Press(self):
            self.send_data[5] = 1

    def f_open_Press(self):
            self.send_data[6] = 1

    def f_close_Press(self):
            self.send_data[7] = 1

    def b_open_Press(self):
            self.send_data[8] = 1

    def b_close_Press(self):
            self.send_data[9] = 1

    def i_shrink_Press(self):
            self.send_data[10] = 1

    def i_stretch_Press(self):
            self.send_data[11] = 1

    def p_shrink_Press(self):
            self.send_data[12] = 1

    def p_stretch_Press(self):
            self.send_data[13] = 1

    def start_Press(self):
            self.send_data[14] = 1

    def unlock_Press(self):
            self.send_data[15] = 1

    def x_home_Press(self):
            self.send_data[16] = 1

    def y_home_Press(self):
            self.send_data[17] = 1

    def z_home_Press(self):
            self.send_data[18] = 1

    def noodle_reset_Press(self):
            self.send_data[19] = 1

    def water_reset_Press(self):
            self.send_data[20] = 1

    def sauce_reset_Press(self):
            self.send_data[21] = 1

    def x_lift_release(self):
            self.send_data[0] = 0

    def x_right_release(self):
            self.send_data[1] = 0

    def y_up_release(self):
            self.send_data[2] = 0

    def y_down_release(self):
            self.send_data[3] = 0

    def z_cw_release(self):
            self.send_data[4] = 0

    def z_ccw_release(self):
            self.send_data[5] = 0

    def f_open_release(self):
            self.send_data[6] = 0

    def f_close_release(self):
            self.send_data[7] = 0

    def b_open_release(self):
            self.send_data[8] = 0

    def b_close_release(self):
            self.send_data[9] = 0

    def i_shrink_release(self):
            self.send_data[10] = 0

    def i_stretch_release(self):
            self.send_data[11] = 0

    def p_shrink_release(self):
            self.send_data[12] = 0

    def p_stretch_release(self):
            self.send_data[13] = 0

    def start_release(self):
            self.send_data[14] = 0

    def unlock_release(self):
            self.send_data[15] = 0

    def x_home_release(self):
            self.send_data[16] = 0

    def y_home_release(self):
            self.send_data[17] = 0

    def z_home_release(self):
            self.send_data[18] = 0

    def noodle_reset_release(self):
            self.send_data[19] = 0

    def water_reset_release(self):
            self.send_data[20] = 0

    def sauce_reset_release(self):
            self.send_data[21] = 0

    # 退出窗体
    def esc_Press(self):
        QCoreApplication.instance().quit()


# 程序入口
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    # 3个窗体，主窗体，登陆窗体，设置窗体
    mainWindow = MyMain()
    loginWindow = Mylogin()
    setWindow = Myset()
    loginWindow.stopwatch.timeout.connect(setWindow.showtime)
    # 使窗口大小和屏幕分辨率一样
    mainWindow.resize(1920, 1080)
    mainWindow.setWindowState(Qt.WindowFullScreen)
    # 创建一个子线程去进行modbus通讯
    modbus_thread = threading.Thread(target=mainWindow.modbus_plc,args=(setWindow.send_data,))
    modbus_thread.setDaemon(True)
    modbus_thread.start()
    # 进入循环
    # mainWindow.show()
    loginWindow.show()
    sys.exit(app.exec_())
