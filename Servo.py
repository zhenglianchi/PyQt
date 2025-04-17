"""
servoing module 
"""
import time
import numpy as np
from machinevisiontoolbox.base import *
from machinevisiontoolbox import *
from spatialmath.base import *
from spatialmath import *
from PyQt5.QtCore import Qt, QThread, pyqtSignal


def visjac_p(uv, depth,K):
    uv = base.getmatrix(uv, (2, None))
    Z = depth

    Z = base.getvector(Z)
    if len(Z) == 1:
        Z = np.repeat(Z, uv.shape[1])
    elif len(Z) != uv.shape[1]:
        raise ValueError("Z must be a scalar or have same number of columns as uv")

    L = np.empty((0, 6))  # empty matrix

    Kinv = np.linalg.inv(K)

    for z, p in zip(Z, uv.T):  # iterate over each column (point)

        # convert to normalized image-plane coordinates
        xy = Kinv @ base.e2h(p)
        x = xy[0, 0]
        y = xy[1, 0]

        # 2x6 Jacobian for this point
        # fmt: off
        Lp = K[:2,:2] @ np.array(
            [ [-1/z,  0,     x/z, x * y,      -(1 + x**2), y],
                [ 0,   -1/z,   y/z, (1 + y**2), -x*y,       -x] ])
        # fmt: on
        # stack them vertically
        L = np.vstack([L, Lp])

    return L


def get_K(fu=0.008,fv=0.008,rhou=1e-05,rhov=1e-05,u0=250.0,v0=250.0):
    # fmt: off
    K = np.array([[fu / rhou, 0,                   u0],
                    [ 0,                  fv / rhov, v0],
                    [ 0,                  0,                    1]
                    ], dtype=np.float64)
    # fmt: on
    return K



def servo(pose,uv,Z,p_star,lambda_gain,K):
    if Z <= 1e-6:
        Z = 0.5

    J = visjac_p(uv, Z, K)  # compute visual Jacobian

    # 计算误差（目标特征点与当前特征点的差值）
    e = uv - p_star  # feature error
    e = e.flatten(order="F")  # convert columnwise to a 1D vector

    error_rms = np.sqrt(np.mean(e**2))
    #print("误差:",error_rms)

    v = -lambda_gain * np.linalg.pinv(J) @ e

    #print("当前增量在相机坐标系下:\n",v)

    # 重新计算位姿增量 Td
    Td = SE3.Delta(v)

    # 获得机械臂末端位姿
    current_pos = pose

    #print(current_pos)

    current_object_pos = current_pos[:3]
    current_object_rot = current_pos[3:]

    T_translation = SE3(current_object_pos)
    T_rotation_to_world = SE3.Rx(current_object_rot[0]) * SE3.Ry(current_object_rot[1]) * SE3.Rz(current_object_rot[2])

    T_matrix_to_world = T_translation * T_rotation_to_world


    T_world_d = T_matrix_to_world @ Td @ T_matrix_to_world.inv()

    #print("当前位姿齐次表示:\n",T_translation * T_rotation)
    #print("当前位姿增量在相机坐标系下:\n",Td)
    #print("当前位姿增量在世界坐标系下:\n",T_world_d)
    #print("下一步位姿齐次表示:\n",next_T_matrix)

    # 提取平移部分
    translation = T_world_d.t
    rot = v[3:]

    delta_speed = np.hstack((translation, rot)).reshape(1, 6).squeeze()

    return v,delta_speed



class VisualServoThread(QThread):
    update_pose_signal = pyqtSignal(list)

    def __init__(self, ui , lambda_gain):
        super().__init__()
        self.ui = ui
        self.video_thread = self.ui.thread
        self.lambda_gain = lambda_gain
        self._run_flag = None

    def run(self):
        while self._run_flag:
            if self.video_thread.uv is not None and self.video_thread.p_star is not None and self.video_thread.Z is not None:
                uv = self.video_thread.uv
                p_star = self.video_thread.p_star
                Z = self.video_thread.Z
                x,y,z,rx,ry,rz = float(self.ui.lineEdit_24.text()),float(self.ui.lineEdit_25.text()),float(self.ui.lineEdit_26.text()),float(self.ui.lineEdit_27.text()),float(self.ui.lineEdit_28.text()),float(self.ui.lineEdit_29.text())
                curr_pose = [x,y,z,rx,ry,rz]
                cam_delta, world_delta = servo(curr_pose, uv, Z, p_star, self.lambda_gain, self.video_thread.camera.K)
                self.update_pose_signal.emit(world_delta.tolist())
            time.sleep(0.1)  # 避免CPU占用过高

    def stop(self):
        self._run_flag = False
        self.wait()

    def start(self):
        self._run_flag = True