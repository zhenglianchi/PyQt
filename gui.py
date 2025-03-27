from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from camera import Camera
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
import time
import cv2
from ultralytics import YOLO
#from ads import TwinCat3_ADSserver
from Servo import servo

names = {
    0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus',
    6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant',
    11: 'stop sign', 12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat',
    16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear',
    22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag',
    27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard',
    32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove',
    36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle',
    40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl',
    46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli',
    51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair',
    57: 'couch', 58: 'potted plant', 59: 'bed', 60: 'dining table', 61: 'toilet',
    62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 66: 'keyboard',
    67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink',
    72: 'refrigerator', 73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors',
    77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush'
}

class VisualServoThread(QThread):
    update_pose_signal = pyqtSignal(list, list)

    def __init__(self, pose, video_thread, lambda_gain):
        super().__init__()
        self.pose = pose
        self.video_thread = video_thread
        self.lambda_gain = lambda_gain
        self._run_flag = True

    def run(self):
        while self._run_flag:
            if self.video_thread.uv is not None and self.video_thread.p_star is not None and self.video_thread.Z is not None:
                uv = self.video_thread.uv
                p_star = self.video_thread.p_star
                Z = self.video_thread.Z
                cam_delta, world_delta = servo(self.pose, uv, Z, p_star, self.lambda_gain, self.video_thread.camera.K)
                self.update_pose_signal.emit(cam_delta.tolist(), world_delta.tolist())
            time.sleep(0.1)  # 避免CPU占用过高

    def stop(self):
        self._run_flag = False
        self.wait()


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.camera = Camera()
        self._run_flag = True
        self.yolo = YOLO("yolo11s.pt").to("cuda")
        self.uv = None
        self.p_star = None
        self.Z = None

    def run(self):
        while self._run_flag:
            if self.camera.is_opened():
                color_intrin, depth_intrin, img_color, img_depth, aligned_depth_frame = self.camera.get_aligned_images()

                img_color = np.array(cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB))

                # 调用 YOLO 模型进行检测
                results = self.yolo(img_color,verbose=False)
                # 获取检测结果
                # 每个检测框数据格式为 [x1, y1, x2, y2, confidence, class_id]
                boxes = results[0].boxes.data.cpu().numpy()
                
                # 遍历每个检测框
                for box in boxes:
                    x1, y1, x2, y2, conf, cls_id = box
                    if cls_id == 9 and conf > 0.5:
                        # 转换坐标为整数
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                        # 绘制矩形框（颜色为绿色，线宽为2）
                        cv2.rectangle(img_color, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        # 生成标签文本（类别和置信度）
                        label = f"{names[int(cls_id)]} {conf:.2f}"
                        # 绘制标签（在框上方显示）
                        cv2.putText(img_color, label, (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                        detected_points = [(x1,y1),(x2,y1),(x2,y2),(x1,y2)]
                        # 计算所有点的 x 坐标和 y 坐标的平均值
                        average_x = (detected_points[0][0] + detected_points[1][0] + detected_points[2][0] + detected_points[3][0]) / 4
                        average_y = (detected_points[0][1] + detected_points[1][1] + detected_points[2][1] + detected_points[3][1]) / 4

                        # 得到中心点坐标
                        center_point = (average_x, average_y)

                        target_points = self.resize_and_center_box(detected_points,padding=0)

                        for point in target_points:
                            cv2.circle(img_color, point, 3, (255, 255, 255), -1)

                        uv = np.array(detected_points).T
                        p_star = np.array(target_points).T

                        self.uv = uv
                        self.p_star = p_star
                        self.Z = img_depth[int(center_point[1]), int(center_point[0])]/1000.0

                # get image info
                h, w, ch = img_color.shape
                # create QImage from image
                bytes_per_line = ch * w
                convert_to_qt_format = QImage(img_color.data, w, h, bytes_per_line, QImage.Format_RGB888)
                # emit signal
                self.change_pixmap_signal.emit(convert_to_qt_format)
            else:
                time.sleep(1)

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()

    def start_camera(self):
        """Start the camera if it's not already running."""
        self._run_flag = True
        self.start()

    def stop_camera(self):
        """Stop the camera without stopping the thread."""
        self.camera.stop()
        self._run_flag = False

    def resize_and_center_box(self, target_points, padding=0):
        # 计算目标框的中心点
        center_x = np.mean([point[0] for point in target_points])
        center_y = np.mean([point[1] for point in target_points])

        # 图像中心点
        image_center_x = self.camera.resolution[0] / 2
        image_center_y = self.camera.resolution[1] / 2

        # 计算目标框与图像中心的偏移量
        offset_x = image_center_x - center_x
        offset_y = image_center_y - center_y

        # 将目标框移动到图像中心
        moved_points = [[point[0] + offset_x, point[1] + offset_y] for point in target_points]

        # 计算移动后的目标框的宽度和高度
        x_coords, y_coords = zip(*moved_points)
        width = max(x_coords) - min(x_coords)
        height = max(y_coords) - min(y_coords)

        # 计算放大比例
        max_dim = max(width, height)
        scale_factor = (max_dim + 2 * padding) / max_dim

        # 等比例放大目标框
        scaled_points = [[int((point[0] - image_center_x) * scale_factor + image_center_x),
                        int((point[1] - image_center_y) * scale_factor + image_center_y)] for point in moved_points]

        return scaled_points

class VisualServoGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("基于图像的视觉伺服界面")
        self.resize(1000, 700)
        self._set_style()
        self.open_camera_flag = False
        self.enable_motor_flag = False
        self.start_visual_servo_flag = False
        self.cam_delta = [0, 0, 0, 0, 0, 0]
        self.world_delta = [0, 0, 0, 0, 0, 0]

        self.pose = [1.1,2.2,3.3,0.7,-0.4,2]

        self.yolo = YOLO("yolo11s.pt").to("cuda")
        self.lambda_gain = 0.6
        self._init_ui()

    def _init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        info_group = QGroupBox("视觉伺服信息", self)
        info_layout = QGridLayout()
        info_layout.setSpacing(10)
        info_group.setLayout(info_layout)

        self.pose_label = QLabel("机械臂末端位姿")
        self.pose_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.pose_display = QLineEdit()
        self.pose_display.setReadOnly(True)
        self.pose_display.setPlaceholderText(f"x:{self.pose[0]} y:{self.pose[1]} z:{self.pose[2]} rx:{self.pose[3]} ry:{self.pose[4]} rz:{self.pose[5]}")

        self.cam_delta_label = QLabel("相机坐标系下的增量:")
        self.cam_delta_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.cam_delta_display = QLineEdit()
        self.cam_delta_display.setReadOnly(True)
        self.cam_delta_display.setPlaceholderText(f"x:{self.cam_delta[0]} y:{self.cam_delta[1]} z:{self.cam_delta[2]} rx:{self.cam_delta[3]} ry:{self.cam_delta[4]} rz:{self.cam_delta[5]}")

        self.world_delta_label = QLabel("世界坐标系下的增量:")
        self.world_delta_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.world_delta_display = QLineEdit()
        self.world_delta_display.setReadOnly(True)
        self.world_delta_display.setPlaceholderText(f"x:{self.world_delta[0]} y:{self.world_delta[1]} z:{self.world_delta[2]} rx:{self.world_delta[3]} ry:{self.world_delta[4]} rz:{self.world_delta[5]}")

        info_layout.addWidget(self.pose_label, 0, 0)
        info_layout.addWidget(self.pose_display, 0, 1)
        info_layout.addWidget(self.cam_delta_label, 1, 0)
        info_layout.addWidget(self.cam_delta_display, 1, 1)
        info_layout.addWidget(self.world_delta_label, 2, 0)
        info_layout.addWidget(self.world_delta_display, 2, 1)

        main_layout.addWidget(info_group)

        btn_group = QGroupBox("操作")
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        btn_group.setLayout(btn_layout)

        self.btn_open_camera = QPushButton("开启相机并检测")
        self.btn_open_camera.clicked.connect(self.open_camera)
        btn_layout.addWidget(self.btn_open_camera)

        self.btn_start_vs = QPushButton("开始视觉伺服")
        self.btn_start_vs.clicked.connect(self.start_visual_servo)
        btn_layout.addWidget(self.btn_start_vs)

        self.btn_enable_motor = QPushButton("开启电机")
        self.btn_enable_motor.clicked.connect(self.enable_motor)
        btn_layout.addWidget(self.btn_enable_motor)

        # 添加急停按钮
        self.btn_emergency_stop = QPushButton("急停")
        self.btn_emergency_stop.setStyleSheet("background-color: red; color: white; font-weight: bold;")
        self.btn_emergency_stop.clicked.connect(self.emergency_stop)
        btn_layout.addWidget(self.btn_emergency_stop)

        main_layout.addWidget(btn_group)

        image_group = QGroupBox("相机图像")
        image_layout = QVBoxLayout()
        image_group.setLayout(image_layout)

        self.image_label = QLabel("图像区域")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid gray; background-color: #F8F8F8;")
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        image_layout.addWidget(self.image_label)
        main_layout.addWidget(image_group, stretch=1)

    def update_image(self, image):
        # Update the image_label with a new image
        self.image_label.setPixmap(QPixmap.fromImage(image))

    def closeEvent(self, event):
        if self.open_camera_flag:
            self.thread.stop_camera()
            self.thread.stop()
        event.accept()

    def emergency_stop(self):
        print("急停按钮被按下！")
        self.pose_display.setText("急停触发，系统停止！")
        self.cam_delta_display.setText("急停")
        self.world_delta_display.setText("急停")

    def open_camera(self):
        if self.open_camera_flag:
            self.thread.stop_camera()
            self.open_camera_flag = False
            self.btn_open_camera.setText("开启相机并检测")
        else:
            self.thread = VideoThread()
            # Connect the signal from the thread to the update_image slot
            self.thread.change_pixmap_signal.connect(self.update_image)
            self.thread.start_camera()
            self.open_camera_flag = True
            self.btn_open_camera.setText("关闭相机")

    def start_visual_servo(self):
        if self.start_visual_servo_flag:
            self.vs_thread.stop()
            self.start_visual_servo_flag = False
            self.btn_start_vs.setText("开始视觉伺服")
        else:
            self.vs_thread = VisualServoThread(self.pose, self.thread, self.lambda_gain)
            self.vs_thread.update_pose_signal.connect(self.update_delta_display)
            self.vs_thread.start()
            self.start_visual_servo_flag = True
            self.btn_start_vs.setText("停止视觉伺服")

    def enable_motor(self):
        if self.enable_motor_flag:
            self.enable_motor_flag = False
            self.btn_enable_motor.setText("开启电机")
        else:
            self.enable_motor_flag = True
            self.btn_enable_motor.setText("关闭电机")

    def update_pose_display(self):
        # 更新位姿显示的函数
        self.pose_display.setText(f"x:{self.pose[0]} y:{self.pose[1]} z:{self.pose[2]} rx:{self.pose[3]} ry:{self.pose[4]} rz:{self.pose[5]}")

    def update_delta_display(self,cam_delta,world_delta):
        self.cam_delta = [round(item,3) for item in cam_delta]
        self.world_delta = [round(item,3) for item in world_delta]
        # 更新增量显示的函数
        self.cam_delta_display.setText(f"x:{self.cam_delta[0]} y:{self.cam_delta[1]} z:{self.cam_delta[2]} rx:{self.cam_delta[3]} ry:{self.cam_delta[4]} rz:{self.cam_delta[5]}")
        self.world_delta_display.setText(f"x:{self.world_delta[0]} y:{self.world_delta[1]} z:{self.world_delta[2]} rx:{self.world_delta[3]} ry:{self.world_delta[4]} rz:{self.world_delta[5]}")

    def _set_style(self):
        """
        设置全局样式，如字体、GroupBox样式等。
        你可以根据需要调整颜色、字体大小等。
        """
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FFFFFF;
            }
            QGroupBox {
                font: 14px 'Microsoft YaHei';
                font-weight: bold;
                color: #333;
                border: 2px solid #B0C4DE;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QLabel {
                font: 13px 'Microsoft YaHei';
            }
            QPushButton {
                font: 13px 'Microsoft YaHei';
                background-color: #E6E6FA;
                border: 1px solid #B0C4DE;
                border-radius: 3px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #D8BFD8;
            }
            QLineEdit {
                font: 13px 'Microsoft YaHei';
                border: 1px solid #B0C4DE;
                border-radius: 3px;
                padding: 3px;
                background-color: #F8F8F8;
            }
        """)
