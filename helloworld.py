from login import Ui_Login
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys


class myform(Ui_Login):
    def __init__(self, parent=None):
        super(myform,self).__init__(parent)
        self.setupUi(self)
        self.BTesc.clicked.connect(self.esc)
        self.BTlogin.clicked.connect(self.login)

        
        
    
    #点击登陆按钮，验证密码是否正确，正确这进入主界面，错误则弹出错误窗口
    def login(self):
        QMessageBox.warning(self, "警告", "密码或用户名错误，请重新输入")
        pass
    #点击退出按钮后，登陆对话框退出
    def esc(self):
        print("这是退出的按钮")
        self.done(1)
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = myform()
    window.show()
    print("这是个例子")
    sys.exit(app.exec_())
    



