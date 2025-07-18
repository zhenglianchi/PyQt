from PyQt5.QtCore import Qt, QThread, pyqtSignal
from camera import Camera
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
import time
import cv2
from ultralytics import YOLO

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.camera = Camera()
        self._run_flag = True
        #self.yolo = YOLO("yolo11s.pt")
        self.yolo = YOLO("best.pt")
        self.uv = None
        self.p_star = None
        self.Z = None
        self.center_z = None

    def run(self):
        while self._run_flag:
            if self.camera.is_opened():
                color_intrin, depth_intrin, img_color, img_depth, aligned_depth_frame = self.camera.get_aligned_images()

                img_color = np.array(cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB))
                forward_img = np.array(cv2.cvtColor(img_color, cv2.COLOR_RGB2BGR))

                # 调用 YOLO 模型进行检测
                results = self.yolo(forward_img,verbose=False)
                # 获取检测结果
                # 每个检测框数据格式为 [x1, y1, x2, y2, confidence, class_id]
                boxes = results[0].boxes.data.cpu().numpy()

                # 遍历每个检测框
                for box in boxes:
                    x1, y1, x2, y2, conf, cls_id = box
                    if cls_id == 0 and conf > 0.5:
                        # 转换坐标为整数
                        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                        x1, x2 = np.clip([x1, x2], 0, img_depth.shape[1])
                        y1, y2 = np.clip([y1, y2], 0, img_depth.shape[0])

                        # 提取检测框内的深度区域
                        depth_roi = img_depth[y1:y2, x1:x2]

                        # 直接计算平均深度（包括 0），单位转换为米
                        self.center_z = np.mean(depth_roi) / 1000.0
                        
                        # 绘制矩形框（颜色为绿色，线宽为2）
                        cv2.rectangle(img_color, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        # 生成标签文本（类别和置信度）
                        label = f"target: {conf:.2f}"
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

                img_color = cv2.resize(img_color, (467, 336))  # 注意参数是 (width, height)
                # emit signal
                self.change_pixmap_signal.emit(img_color)
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