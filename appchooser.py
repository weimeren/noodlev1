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


from PyQt5.QtCore import (QPointF, QPropertyAnimation, QRect, QRectF,
        QSequentialAnimationGroup, QSizeF, QState, QStateMachine, Qt,pyqtSignal,QSize,QCoreApplication,QBasicTimer)
from PyQt5.QtGui import QPixmap,QMovie,QPalette,QBrush,QCursor,QFont
from PyQt5.QtWidgets import (QApplication, QGraphicsScene, QGraphicsView,
        QGraphicsWidget,QLabel,QDialog,QPushButton,QHBoxLayout,QVBoxLayout,QSplitter,QWidget,QSpinBox,QProgressBar,QGroupBox,QGridLayout,QMenu
                             )
import threading
import serial
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
from time import sleep



class Pixmap(QGraphicsWidget):
    clicked = pyqtSignal()

    def __init__(self, pix, parent=None):
        super(Pixmap, self).__init__(parent)

        self.orig = QPixmap(pix)
        self.p = QPixmap(pix)

    def paint(self, painter, option, widget):
        painter.drawPixmap(QPointF(), self.p)

    def mousePressEvent(self, ev):
        self.clicked.emit()

    def setGeometry(self, rect):
        super(Pixmap, self).setGeometry(rect)

        if rect.size().width() > self.orig.size().width():
            self.p = self.orig.scaled(rect.size().toSize(),Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
        else:
            self.p = QPixmap(self.orig)


class MyLable(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super(MyLable, self).__init__(parent)

    def mousePressEvent(self, ev):
        self.clicked.emit()

    def MyEmit(self):
        self.clicked.emit()


def createStates(objects, selectedRect, parent):
    for obj in objects:
        state = QState(parent)
        state.assignProperty(obj, 'geometry', selectedRect)
        parent.addTransition(obj.clicked, state)


def createAnimations(objects, machine):
    for obj in objects:
        animation = QPropertyAnimation(obj, b'geometry', obj)
        machine.addDefaultAnimation(animation)


class MyClass(QWidget):
    updata = pyqtSignal(int,int,int)
    def __init__(self , parent=None):
        super(MyClass , self).__init__(parent)
        MyPalette = QPalette()
        data = "./img/beijin.jpg"
        MyPalette.setBrush(self.backgroundRole(), QBrush(QPixmap(data)))   # 设置背景图片
        self.setPalette(MyPalette)
        # self.setAutoFillBackground(True) # 不设置也可以
        # self.setAttribute(Qt.WA_TranslucentBackground)
        # 设置接受触摸屏
        self.setAttribute(Qt.WA_AcceptTouchEvents, True)
        # QCoreApplication.setAttribute(Qt.AA_SynthesizeTouchForUnhandledMouseEvents, True)  # 禁用将触摸事件转为鼠标事件
        # QCoreApplication.setAttribute(Qt.AA_SynthesizeMouseForUnhandledTouchEvents, True)

        #定义发送和接受PLC数据的列表
        self.send_data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.rcv_data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        # 必须将ContextMenuPolicy设置为Qt.CustomContextMenu
        # 否则无法使用customContextMenuRequested信号
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

        self.MyLable1 = MyLable(self)
        self.MyLable2 = MyLable(self)
        self.MyLable3 = MyLable(self)
        self.MyLable4 = MyLable(self)
        self.MyLable5 = MyLable(self)
        self.MyLable6 = MyLable(self)
        self.MyLable7 = MyLable(self)


        self.MyMovie1 = QMovie("./img/300二维码.gif")
        self.MyMovie2 = QMovie("./img/300购买.gif")
        self.MyMovie3 = QMovie("./img/300取料.gif")
        self.MyMovie4 = QMovie("./img/300注料.gif")
        self.MyMovie5 = QMovie("./img/300加热.gif")
        self.MyMovie6 = QMovie("./img/300取面.gif")
        self.MyMovie7 = QMovie("./img/300完成.gif")

        MySize = QSize(300,300)
        self.MyMovie1.setScaledSize(MySize)
        self.MyMovie2.setScaledSize(MySize)
        self.MyMovie3.setScaledSize(MySize)
        self.MyMovie4.setScaledSize(MySize)
        self.MyMovie5.setScaledSize(MySize)
        self.MyMovie6.setScaledSize(MySize)
        self.MyMovie7.setScaledSize(MySize)
        

        self.MyLable1.setMovie(self.MyMovie1)
        self.MyLable2.setMovie(self.MyMovie2)
        self.MyLable3.setMovie(self.MyMovie3)
        self.MyLable4.setMovie(self.MyMovie4)
        self.MyLable5.setMovie(self.MyMovie5)
        self.MyLable6.setMovie(self.MyMovie6)
        self.MyLable7.setMovie(self.MyMovie7)


        self.MyMovie1.start()
        self.MyMovie2.start()
        self.MyMovie3.start()
        self.MyMovie4.start()
        self.MyMovie5.start()
        self.MyMovie6.start()
        self.MyMovie7.start()

        # self.MyMovie1.stop()
        self.MyMovie2.stop()
        self.MyMovie3.stop()
        self.MyMovie4.stop()
        self.MyMovie5.stop()
        self.MyMovie6.stop()
        self.MyMovie7.stop()

        #等待界面图片和进度
        self.MyWait = MyLable(self)
        self.MyWait.setPixmap(QPixmap("img/wait.jpg"))
        self.MyWait.setGeometry(160, 140, 1600, 800)
        #倒计时
        self.Mytime = MyLable(self)
        self.Mytime.setGeometry(1050, 400, 300, 300)
        self.Mytime.setFont(QFont("Roman times",120,QFont.Bold))
        self.Mytime.setStyleSheet("color: rgb(255,255,255)")
        self.Mytime.setAlignment(Qt.AlignCenter)
        self.Mytime.setText("99")
        #调试组
        self.MyGroup = QGroupBox(self)
        self.MyGroup.setTitle("调试")
        self.MyGroup.setStyleSheet("background-color: rgb(221, 221, 221)")
        self.MyGroup.setGeometry(780, 180, 480, 720)
        self.MyGroupGLayout = QGridLayout(self.MyGroup)
        self.btn_lift = QPushButton(self.MyGroup)
        self.btn_right = QPushButton(self.MyGroup)
        self.btn_up = QPushButton(self.MyGroup)
        self.btn_down = QPushButton(self.MyGroup)
        self.btn_cw = QPushButton(self.MyGroup)
        self.btn_ccw = QPushButton(self.MyGroup)
        self.btn_start = QPushButton(self.MyGroup)
        self.btn_stop = QPushButton(self.MyGroup)
        self.btn_xhome = QPushButton(self.MyGroup)
        self.btn_yhome = QPushButton(self.MyGroup)
        self.btn_zhome = QPushButton(self.MyGroup)
        self.btn_reset = QPushButton(self.MyGroup)
        self.lab_num = QLabel(self.MyGroup)
        self.lab_num.setAlignment(Qt.AlignCenter)
        self.lab_wnum = QLabel(self.MyGroup)
        self.lab_wnum.setAlignment(Qt.AlignCenter)
        self.btn_wreset = QPushButton(self.MyGroup)




        self.btn_lift.setText("X_lift")
        self.btn_right.setText("X_right")
        self.btn_up.setText("Y_up")
        self.btn_down.setText("Y_down")
        self.btn_cw.setText("Z_cw")
        self.btn_ccw.setText("Z_ccw")
        self.btn_start.setText("start")
        self.btn_stop.setText("unlock")
        self.btn_xhome.setText("X_home")
        self.btn_yhome.setText("Y_home")
        self.btn_zhome.setText("Z_home")
        self.btn_reset.setText("Noodle_reset")
        self.btn_wreset.setText("Water_reset")
        self.lab_num.setText("99")
        self.lab_num.setFont(QFont("Microsoft YaHei", 30, 75))
        self.lab_num.setStyleSheet("background-color: rgb(255, 0, 0)")
        self.lab_wnum.setText("99")
        self.lab_wnum.setFont(QFont("Microsoft YaHei", 30, 75))
        self.lab_wnum.setStyleSheet("background-color: rgb(0, 255, 0)")



        self.btn_lift.setMinimumHeight(80)
        self.btn_right.setMinimumHeight(80)
        self.btn_up.setMinimumHeight(80)
        self.btn_down.setMinimumHeight(80)
        self.btn_cw.setMinimumHeight(80)
        self.btn_ccw.setMinimumHeight(80)
        self.btn_start.setMinimumHeight(80)
        self.btn_stop.setMinimumHeight(80)
        self.btn_xhome.setMinimumHeight(80)
        self.btn_yhome.setMinimumHeight(80)
        self.btn_zhome.setMinimumHeight(80)
        self.btn_reset.setMinimumHeight(80)
        self.btn_wreset.setMinimumHeight(80)
    
        #3######################
        self.btn_fo = QPushButton(self.MyGroup)
        self.btn_fc = QPushButton(self.MyGroup)
        self.btn_bo = QPushButton(self.MyGroup)
        self.btn_bc = QPushButton(self.MyGroup)
        self.btn_io = QPushButton(self.MyGroup)
        self.btn_ic = QPushButton(self.MyGroup)
        self.btn_po = QPushButton(self.MyGroup)
        self.btn_pc = QPushButton(self.MyGroup)
        self.btn_fo.setText("前门开")
        self.btn_fc.setText("前门关")
        self.btn_bo.setText("后门开")
        self.btn_bc.setText("后门关")
        self.btn_io.setText("料注出")
        self.btn_ic.setText("料抽入")
        self.btn_po.setText("推出")
        self.btn_pc.setText("推入")

        self.btn_fo.setMinimumHeight(80)
        self.btn_fc.setMinimumHeight(80)
        self.btn_bo.setMinimumHeight(80)
        self.btn_bc.setMinimumHeight(80)
        self.btn_io.setMinimumHeight(80)
        self.btn_ic.setMinimumHeight(80)
        self.btn_po.setMinimumHeight(80)
        self.btn_pc.setMinimumHeight(80)
        
        #################################
        self.MyGroupGLayout.addWidget(self.btn_lift,0,0)
        self.MyGroupGLayout.addWidget(self.btn_right,0,1)
        self.MyGroupGLayout.addWidget(self.btn_up,1,0)
        self.MyGroupGLayout.addWidget(self.btn_down,1,1)
        self.MyGroupGLayout.addWidget(self.btn_cw, 2, 0)
        self.MyGroupGLayout.addWidget(self.btn_ccw, 2, 1)
        self.MyGroupGLayout.addWidget(self.btn_fo, 3, 0)
        self.MyGroupGLayout.addWidget(self.btn_fc, 3, 1)
        self.MyGroupGLayout.addWidget(self.btn_bo, 4, 0)
        self.MyGroupGLayout.addWidget(self.btn_bc, 4, 1)
        self.MyGroupGLayout.addWidget(self.btn_io, 5, 0)
        self.MyGroupGLayout.addWidget(self.btn_ic, 5, 1)
        self.MyGroupGLayout.addWidget(self.btn_po, 6, 0)
        self.MyGroupGLayout.addWidget(self.btn_pc, 6, 1)
        self.MyGroupGLayout.addWidget(self.btn_start, 7, 0)
        self.MyGroupGLayout.addWidget(self.btn_stop, 7, 1)
        self.MyGroupGLayout.addWidget(self.btn_xhome, 0, 2)
        self.MyGroupGLayout.addWidget(self.btn_yhome, 1, 2)
        self.MyGroupGLayout.addWidget(self.btn_zhome, 2, 2)
        self.MyGroupGLayout.addWidget(self.lab_num,3,2)
        self.MyGroupGLayout.addWidget(self.btn_reset,4,2)
        self.MyGroupGLayout.addWidget(self.lab_wnum,5,2)
        self.MyGroupGLayout.addWidget(self.btn_wreset,6,2)




        self.btn_lift.pressed.connect(self.Xlift_Press)
        self.btn_lift.released.connect(self.Xlift_Release)
        self.btn_right.pressed.connect(self.Xright_Press)
        self.btn_right.released.connect(self.Xright_Release)
        self.btn_up.pressed.connect(self.Yup_Press)
        self.btn_up.released.connect(self.Yup_Release)
        self.btn_down.pressed.connect(self.Ydown_Press)
        self.btn_down.released.connect(self.Ydown_Release)
        self.btn_cw.pressed.connect(self.Zcw_Press)
        self.btn_cw.released.connect(self.Zcw_Release)
        self.btn_ccw.pressed.connect(self.Zccw_Press)
        self.btn_ccw.released.connect(self.Zccw_Release)

        self.btn_fo.pressed.connect(self.fo_Press)
        self.btn_fo.released.connect(self.fo_Release)
        self.btn_fc.pressed.connect(self.fc_Press)
        self.btn_fc.released.connect(self.fc_Release)
        self.btn_bo.pressed.connect(self.bo_Press)
        self.btn_bo.released.connect(self.bo_Release)
        self.btn_bc.pressed.connect(self.bc_Press)
        self.btn_bc.released.connect(self.bc_Release)
        self.btn_io.pressed.connect(self.io_Press)
        self.btn_io.released.connect(self.io_Release)
        self.btn_ic.pressed.connect(self.ic_Press)
        self.btn_ic.released.connect(self.ic_Release)
        self.btn_po.pressed.connect(self.po_Press)
        self.btn_po.released.connect(self.po_Release)
        self.btn_pc.pressed.connect(self.pc_Press)
        self.btn_pc.released.connect(self.pc_Release)

        self.btn_start.pressed.connect(self.Start_Press)
        self.btn_start.released.connect(self.Start_Release)

        self.btn_stop.pressed.connect(self.Stop_Press)
        self.btn_stop.released.connect(self.Stop_release)

        self.btn_xhome.pressed.connect(self.X_home_Press)
        self.btn_xhome.released.connect(self.X_home_release)
        self.btn_yhome.pressed.connect(self.Y_home_Press)
        self.btn_yhome.released.connect(self.Y_home_release)
        self.btn_zhome.pressed.connect(self.Z_home_Press)
        self.btn_zhome.released.connect(self.Z_home_release)
        self.btn_reset.pressed.connect(self.Noodle_reset_Press)
        self.btn_reset.released.connect(self.Noodle_reset_release)
        self.btn_wreset.pressed.connect(self.Water_reset_Press)
        self.btn_wreset.released.connect(self.Water_reset_release)
        

        self.MyGroup.setVisible(False)

    #调试按钮按下的功能
    def Xlift_Press(self):
        self.send_data[0] = 1
        print(self.send_data[0])

    def Xright_Press(self):
        self.send_data[1] = 1

    def Yup_Press(self):
        self.send_data[2] = 1

    def Ydown_Press(self):
        self.send_data[3] = 1

    def Zcw_Press(self):
        self.send_data[4] = 1

    def Zccw_Press(self):
        self.send_data[5] = 1

    def fo_Press(self):
        self.send_data[6] = 1

    def fc_Press(self):
        self.send_data[7] = 1

    def bo_Press(self):
        self.send_data[8] = 1

    def bc_Press(self):
        self.send_data[9] = 1

    def io_Press(self):
        self.send_data[10] = 1

    def ic_Press(self):
        self.send_data[11] = 1

    def po_Press(self):
        self.send_data[12] = 1

    def pc_Press(self):
        self.send_data[13] = 1

    def Start_Press(self):
        self.send_data[14] = 1

    def Stop_Press(self):
        self.send_data[15] = 1

    def X_home_Press(self):
        self.send_data[16] = 1
    
    def Y_home_Press(self):
        self.send_data[17] = 1
    
    def Z_home_Press(self):
        self.send_data[18] = 1
    
    def Noodle_reset_Press(self):
        self.send_data[19] = 1
    
    def Water_reset_Press(self):
        self.send_data[20] = 1
    

     # 调试按钮释放的功能

    def Xlift_Release(self):
        self.send_data[0] = 0
        print(self.send_data[0])
    def Xright_Release(self):
        self.send_data[1] = 0

    def Yup_Release(self):
        self.send_data[2] = 0

    def Ydown_Release(self):
        self.send_data[3] = 0

    def Zcw_Release(self):
        self.send_data[4] = 0

    def Zccw_Release(self):
        self.send_data[5] = 0

    def fo_Release(self):
        self.send_data[6] = 0

    def fc_Release(self):
        self.send_data[7] = 0

    def bo_Release(self):
        self.send_data[8] = 0

    def bc_Release(self):
        self.send_data[9] = 0

    def io_Release(self):
        self.send_data[10] = 0

    def ic_Release(self):
        self.send_data[11] = 0

    def po_Release(self):
        self.send_data[12] = 0

    def pc_Release(self):
        self.send_data[13] = 0

    def Start_Release(self):
        self.send_data[14] = 0

    def Stop_release(self):
        self.send_data[15] = 0

    def X_home_release(self):
        self.send_data[16] = 0
    
    def Y_home_release(self):
        self.send_data[17] = 0
    
    def Z_home_release(self):
        self.send_data[18] = 0
    
    def Noodle_reset_release(self):
        self.send_data[19] = 0
    
    def Water_reset_release(self):
        self.send_data[20] = 0    
    #显示等待界面
    def wait_dispaly(self):
        self.MyWait.setVisible(True)
        self.Mytime.setVisible(True)
    def wait_hide(self):
        self.MyWait.setVisible(False)
        self.Mytime.setVisible(False)
    #隐藏界面
    def hide(self):
        self.MyGroup.setVisible(False)
    #调试界面显示
    def debug_display(self):
        self.MyGroup.setVisible(True)

    def data_updata(self,i,j,k):
        self.Mytime.setText(str(i))
        self.lab_num.setText(str(j))
        self.lab_wnum.setText(str(k))


    #添加右键按钮
    def showContextMenu(self):
        self.contextMenu = QMenu(self)
        self.debug = self.contextMenu.addAction('Debug')
        self.wait = self.contextMenu.addAction("Wait")
        self.Hide = self.contextMenu.addAction("Hide")
        self.Esc = self.contextMenu.addAction("Esc")
        self.contextMenu.addAction(self.debug)
        self.contextMenu.addAction(self.wait)
        self.contextMenu.addAction(self.Hide)
        self.contextMenu.addAction(self.Esc)

        self.debug.triggered.connect(self.debug_display)
        self.wait.triggered.connect(self.wait_dispaly)
        self.Hide.triggered.connect(self.hide)
        self.Esc.triggered.connect(QCoreApplication.instance().quit)

        self.contextMenu.exec_(QCursor.pos())


    #通讯功能实现

    def send_rev(self):
        logger = modbus_tk.utils.create_logger("console")
        #通讯口COM2
        PORT = "COM1"
        #通讯口com3，波特率9600，8位数据位，无校验，1位停止位，无流控
        master = modbus_rtu.RtuMaster(
                    serial.Serial(port=PORT, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0)
                )
        #通讯超时时间1
        master.set_timeout(0.2)
        master.set_verbose(True)
        while(True):
            try:
                #Connect to the slave
                logger.info("connected")
                self.rcv_data= master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 10)
                logger.info(self.rcv_data)
                #send some queries
                #logger.info(master.execute(1, cst.READ_COILS, 0, 10))
                #logger.info(master.execute(1, cst.READ_DISCRETE_INPUTS, 0, 8))
                #logger.info(master.execute(1, cst.READ_INPUT_REGISTERS, 100, 3))
                #logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 100, 12))
                #logger.info(master.execute(1, cst.WRITE_SINGLE_COIL, 7, output_value=1))
                #logger.info(master.execute(1, cst.WRITE_SINGLE_REGISTER, 100, output_value=54))
                #logger.info(master.execute(1, cst.WRITE_MULTIPLE_COILS, 0, output_value=[1, 1, 0, 1, 1, 0, 1, 1]))
                logger.info(master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 10, output_value=self.send_data))

            except Exception :
                #logger.error("%s- Code=%d", exc, exc.get_exception_code())
                pass
            if self.rcv_data[0] >=1 :
                self.wait_dispaly()
            else:
                self.wait_hide()
            print(self.rcv_data[1])
            self.updata.emit(self.rcv_data[1],self.rcv_data[2],self.rcv_data[3])
            sleep(0.5)

    def MyFuc(self):
        machine = QStateMachine(self)
        state1 = QState(machine)
        machine.setInitialState(state1)

        # State 1.
        state1.assignProperty(self.MyLable1, 'geometry', QRectF(810, 180, 300, 300))
        state1.assignProperty(self.MyLable2, 'geometry', QRectF(10, 661, 300, 300))
        state1.assignProperty(self.MyLable3, 'geometry', QRectF(330, 661, 300, 300))
        state1.assignProperty(self.MyLable4, 'geometry', QRectF(650, 661, 300, 300))
        state1.assignProperty(self.MyLable5, 'geometry', QRectF(970, 661, 300, 300))
        state1.assignProperty(self.MyLable6, 'geometry', QRectF(1290, 661, 300, 300))
        state1.assignProperty(self.MyLable7, 'geometry', QRectF(1610, 661, 300, 300))

        machine.start()


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = MyClass()
    window.MyFuc()
    window.updata.connect(window.data_updata)
    #使窗口大小和屏幕分辨率一样
    window.resize(1920, 1080)
    window.setWindowState(Qt.WindowFullScreen)
    #创建一个子线程去进行modbus通讯
    modbus_thread = threading.Thread(target=window.send_rev)
    modbus_thread.setDaemon(True)
    modbus_thread.start()
    #进入循环
    window.show()

    sys.exit(app.exec_())
