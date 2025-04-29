import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QTableWidgetItem
from Ui_System import Ui_MainWindow  #导入你写的界面类
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtCore import Qt
from control import Control
 
class MyMainWindow(QMainWindow,Ui_MainWindow): #这里也要记得改
    def __init__(self,parent =None):
        super(MyMainWindow,self).__init__(parent)
        self.setupUi(self)
        
        self.logText.setVisible(True)
        self.logText.setReadOnly(True)
        self.box_motor.addItem("请选择电机")
        self.box_motor.addItems(["关节电机:a1","关节电机:a2","关节电机:a3","关节电机:a4","关节电机:a5","关节电机:a6","关节电机:a7",
                                "机构电机:b1","机构电机:b2","机构电机:b3","机构电机:b4","机构电机:b5","机构电机:b6","机构电机:b7"])
        
        for i in range(1,15):
            if i<=7:
                index=f"a{i}"
            else:
                index=f"b{i-7}"
            item_data = QTableWidgetItem(index)
            self.table.setItem(i-1,0,item_data)

        # 不可编辑表格
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)   # 禁止编辑
        self.table.setSelectionMode(QAbstractItemView.NoSelection)     # 禁止选中  
        self.table.setFocusPolicy(Qt.NoFocus)                   # 禁止焦点（防止虚线框） 
        self.table.horizontalHeader().setHighlightSections(False)
        self.table.verticalHeader().setHighlightSections(False)
        self.table.horizontalHeader().setHighlightSections(False)
        self.table.horizontalHeader().setSectionsClickable(False)
        self.table.verticalHeader().setHighlightSections(False)
        self.table.verticalHeader().setSectionsClickable(False)
        # 不可编辑的文本框相关
        for line_edit in [self.line1, self.line2, self.line3,self.line4,self.line5,self.line6,self.line7,self.line8,self.line_x,self.line_y,self.line_z,
                          self.line_Rp,self.line_Rr,self.line_Ry,self.line_Fx,self.line_Fy,self.line_Fz,self.line_Tx,self.line_Ty,self.line_Tz]:
             line_edit.setReadOnly(True)
       
        # 按钮相关逻辑
        self.control = Control(self)
        # 按钮函数绑定
        self.button_connect.clicked.connect(self.control.open_connect)
        self.button_camera.clicked.connect(self.control.open_camera)
        self.button_motor.clicked.connect(self.control.open_motor)
        self.button_force.clicked.connect(self.control.open_force)
        self.button_start.clicked.connect(self.control.open_start)
        self.button_forward.clicked.connect(self.control.open_forward)
        self.button_reverse.clicked.connect(self.control.open_reverse)
        self.button_stop.clicked.connect(self.control.open_stop)
        self.button_reset.clicked.connect(self.control.open_reset)
        self.button_zero.clicked.connect(self.control.open_zero)
        self.button_move.clicked.connect(self.control.open_move)
        self.button1.clicked.connect(self.control.open_machineopen)
        self.button2.clicked.connect(self.control.open_dooropen)
        self.button3.clicked.connect(self.control.open_capture)
        self.button4.clicked.connect(self.control.open_doorclose)
        self.button5.clicked.connect(self.control.open_dock)
        self.button6.clicked.connect(self.control.open_doormoveopen)
        self.button7.clicked.connect(self.control.open_machineclose)
        self.button8.clicked.connect(self.control.open_target)

        self.ip_edit.setText("192.168.111.20")
    # 日志显示
    def addLogs(self, *args, split=''):
       
        newLog = split.join(args)
        self.logText.appendPlainText(newLog)

        print(newLog)
       
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())    