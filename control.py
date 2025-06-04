from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from ads import TwinCat3_ADSserver
import pyads
import re
from video import VideoThread
from Servo import VisualServoThread
import time
from FTSensor.ForceThread import ForceThread

class Control:
    def __init__(self, ui):
        # 将 ui 的所有控件动态绑定到 self
        for name, widget in ui.__dict__.items():
            setattr(self, name, widget)  # 例如：self.button_camera = ui.button_camera
        
        # 初始化状态标志
        self.open_camera_flag = False
        self.connect_flag = False
        self.open_motor_flag = False
        self.open_force_flag = False

        self.open_start_flag = False
        self.open_forward_flag = True
        self.open_reverse_flag = True
        self.open_stop_flag = True
        self.open_reset_flag = True
        self.open_zero_flag = True
        self.open_move_flag = True

        self.open_machineopen_flag = False
        self.open_dooropen_flag = False
        self.open_doorclose_flag = False
        self.open_dock_flag = False
        self.open_doormoveopen_flag = False
        self.open_machineclose_flag = False
        self.open_target_flag = False
        self.open_servo_flag = False
        # 初始化连接
        self.tc3 = TwinCat3_ADSserver()
        
        
     # ---------------------总体控制相关函数-------------------------
    def open_connect(self):
        if self.connect_flag:
            self.connect_flag = False
            self.button_connect.setText("启动")
            # 指示灯颜色
            self.connect_led.setStyleSheet("""
            background-color:red;
            border-radius: 20px; 
            border: 1px solid gray;
            margin-top: 0px;
            """)
            self.button_connect.setStyleSheet("""
            background-color: #f3f3f3;
            color: black;
            padding: 5px 10px;
            border-left: 0px;
            border-top: 0px;
            border-right: 2px solid #a3a3a3;
            border-bottom: 2px solid #a3a3a3;
            margin-top: 0px;
        """)
            self.addLogs("Twincat连接关闭")
            self.tc3.stop_monitoring()
            self.tc3.variables={}
            self.tc3.close()
        else:
            try:
                self.connect_flag = True
                self.button_connect.setText("关闭")
                self.addLogs("Twincat连接开启")
                self.tc3.connect()
                self.add_adsvars()
                self.tc3.moving_signal.connect(self.value_changed)
                self.tc3.pos_signal.connect(self.value_changed)
                self.tc3.velo_signal.connect(self.value_changed)
                self.tc3.error_signal.connect(self.value_changed)
                self.tc3.eeposx_signal.connect(self.value_changed)
                self.tc3.eeposy_signal.connect(self.value_changed)
                self.tc3.eeposz_signal.connect(self.value_changed)
                self.tc3.eeposrx_signal.connect(self.value_changed)
                self.tc3.eeposry_signal.connect(self.value_changed)
                self.tc3.eeposrz_signal.connect(self.value_changed)
                self.tc3.JigouZhankai_State.connect(self.value_changed)
                self.tc3.CangMen_State.connect(self.value_changed)
                self.tc3.CangMen_State_Close.connect(self.value_changed)
                self.tc3.Zhuanyi_State.connect(self.value_changed)
                self.tc3.ZhuanyiCangmen_State.connect(self.value_changed)
                self.tc3.Jigoushoulong_State.connect(self.value_changed)
                self.tc3.Tuisong_State.connect(self.value_changed)

                self.tc3.start_monitoring()
                self.connect_led.setStyleSheet("""
                background-color: rgb(88, 214, 92);
                border-radius: 20px; 
                border: 1px solid gray;
                margin-top: 0px;
                """)
                self.button_connect.setStyleSheet("""
                background-color: gray;
                color: black;
                padding: 5px 10px;
                border-left: 0px;
                border-top: 0px;
                border-right: 2px solid #a3a3a3;
                border-bottom: 2px solid #a3a3a3;
                margin-top: 0px;
                """)
            except Exception as e:
                self.addLogs(str(e))

    def open_camera(self):
        if self.open_camera_flag:
            self.open_camera_flag = False
            self.button_camera.setText("开启相机")
            self.button_camera.setStyleSheet("""
            background-color: #f3f3f3;
            color: black;
            padding: 5px 10px;
            border-left: 0px;
            border-top: 0px;
            border-right: 2px solid #a3a3a3;
            border-bottom: 2px solid #a3a3a3;
            margin-top: 0px;
        """)
            self.addLogs("相机关闭")
            self.thread.stop_camera()
            self.VisionPictureRGB_2.setPixmap(QPixmap(""))
        else:
            self.addLogs("相机开启中")
            try:
                self.open_camera_flag = True
                self.button_camera.setText("关闭相机")
                self.button_camera.setStyleSheet("""
                background-color: gray;
                color: black;
                padding: 5px 10px;
                border-left: 0px;
                border-top: 0px;
                border-right: 2px solid #a3a3a3;
                border-bottom: 2px solid #a3a3a3;
                margin-top: 0px;
            """)
                self.addLogs("相机开启")
                self.thread = VideoThread()
                self.thread.change_pixmap_signal.connect(self.update_image)
                self.thread.start_camera()
            except Exception as e:
                self.addLogs(str(e))


    def open_motor(self):
        if self.open_motor_flag:
            self.open_motor_flag = False
            self.button_motor.setText("开启电机")
            self.button_motor.setStyleSheet("""
            background-color: #f3f3f3;
            color: black;
            padding: 5px 10px;
            border-left: 0px;
            border-top: 0px;
            border-right: 2px solid #a3a3a3;
            border-bottom: 2px solid #a3a3a3;
            margin-top: 0px;
        """)
            self.addLogs("电机关闭")
            self.tc3.write_by_name(f"GVL.Enable_Open", False, pyads.PLCTYPE_BOOL)
            self.box_motor.setEnabled(False)
        else:
            try:
                self.open_motor_flag = True
                self.button_motor.setText("关闭电机")
                self.button_motor.setStyleSheet("""
                background-color: gray;
                color: black;
                padding: 5px 10px;
                border-left: 0px;
                border-top: 0px;
                border-right: 2px solid #a3a3a3;
                border-bottom: 2px solid #a3a3a3;
                margin-top: 0px;
            """)
                self.addLogs("电机开启")
                self.tc3.write_by_name(f"GVL.Enable_Open", True, pyads.PLCTYPE_BOOL)
                self.box_motor.setEnabled(True)
            except Exception as e:
                self.addLogs(str(e))



    def open_force(self):
        ip_address = self.ip_edit.text().strip()
        if self.open_force_flag:
            self.open_force_flag = False
            self.button_force.setText("开启六维力")
            self.button_force.setStyleSheet("""
            background-color: #f3f3f3;
            color: black;
            padding: 5px 10px;
            border-left: 0px;
            border-top: 0px;
            border-right: 2px solid #a3a3a3;
            border-bottom: 2px solid #a3a3a3;
            margin-top: 0px;
        """)
            # self.ip_edit.clear()
            self.forceThread.stop()
            self.addLogs("六维力关闭")
        else:
            #后续双六维力判断
            if ip_address == "169.254.117.20":
                self.open_force_flag = True
                self.button_force.setText("关闭六维力")
                self.button_force.setStyleSheet("""
            background-color: gray;
            color: black;
            padding: 5px 10px;
            border-left: 0px;
            border-top: 0px;
            border-right: 2px solid #a3a3a3;
            border-bottom: 2px solid #a3a3a3;
            margin-top: 0px;
        """)
                self.forceThread = ForceThread(ip_address)
                self.forceThread._ft_data.connect(self.updateFT)
                self.forceThread.write_ft_data.connect(self.writeFT)
                self.forceThread.start()

                self.addLogs("六维力开启")
            else:
                print("六维力ip地址错误")
                self.addLogs("六维力ip地址错误")

    def updateFT(self, ft):
        if len(ft) == 6:
            self.line_Fx.setText(str(round(ft[0],3)))
            self.line_Fy.setText(str(round(ft[1],3)))
            self.line_Fz.setText(str(round(ft[2],3)))
            self.line_Tx.setText(str(round(ft[3],3)))
            self.line_Ty.setText(str(round(ft[4],3)))
            self.line_Tz.setText(str(round(ft[5],3)))

    def writeFT(self, ft):
        if len(ft) == 6:
            self.tc3.write_by_name(f"SiJueSiFu.FX", round(ft[0],3), pyads.PLCTYPE_LREAL)
            self.tc3.write_by_name(f"SiJueSiFu.FY", round(ft[1],3), pyads.PLCTYPE_LREAL)
            self.tc3.write_by_name(f"SiJueSiFu.FZ", round(ft[2],3), pyads.PLCTYPE_LREAL)
            self.tc3.write_by_name(f"SiJueSiFu.TX", round(ft[3],3), pyads.PLCTYPE_LREAL)
            self.tc3.write_by_name(f"SiJueSiFu.TY", round(ft[4],3), pyads.PLCTYPE_LREAL)
            self.tc3.write_by_name(f"SiJueSiFu.TZ", round(ft[5],3), pyads.PLCTYPE_LREAL)
    # ------------------------------单机调试相关函数-------------------------------------
    
    def open_start(self):
        if self.open_start_flag:
            self.open_start_flag = False
            self.box_motor.setEnabled(True)
            self.button_start.setText("启动")
            self.start_led.setStyleSheet("""
            background-color:red;
            border-radius: 20px; 
            border: 1px solid gray;
            margin-top: 0px;
            """)
            self.button_start.setStyleSheet("""
            background-color: #f3f3f3;
            color: black;
            padding: 5px 10px;
            border-left: 0px;
            border-top: 0px;
            border-right: 2px solid #a3a3a3;
            border-bottom: 2px solid #a3a3a3;
            margin-top: 0px;
        """)
            self.addLogs("单机调试关闭")
            select_axis = int(self.box_motor.currentIndex())
            self.tc3.write_by_name(f"Single.nSelect", select_axis, pyads.PLCTYPE_INT)
            self.tc3.write_by_name(f"Single.Enable_Open[{select_axis}]", False, pyads.PLCTYPE_BOOL)
        else:
            try:
                # 检查是否选择了电机
                select_axis = self.box_motor.currentIndex()
                if select_axis == 0:
                    self.addLogs("请先选择电机")
                    return
                self.open_start_flag = True
                self.box_motor.setEnabled(False)
                self.button_start.setText("关闭")
                self.addLogs(f"{select_axis}单机调试启动")
                self.tc3.write_by_name(f"Single.nSelect", select_axis, pyads.PLCTYPE_INT)
                self.tc3.write_by_name(f"Single.Enable_Open[{select_axis}]", True, pyads.PLCTYPE_BOOL)
                self.start_led.setStyleSheet("""
                background-color: rgb(88, 214, 92);
                border-radius: 20px; 
                border: 1px solid gray;
                margin-top: 0px;
                """)
                self.button_start.setStyleSheet("""
                background-color: gray;
                color: black;
                padding: 5px 10px;
                border-left: 0px;
                border-top: 0px;
                border-right: 2px solid #a3a3a3;
                border-bottom: 2px solid #a3a3a3;
                margin-top: 0px;
            """)
            except Exception as e:
                self.addLogs(str(e))


    def open_forward(self):
        if self.open_forward_flag:
            if not self.open_start_flag:
                self.addLogs("请先开启电机")
                return
            self.open_forward_flag = True
            self.button_forward.setText("正转")
            self.button_forward.setStyleSheet("""
            background-color: gray;
            color: black;
            padding: 5px 10px;
            border-left: 0px;
            border-top: 0px;
            border-right: 2px solid #a3a3a3;
            border-bottom: 2px solid #a3a3a3;
            margin-top: 0px;
        """)
            self.addLogs("电机正转")
            select_axis = self.box_motor.currentIndex()
        self.tc3.write_by_name(f"Single.Positive_Open[{select_axis}]", True, pyads.PLCTYPE_BOOL)
        self.button_reverse.setEnabled(False)
        self.button_move.setEnabled(False)
        self.button_zero.setEnabled(False)
        self.button_reset.setEnabled(False)
        self.button_start.setEnabled(False)

    def open_reverse(self):
        if self.open_reverse_flag:
            if not self.open_start_flag:
                self.addLogs("请先开启电机")
                return
            self.open_reverse_flag = True
            self.button_reverse.setText("反转")
            self.button_reverse.setStyleSheet("""
            background-color: gray;
            color: black;
            padding: 5px 10px;
            border-left: 0px;
            border-top: 0px;
            border-right: 2px solid #a3a3a3;
            border-bottom: 2px solid #a3a3a3;
            margin-top: 0px;
        """)
            self.addLogs("电机反转")
            select_axis = self.box_motor.currentIndex()
        self.tc3.write_by_name(f"Single.Negative_Open[{select_axis}]", True, pyads.PLCTYPE_BOOL)
        self.button_forward.setEnabled(False)
        self.button_move.setEnabled(False)
        self.button_zero.setEnabled(False)
        self.button_reset.setEnabled(False)
        self.button_start.setEnabled(False)
            
    def open_stop(self):
        if self.open_stop_flag:
            self.button_stop.setText("停止")
            self.button_stop.setStyleSheet("""
            background-color: #f3f3f3;
            color: black;
            padding: 5px 10px;
            border-left: 0px;
            border-top: 0px;
            border-right: 2px solid #a3a3a3;
            border-bottom: 2px solid #a3a3a3;
            margin-top: 0px;
        """)
            self.button_forward.setText("正转")
            self.button_forward.setStyleSheet("""
            background-color: #f3f3f3;
            color: black;
            padding: 5px 10px;
            border-left: 0px;
            border-top: 0px;
            border-right: 2px solid #a3a3a3;
            border-bottom: 2px solid #a3a3a3;
            margin-top: 0px;
            """)
            # 反转按钮变色
            self.button_reverse.setText("反转")
            self.button_reverse.setStyleSheet("""
            background-color: #f3f3f3;
            color: black;
            padding: 5px 10px;
            border-left: 0px;
            border-top: 0px;
            border-right: 2px solid #a3a3a3;
            border-bottom: 2px solid #a3a3a3;
            margin-top: 0px;
            """)
            # 复位按钮
            self.button_reset.setText("复位")
            self.button_reset.setStyleSheet("""
            background-color: #f3f3f3;
            color: black;
            padding: 5px 10px;
            border-left: 0px;
            border-top: 0px;
            border-right: 2px solid #a3a3a3;
            border-bottom: 2px solid #a3a3a3;
            margin-top: 0px;
            """)

            # 回零按钮
            self.button_zero.setText("回零")
            self.button_zero.setStyleSheet("""
            background-color: #f3f3f3;
            color: black;
            padding: 5px 10px;
            border-left: 0px;
            border-top: 0px;
            border-right: 2px solid #a3a3a3;
            border-bottom: 2px solid #a3a3a3;
            margin-top: 0px;
            """)

            # 移动按钮
            self.button_move.setText("移动")
            self.button_move.setStyleSheet("""
            background-color: #f3f3f3;
            color: black;
            padding: 5px 10px;
            border-left: 0px;
            border-top: 0px;
            border-right: 2px solid #a3a3a3;
            border-bottom: 2px solid #a3a3a3;
            margin-top: 0px;
            """)
            self.addLogs("电机停止")
            select_axis = self.box_motor.currentIndex()
        self.tc3.write_by_name(f"Single.stop_flag[{select_axis}]", True, pyads.PLCTYPE_BOOL)
        self.button_forward.setEnabled(True)
        self.button_reverse.setEnabled(True)
        self.button_move.setEnabled(True)
        self.button_zero.setEnabled(True)
        self.button_reset.setEnabled(True)
        self.button_start.setEnabled(True)

    def open_reset(self):
        if self.open_reset_flag:
            if not self.open_start_flag:
                self.addLogs("请先开启电机")
                return
            self.open_reset_flag = True
            self.button_reset.setText("复位")
            self.button_reset.setStyleSheet("""
            background-color: gray;
            color: black;
            padding: 5px 10px;
            border-left: 0px;
            border-top: 0px;
            border-right: 2px solid #a3a3a3;
            border-bottom: 2px solid #a3a3a3;
            margin-top: 0px;
        """)
            self.addLogs("电机复位")
            select_axis = self.box_motor.currentIndex()
        self.tc3.write_by_name(f"Single.reset_flag[{select_axis}]", True, pyads.PLCTYPE_BOOL)
        self.set_button_style(self.button_reset,False)

    def open_zero(self):
        if self.open_zero_flag:
            if not self.open_start_flag:
                self.addLogs("请先开启电机")
                return
            self.open_zero_flag = True
            self.button_zero.setText("回零")
            self.button_zero.setStyleSheet("""
            background-color: gray;
            color: black;
            padding: 5px 10px;
            border-left: 0px;
            border-top: 0px;
            border-right: 2px solid #a3a3a3;
            border-bottom: 2px solid #a3a3a3;
            margin-top: 0px;
        """)
            self.addLogs("电机回零")
            select_axis = self.box_motor.currentIndex()
        self.tc3.write_by_name(f"Single.home_flag[{select_axis}]", True, pyads.PLCTYPE_BOOL)
        self.set_button_style(self.button_zero,False)

    def open_move(self):
        if self.open_move_flag:
            position_text = self.p_edit.text().strip()
            speed_text = self.v_edit.text().strip()
            # --------------------------------------限制位置速度大小-------------------------------------------
            if not self.open_start_flag:
                self.addLogs("请先开启电机")
                return
             # 判断输入合法性
            if not position_text and not speed_text:
                self.addLogs("请输入位置和速度")
                return
            elif not position_text:
                self.addLogs("请输入位置")
                return
            elif not speed_text:
                self.addLogs("请输入速度")
                return
             # 限制范围判断（这部分按实际修改）
            try:
                position = float(position_text)
                speed = float(speed_text)
                
                # 检查位置和速度范围
                if position < -100 or position > 100:
                    self.addLogs("位置范围错误,请输入-100到100之间的值")
                    return
                    
                if speed < 0 or speed > 15:
                    self.addLogs("速度范围错误,请输入0到15之间的值")
                    return
                
            except ValueError:
                self.addLogs("输入错误，请输入有效的数字")
                return
            self.open_move_flag = True
            self.button_move.setText("移动")
            select_axis = self.box_motor.currentIndex()
            setpos = float(self.p_edit.text())
            setvelo = float(self.v_edit.text())
            self.tc3.write_by_name(f"Single.abs_Position[{select_axis}]", setpos, pyads.PLCTYPE_LREAL)
            self.tc3.write_by_name(f"Single.abs_Velocity[{select_axis}]", setvelo, pyads.PLCTYPE_LREAL)
            self.tc3.write_by_name(f"Single.abs_flag[{select_axis}]", True, pyads.PLCTYPE_BOOL)
            self.button_move.setStyleSheet("""
            background-color: gray;
            color: black;
            padding: 5px 10px;
            border-left: 0px;
            border-top: 0px;
            border-right: 2px solid #a3a3a3;
            border-bottom: 2px solid #a3a3a3;
            margin-top: 0px;
        """)
            self.addLogs(f"电机以{speed_text}m/s速度移动至({position_text})")
    # ------------------------分系统流程相关函数----------------------------
    def set_button_style(self, button, active):
        if active:
            button.setStyleSheet("""
                background-color: gray;
                color: black;
                padding: 5px 10px;
                border-left: 0px;
                border-top: 0px;
                border-right: 2px solid #a3a3a3;
                border-bottom: 2px solid #a3a3a3;
                margin-top: 0px;
            """)
        else:
            button.setStyleSheet("""
                background-color: #f3f3f3;
                color: black;
                padding: 5px 10px;
                border-left: 0px;
                border-top: 0px;
                border-right: 2px solid #a3a3a3;
                border-bottom: 2px solid #a3a3a3;
                margin-top: 0px;
            """)

    def set_led_style(self, led, active):
        if active:
            led.setStyleSheet("""
                background-color: rgb(88, 214, 92);
                border-radius: 15px; 
                border: 1px solid gray;
                margin-top: 0px;
            """)
        else:
            led.setStyleSheet("""
                background-color: red;
                border-radius: 15px; 
                border: 1px solid gray;
                margin-top: 0px;
            """)
       
    def open_machineopen(self):
            if not self.open_machineopen_flag:
                self.addLogs("机构展开流程开始")
                self.open_machineopen_flag = True
                self.set_button_style(self.button1, self.open_machineopen_flag)
                self.tc3.write_by_name(f"GVL.JigouZhanKai_Open", True, pyads.PLCTYPE_BOOL)
            else:
                JigouZhankai_State = self.tc3.read_by_name(f"GVL.JigouZhankai_State", pyads.PLCTYPE_BOOL)
                if JigouZhankai_State:
                    self.addLogs("机构展开流程结束")
                    self.set_led_style(self.led1, self.open_machineopen_flag)
            

    def open_dooropen(self):
            if not self.open_dooropen_flag:
                self.addLogs("捕获舱门打开流程开始")
                self.open_dooropen_flag = True
                self.set_button_style(self.button2, self.open_dooropen_flag)
                self.tc3.write_by_name(f"GVL.CangMen_Open", True, pyads.PLCTYPE_BOOL)
            else:
                CangMen_State = self.tc3.read_by_name(f"GVL.CangMen_State", pyads.PLCTYPE_BOOL)
                if CangMen_State:
                    self.addLogs("捕获舱门打开流程结束")
                    self.set_led_style(self.led2, self.open_dooropen_flag)

    def open_capture(self):
        if self.open_servo_flag:
            self.addLogs("捕获流程结束")
            self.servo.stop()
            self.open_servo_flag = False
            self.set_led_style(self.led3, not self.open_servo_flag)
            self.tc3.write_by_name(f"SiJueSiFu.RepythonX", 0, pyads.PLCTYPE_LREAL)
            self.tc3.write_by_name(f"SiJueSiFu.RepythonY", 0, pyads.PLCTYPE_LREAL)
            self.tc3.write_by_name(f"SiJueSiFu.RepythonZ", 0, pyads.PLCTYPE_LREAL)
        else:
            self.open_servo_flag = True
            self.addLogs("捕获流程开始")
            self.set_button_style(self.button3, self.open_servo_flag)
            self.servo = VisualServoThread(self, 0.6)
            self.servo.update_pose_signal.connect(self.write_delta)
            self.servo.finished_signal.connect(self.judge)
            self.servo.start_servo()


    def open_doorclose(self):
        if not self.open_doorclose_flag:
            self.addLogs("捕获舱门关闭流程开始")
            self.open_doorclose_flag = True
            self.set_button_style(self.button4, self.open_doorclose_flag)
            self.tc3.write_by_name(f"GVL.CangMen_Close", True, pyads.PLCTYPE_BOOL)
        else:
            CangMen_State_Close = self.tc3.read_by_name(f"GVL.CangMen_State_Close", pyads.PLCTYPE_BOOL)
            if CangMen_State_Close:
                self.addLogs("捕获舱门关闭流程结束")
                self.set_led_style(self.led4, self.open_doorclose_flag)
        
    def open_dock(self):
        if not self.open_dock_flag:
            self.addLogs("转移对接流程开始")
            self.open_dock_flag = True
            self.set_button_style(self.button5, self.open_dock_flag)
            self.tc3.write_by_name(f"GVL.Zhuanyi_Open", True, pyads.PLCTYPE_BOOL)
        else:
            Zhuanyi_State = self.tc3.read_by_name(f"GVL.Zhuanyi_State", pyads.PLCTYPE_BOOL)
            if Zhuanyi_State:
                self.addLogs("转移对接流程结束")
                self.set_led_style(self.led5, self.open_dock_flag)
                
            
    def open_doormoveopen(self):
        if not self.open_doormoveopen_flag:
            self.addLogs("转移舱门打开流程开始")
            self.open_doormoveopen_flag = True
            self.set_button_style(self.button6, self.open_doormoveopen_flag)
            self.tc3.write_by_name(f"GVL.ZhuanYiMen_Open", True, pyads.PLCTYPE_BOOL)
        else:
            ZhuanyiCangmen_State = self.tc3.read_by_name(f"GVL.ZhuanyiCangmen_State", pyads.PLCTYPE_BOOL)
            if ZhuanyiCangmen_State:
                self.addLogs("转移舱门打开流程结束")
                self.set_led_style(self.led6, self.open_doormoveopen_flag)
                    
            
    def open_machineclose(self):
        if not self.open_machineclose_flag:
            self.addLogs("机构收拢流程开始")
            self.open_machineclose_flag = True
            self.set_button_style(self.button7, self.open_machineclose_flag)
            self.tc3.write_by_name(f"GVL.Jigoushoulong_Open", True, pyads.PLCTYPE_BOOL)
        else:
            Jigoushoulong_State = self.tc3.read_by_name(f"GVL.Jigoushoulong_State", pyads.PLCTYPE_BOOL)
            if Jigoushoulong_State:
                self.addLogs("机构收拢流程结束")
                self.set_led_style(self.led7, self.open_machineclose_flag)
                    
            
    def open_target(self):
        if not self.open_target_flag:
            self.addLogs("目标推送流程开始")
            self.open_target_flag = True
            self.set_button_style(self.button8, self.open_target_flag)
            self.tc3.write_by_name(f"GVL.MubiaoTuisong", True, pyads.PLCTYPE_BOOL)
        else:
            Tuisong_State = self.tc3.read_by_name(f"GVL.Tuisong_State", pyads.PLCTYPE_BOOL)
            if Tuisong_State:
                self.addLogs("机构收拢流程结束")
                self.set_led_style(self.led8, self.open_target_flag)
                    
    
    # 日志显示相关
    def addLogs(self, *args, split=''):
       
        newLog = split.join(args)
        self.logText.appendPlainText(newLog)
       
        print(newLog)


    def add_adsvars(self):
        # 添加要监控的变量
        for i in range(14):
            self.tc3.add_variable(f"GVL.axis[{i+1}].Status.Moving", pyads.PLCTYPE_BOOL, self.value_changed)
            self.tc3.add_variable(f"GVL.axis[{i+1}].NcToPlc.ActVelo", pyads.PLCTYPE_LREAL, self.value_changed)
            self.tc3.add_variable(f"GVL.axis[{i+1}].NcToPlc.ActPos", pyads.PLCTYPE_LREAL, self.value_changed)
            self.tc3.add_variable(f"GVL.axis[{i+1}].NcToPlc.ErrorCode", pyads.PLCTYPE_UDINT, self.value_changed)

        self.tc3.add_variable(f"SiJueSiFu.ReaTwinX", pyads.PLCTYPE_LREAL, self.value_changed)
        self.tc3.add_variable(f"SiJueSiFu.ReaTwinY", pyads.PLCTYPE_LREAL, self.value_changed)
        self.tc3.add_variable(f"SiJueSiFu.ReaTwinZ", pyads.PLCTYPE_LREAL, self.value_changed)
        self.tc3.add_variable(f"SiJueSiFu.ReaTwinRX", pyads.PLCTYPE_LREAL, self.value_changed)
        self.tc3.add_variable(f"SiJueSiFu.ReaTwinRY", pyads.PLCTYPE_LREAL, self.value_changed)
        self.tc3.add_variable(f"SiJueSiFu.ReaTwinRZ", pyads.PLCTYPE_LREAL, self.value_changed)

        self.tc3.add_variable(f"GVL.JigouZhankai_State", pyads.PLCTYPE_BOOL, self.value_changed)
        self.tc3.add_variable(f"GVL.CangMen_State", pyads.PLCTYPE_BOOL, self.value_changed)
        self.tc3.add_variable(f"GVL.CangMen_State_Close", pyads.PLCTYPE_BOOL, self.value_changed)
        self.tc3.add_variable(f"GVL.Zhuanyi_State", pyads.PLCTYPE_BOOL, self.value_changed)
        self.tc3.add_variable(f"GVL.ZhuanyiCangmen_State", pyads.PLCTYPE_BOOL, self.value_changed)
        self.tc3.add_variable(f"GVL.Jigoushoulong_State", pyads.PLCTYPE_BOOL, self.value_changed)
        self.tc3.add_variable(f"GVL.Tuisong_State", pyads.PLCTYPE_BOOL, self.value_changed)

    # 定义回调函数
    def value_changed(self, name ,value):
        pattern = r'\d+'
        types = name.split(".")[-1]
        try:
            row = int(re.findall(pattern, name)[0])
            if types == "Moving":
                if float(self.table.item(row-1,2).text()) == 0:
                    astr = "停止状态"
                else:
                    astr = "运行状态"
                item_data = QtWidgets.QTableWidgetItem(astr)
                self.table.setItem(row-1,1,item_data)
            elif types == "ActVelo":
                item_data = QtWidgets.QTableWidgetItem(str(round(value,3)))
                self.table.setItem(row-1,2,item_data)
            elif types == "ActPos":
                item_data = QtWidgets.QTableWidgetItem(str(round(value,3)))
                self.table.setItem(row-1,3,item_data)
            elif types == "ErrorCode":
                item_data = QtWidgets.QTableWidgetItem(str(value))
                self.table.setItem(row-1,4,item_data)
        except:
            if types == "ReaTwinX":
                self.line_x.setText(str(round(value,3)))
            elif types == "ReaTwinY":
                self.line_y.setText(str(round(value,3)))
            elif types == "ReaTwinZ":
                self.line_z.setText(str(round(value,3)))
            elif types == "ReaTwinRX":
                self.line_Rr.setText(str(round(value,3)))
            elif types == "ReaTwinRY":
                self.line_Rp.setText(str(round(value,3)))
            elif types == "ReaTwinRZ":
                self.line_Ry.setText(str(round(value,3)))

            elif types == "Done":
                if value:
                    self.set_button_style(self.button_move, True)

            elif types == "JigouZhankai_State":
                if value and self.open_machineopen_flag:
                    self.open_machineopen()
                    self.open_machineopen_flag = False
            elif types == "CangMen_State":
                if value and self.open_dooropen_flag:
                    self.open_dooropen()
                    self.open_dooropen_flag = False
            elif types == "CangMen_State_Close":
                if value and self.open_doorclose_flag:
                    self.open_doorclose()
                    self.open_doorclose_flag = False
            elif types == "Zhuanyi_State":
                if value and self.open_dock_flag:
                    self.open_dock()
                    self.open_dock_flag = False
            elif types == "ZhuanyiCangmen_State":
                if value and self.open_doormoveopen_flag:
                    self.open_doormoveopen()
                    self.open_doormoveopen_flag = False
            elif types == "Jigoushoulong_State":
                if value and self.open_machineclose_flag:
                    self.open_machineclose()
                    self.open_machineclose_flag = False
            elif types == "Tuisong_State":
                if value and self.open_target_flag:
                    self.open_target()
                    self.open_target_flag = False
        

    def update_image(self, image):
        # Update the image_label with a new image
        self.VisionPictureRGB_2.setPixmap(QPixmap.fromImage(image))

    def write_delta(self, delta_world):
        self.tc3.write_by_name(f"SiJueSiFu.RepythonX", delta_world[0], pyads.PLCTYPE_LREAL)
        self.tc3.write_by_name(f"SiJueSiFu.RepythonY", delta_world[1], pyads.PLCTYPE_LREAL)
        self.tc3.write_by_name(f"SiJueSiFu.RepythonZ", delta_world[2], pyads.PLCTYPE_LREAL)

    def judge(self, finished_flag = False):
        if finished_flag:
            self.open_capture()

