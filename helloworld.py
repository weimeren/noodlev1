import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from set import Ui_Set


class myform(QDialog, Ui_Set):
	def __init__(self, parent=None):
		super(myform, self).__init__(parent)
		self.setupUi(self)
		# 用来保存时间产生的
		self.setting = QSettings("mysetting.ini", QSettings.IniFormat)
		# 连接所有信号与槽
		self.signalsolt()
		# 读取上次保存的时间参数配置ini
		self.init_setting()

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
		pass

	# 退出窗体
	def esc_Press(self):
		self.done(True)



if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = myform()
	window.show()
	print("这是个改变")
	print("这是个例子")
	sys.exit(app.exec_())
