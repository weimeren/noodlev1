#-*-conding:utf-8-*-

#############################################################################
#程序主窗体
#############################################################################

from PyQt5.QtCore import (Qt, QSize)
from PyQt5.QtGui import QPixmap, QMovie, QPalette, QBrush, QCursor, QFont
from PyQt5.QtWidgets import ( QLabel, QWidget, QMenu,QApplication)
# 主窗体
class MainForm(QWidget):

	def __init__(self, parent=None):
		super(MainForm, self).__init__(parent)
		MyPalette = QPalette()
		data = "./img/beijin.jpg"
		MyPalette.setBrush(self.backgroundRole(), QBrush(QPixmap(data)))  # 设置背景图片
		self.setPalette(MyPalette)
		# 设置接受触摸屏
		self.setAttribute(Qt.WA_AcceptTouchEvents, True)


		self.MyLable1 = QLabel(self)
		self.MyLable2 = QLabel(self)
		self.MyLable3 = QLabel(self)
		self.MyLable4 = QLabel(self)
		self.MyLable5 = QLabel(self)
		self.MyLable6 = QLabel(self)
		self.MyLable7 = QLabel(self)

		self.MyMovie1 = QMovie("./img/300二维码.gif")
		self.MyMovie2 = QMovie("./img/300购买.gif")
		self.MyMovie3 = QMovie("./img/300取料.gif")
		self.MyMovie4 = QMovie("./img/300注料.gif")
		self.MyMovie5 = QMovie("./img/300加热.gif")
		self.MyMovie6 = QMovie("./img/300取面.gif")
		self.MyMovie7 = QMovie("./img/300完成.gif")

		MySize = QSize(300, 300)
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

		self.MyLable1.setGeometry(810, 180, 300, 300)
		self.MyLable2.setGeometry(10, 661, 300, 300)
		self.MyLable3.setGeometry(330, 661, 300, 300)
		self.MyLable4.setGeometry(650, 661, 300, 300)
		self.MyLable5.setGeometry(970, 661, 300, 300)
		self.MyLable6.setGeometry(1290, 661, 300, 300)
		self.MyLable7.setGeometry(1610, 661, 300, 300)

		# 等待界面图片和进度
		self.MyWait = QLabel(self)
		self.MyWait.setPixmap(QPixmap("./img/wait.jpg"))
		self.MyWait.setGeometry(160, 140, 1600, 800)
		# 倒计时
		self.Mytime = QLabel(self)
		self.Mytime.setGeometry(1050, 400, 300, 300)
		self.Mytime.setFont(QFont("Roman times", 120, QFont.Bold))
		self.Mytime.setStyleSheet("color: rgb(255,255,255)")
		self.Mytime.setAlignment(Qt.AlignCenter)
		self.Mytime.setText("99")




if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	m = MainForm()
	m.show()
	sys.exit(app.exec_())



















