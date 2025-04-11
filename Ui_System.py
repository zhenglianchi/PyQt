from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from camera import Camera
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
import time
import cv2
from ultralytics import YOLO
from ads import TwinCat3_ADSserver
from Servo import servo
import pyads


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1828, 1026)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1600, 900))
        MainWindow.setMaximumSize(QtCore.QSize(3840, 2160))
        font = QtGui.QFont()
        font.setPointSize(14)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("")
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.centralWidget.sizePolicy().hasHeightForWidth())
        self.centralWidget.setSizePolicy(sizePolicy)
        self.centralWidget.setMinimumSize(QtCore.QSize(1600, 900))
        self.centralWidget.setMaximumSize(QtCore.QSize(3840, 2160))
        self.centralWidget.setStyleSheet("background-color: rgb(105, 105, 105);")
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setContentsMargins(8, 0, 8, 30)
        self.verticalLayout_5.setSpacing(8)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(-1, -1, -1, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupConfig = QtWidgets.QWidget(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupConfig.sizePolicy().hasHeightForWidth())
        self.groupConfig.setSizePolicy(sizePolicy)
        self.groupConfig.setMinimumSize(QtCore.QSize(0, 65))
        self.groupConfig.setStyleSheet("background-color:#d3d3d3;\n"
"font: 22pt \"Adobe 黑体 Std R\";")
        self.groupConfig.setObjectName("groupConfig")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupConfig)
        self.horizontalLayout_2.setContentsMargins(80, 0, 80, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_5 = QtWidgets.QLabel(self.groupConfig)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.verticalLayout_4.addWidget(self.groupConfig)
        self.verticalLayout_5.addLayout(self.verticalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.groupTarget = QtWidgets.QGroupBox(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupTarget.sizePolicy().hasHeightForWidth())
        self.groupTarget.setSizePolicy(sizePolicy)
        self.groupTarget.setMinimumSize(QtCore.QSize(850, 0))
        self.groupTarget.setMaximumSize(QtCore.QSize(900, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.groupTarget.setFont(font)
        self.groupTarget.setStyleSheet("")
        self.groupTarget.setTitle("")
        self.groupTarget.setObjectName("groupTarget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupTarget)
        self.verticalLayout_2.setContentsMargins(-1, 3, -1, 3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.SingleMachine = QtWidgets.QGroupBox(self.groupTarget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SingleMachine.sizePolicy().hasHeightForWidth())
        self.SingleMachine.setSizePolicy(sizePolicy)
        self.SingleMachine.setMinimumSize(QtCore.QSize(0, 120))
        self.SingleMachine.setStyleSheet("font: 15pt \"Adobe 黑体 Std R\";\n"
"border-color: rgb(249, 249, 249);\n"
"border: 3px solid #f9f9f9;      /* 边框粗细+颜色 */\n"
"border-radius: 8px;         /* 圆角半径 */\n"
"margin-top: 1ex;\n"
"color:white\n"
"")
        self.SingleMachine.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.SingleMachine.setFlat(False)
        self.SingleMachine.setCheckable(False)
        self.SingleMachine.setObjectName("SingleMachine")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.SingleMachine)
        self.verticalLayout_9.setContentsMargins(-1, 5, -1, 0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.widget = QtWidgets.QWidget(self.SingleMachine)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(0, 80))
        self.widget.setStyleSheet("border-color: rgb(173, 178, 181);\n"
"background-color:#d3d3d3;\n"
"border-radius: 0px; \n"
"color:black;\n"
"font: 14pt \"Adobe 黑体 Std R\";\n"
"\n"
"")
        self.widget.setObjectName("widget")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_10.setContentsMargins(-1, 11, -1, 0)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.widget_2 = QtWidgets.QWidget(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setMinimumSize(QtCore.QSize(0, 60))
        self.widget_2.setStyleSheet("border:none;\n"
"\n"
"")
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_13 = QtWidgets.QLabel(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setMinimumSize(QtCore.QSize(40, 40))
        self.label_13.setStyleSheet("background-color: rgb(88, 214, 92);\n"
"border-radius: 20px; \n"
"border: 1px solid gray;\n"
"margin-top: 0px;\n"
"")
        self.label_13.setText("")
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_3.addWidget(self.label_13)
        self.pushButton_6 = QtWidgets.QPushButton(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_6.sizePolicy().hasHeightForWidth())
        self.pushButton_6.setSizePolicy(sizePolicy)
        self.pushButton_6.setMinimumSize(QtCore.QSize(70, 0))
        self.pushButton_6.setStyleSheet("background-color: #f4f4f4;\n"
"color: black;\n"
"   \n"
"padding: 5px 10px;\n"
"\n"
"border-left:0px;\n"
"border-top:0px;\n"
" border-right: 2px solid #a3a3a3;  /* 右边边框 */\n"
"    border-bottom: 2px solid #a3a3a3; /* 下边边框 */\n"
"margin-top: 0px;")
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.clicked.connect(self.open_connect)
        self.horizontalLayout_3.addWidget(self.pushButton_6)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.pushButton_8 = QtWidgets.QPushButton(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_8.sizePolicy().hasHeightForWidth())
        self.pushButton_8.setSizePolicy(sizePolicy)
        self.pushButton_8.setMinimumSize(QtCore.QSize(120, 0))
        self.pushButton_8.setStyleSheet("background-color: #f4f4f4;\n"
"color: black;\n"
"   \n"
"padding: 5px 10px;\n"
"\n"
"border-left:0px;\n"
"border-top:0px;\n"
" border-right: 2px solid #a3a3a3;  /* 右边边框 */\n"
"    border-bottom: 2px solid #a3a3a3; /* 下边边框 */\n"
"margin-top: 0px;")
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_8.clicked.connect(self.open_camera)
        self.horizontalLayout_3.addWidget(self.pushButton_8)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget_2)
        self.pushButton_2.setStyleSheet("background-color: #f4f4f4;\n"
"color: black;\n"
"   \n"
"padding: 5px 10px;\n"
"\n"
"border-left:0px;\n"
"border-top:0px;\n"
" border-right: 2px solid #a3a3a3;  /* 右边边框 */\n"
"    border-bottom: 2px solid #a3a3a3; /* 下边边框 */\n"
"margin-top: 0px;")
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_3.addWidget(self.pushButton_2)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.pushButton_7 = QtWidgets.QPushButton(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_7.sizePolicy().hasHeightForWidth())
        self.pushButton_7.setSizePolicy(sizePolicy)
        self.pushButton_7.setMinimumSize(QtCore.QSize(145, 0))
        self.pushButton_7.setStyleSheet("background-color: #f4f4f4;\n"
"color: black;\n"
"   \n"
"padding: 5px 10px;\n"
"\n"
"border-left:0px;\n"
"border-top:0px;\n"
" border-right: 2px solid #a3a3a3;  /* 右边边框 */\n"
"    border-bottom: 2px solid #a3a3a3; /* 下边边框 */\n"
"margin-top: 0px;")
        self.pushButton_7.setObjectName("pushButton_7")
        self.horizontalLayout_3.addWidget(self.pushButton_7)
        self.label_36 = QtWidgets.QLabel(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_36.sizePolicy().hasHeightForWidth())
        self.label_36.setSizePolicy(sizePolicy)
        self.label_36.setStyleSheet("margin-top: 0px;")
        self.label_36.setObjectName("label_36")
        self.horizontalLayout_3.addWidget(self.label_36)
        self.lineEdit_7 = QtWidgets.QLineEdit(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_7.sizePolicy().hasHeightForWidth())
        self.lineEdit_7.setSizePolicy(sizePolicy)
        self.lineEdit_7.setMinimumSize(QtCore.QSize(100, 0))
        self.lineEdit_7.setStyleSheet("background-color: #f9f9f9;\n"
"padding: 5px 10px;\n"
"border:none;\n"
"margin-top: 0px;")
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.horizontalLayout_3.addWidget(self.lineEdit_7)
        self.verticalLayout_10.addWidget(self.widget_2)
        self.verticalLayout_9.addWidget(self.widget)
        self.verticalLayout_2.addWidget(self.SingleMachine)
        self.SingleMachine_2 = QtWidgets.QGroupBox(self.groupTarget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SingleMachine_2.sizePolicy().hasHeightForWidth())
        self.SingleMachine_2.setSizePolicy(sizePolicy)
        self.SingleMachine_2.setMinimumSize(QtCore.QSize(0, 185))
        self.SingleMachine_2.setStyleSheet("font: 15pt \"Adobe 黑体 Std R\";\n"
"border-color: rgb(249, 249, 249);\n"
"border: 3px solid #f9f9f9;      /* 边框粗细+颜色 */\n"
"border-radius: 8px;         /* 圆角半径 */\n"
"margin-top: 1ex;\n"
"color:white\n"
"")
        self.SingleMachine_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.SingleMachine_2.setFlat(False)
        self.SingleMachine_2.setCheckable(False)
        self.SingleMachine_2.setObjectName("SingleMachine_2")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.SingleMachine_2)
        self.verticalLayout_13.setContentsMargins(-1, 5, -1, 5)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.widget_3 = QtWidgets.QWidget(self.SingleMachine_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.widget_3.setMinimumSize(QtCore.QSize(0, 145))
        self.widget_3.setStyleSheet("border-color: rgb(173, 178, 181);\n"
"background-color:#d3d3d3;\n"
"border-radius: 0px; \n"
"color:black;\n"
"font: 14pt \"Adobe 黑体 Std R\";\n"
"\n"
"")
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout_14.setContentsMargins(-1, 11, -1, 0)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.widget_15 = QtWidgets.QWidget(self.widget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_15.sizePolicy().hasHeightForWidth())
        self.widget_15.setSizePolicy(sizePolicy)
        self.widget_15.setMinimumSize(QtCore.QSize(0, 45))
        self.widget_15.setStyleSheet("border:none;margin-top: 0px;\n"
"\n"
"")
        self.widget_15.setObjectName("widget_15")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout(self.widget_15)
        self.horizontalLayout_15.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.label_34 = QtWidgets.QLabel(self.widget_15)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_34.sizePolicy().hasHeightForWidth())
        self.label_34.setSizePolicy(sizePolicy)
        self.label_34.setMinimumSize(QtCore.QSize(40, 40))
        self.label_34.setStyleSheet("background-color: rgb(88, 214, 92);\n"
"border-radius: 20px; \n"
"border: 1px solid gray;\n"
"margin-top: 0px;\n"
"")
        self.label_34.setText("")
        self.label_34.setObjectName("label_34")
        self.horizontalLayout_15.addWidget(self.label_34)
        self.comboBox = QtWidgets.QComboBox(self.widget_15)
        self.comboBox.setStyleSheet("background-color: #f9f9f9;\n"
"padding: 5px 10px;\n"
"border:none;\n"
"margin-top: 0px;")
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout_15.addWidget(self.comboBox)
        spacerItem3 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_15.addItem(spacerItem3)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_15.addItem(spacerItem4)
        self.pushButton_9 = QtWidgets.QPushButton(self.widget_15)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_9.sizePolicy().hasHeightForWidth())
        self.pushButton_9.setSizePolicy(sizePolicy)
        self.pushButton_9.setMinimumSize(QtCore.QSize(70, 0))
        self.pushButton_9.setStyleSheet("background-color: #f4f4f4;\n"
"color: black;\n"
"   \n"
"padding: 5px 10px;\n"
"\n"
"border-left:0px;\n"
"border-top:0px;\n"
" border-right: 2px solid #a3a3a3;  /* 右边边框 */\n"
"    border-bottom: 2px solid #a3a3a3; /* 下边边框 */\n"
"margin-top: 0px;")
        self.pushButton_9.setObjectName("pushButton_9")
        self.horizontalLayout_15.addWidget(self.pushButton_9)
        spacerItem5 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_15.addItem(spacerItem5)
        self.pushButton_10 = QtWidgets.QPushButton(self.widget_15)
        self.pushButton_10.setMinimumSize(QtCore.QSize(70, 0))
        self.pushButton_10.setStyleSheet("background-color: #f4f4f4;\n"
"color: black;\n"
"   \n"
"padding: 5px 10px;\n"
"\n"
"border-left:0px;\n"
"border-top:0px;\n"
" border-right: 2px solid #a3a3a3;  /* 右边边框 */\n"
"    border-bottom: 2px solid #a3a3a3; /* 下边边框 */\n"
"margin-top: 0px;")
        self.pushButton_10.setObjectName("pushButton_10")
        self.horizontalLayout_15.addWidget(self.pushButton_10)
        spacerItem6 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_15.addItem(spacerItem6)
        self.pushButton_11 = QtWidgets.QPushButton(self.widget_15)
        self.pushButton_11.setMinimumSize(QtCore.QSize(70, 0))
        self.pushButton_11.setStyleSheet("background-color: #f4f4f4;\n"
"color: black;\n"
"   \n"
"padding: 5px 10px;\n"
"\n"
"border-left:0px;\n"
"border-top:0px;\n"
" border-right: 2px solid #a3a3a3;  /* 右边边框 */\n"
"    border-bottom: 2px solid #a3a3a3; /* 下边边框 */\n"
"margin-top: 0px;")
        self.pushButton_11.setObjectName("pushButton_11")
        self.horizontalLayout_15.addWidget(self.pushButton_11)
        spacerItem7 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_15.addItem(spacerItem7)
        self.label_43 = QtWidgets.QLabel(self.widget_15)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_43.sizePolicy().hasHeightForWidth())
        self.label_43.setSizePolicy(sizePolicy)
        self.label_43.setMinimumSize(QtCore.QSize(60, 0))
        self.label_43.setStyleSheet("margin-top: 0px;")
        self.label_43.setObjectName("label_43")
        self.horizontalLayout_15.addWidget(self.label_43)
        self.lineEdit_14 = QtWidgets.QLineEdit(self.widget_15)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_14.sizePolicy().hasHeightForWidth())
        self.lineEdit_14.setSizePolicy(sizePolicy)
        self.lineEdit_14.setMinimumSize(QtCore.QSize(230, 0))
        self.lineEdit_14.setStyleSheet("background-color: #f9f9f9;\n"
"padding: 5px 10px;\n"
"border:none;\n"
"margin-top: 0px;")
        self.lineEdit_14.setObjectName("lineEdit_14")
        self.horizontalLayout_15.addWidget(self.lineEdit_14)
        self.verticalLayout_14.addWidget(self.widget_15)
        self.widget_16 = QtWidgets.QWidget(self.widget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_16.sizePolicy().hasHeightForWidth())
        self.widget_16.setSizePolicy(sizePolicy)
        self.widget_16.setMinimumSize(QtCore.QSize(0, 45))
        self.widget_16.setStyleSheet("border:none;")
        self.widget_16.setObjectName("widget_16")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout(self.widget_16)
        self.horizontalLayout_16.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        spacerItem8 = QtWidgets.QSpacerItem(80, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_16.addItem(spacerItem8)
        self.pushButton_12 = QtWidgets.QPushButton(self.widget_16)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_12.sizePolicy().hasHeightForWidth())
        self.pushButton_12.setSizePolicy(sizePolicy)
        self.pushButton_12.setMinimumSize(QtCore.QSize(70, 0))
        self.pushButton_12.setStyleSheet("background-color: #f4f4f4;\n"
"color: black;\n"
"   \n"
"padding: 5px 10px;\n"
"\n"
"border-left:0px;\n"
"border-top:0px;\n"
" border-right: 2px solid #a3a3a3;  /* 右边边框 */\n"
"    border-bottom: 2px solid #a3a3a3; /* 下边边框 */\n"
"margin-top: 0px;")
        self.pushButton_12.setObjectName("pushButton_12")
        self.horizontalLayout_16.addWidget(self.pushButton_12)
        spacerItem9 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_16.addItem(spacerItem9)
        self.pushButton_13 = QtWidgets.QPushButton(self.widget_16)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_13.sizePolicy().hasHeightForWidth())
        self.pushButton_13.setSizePolicy(sizePolicy)
        self.pushButton_13.setMinimumSize(QtCore.QSize(70, 0))
        self.pushButton_13.setStyleSheet("background-color: #f4f4f4;\n"
"color: black;\n"
"   \n"
"padding: 5px 10px;\n"
"\n"
"border-left:0px;\n"
"border-top:0px;\n"
" border-right: 2px solid #a3a3a3;  /* 右边边框 */\n"
"    border-bottom: 2px solid #a3a3a3; /* 下边边框 */\n"
"margin-top: 0px;")
        self.pushButton_13.setObjectName("pushButton_13")
        self.horizontalLayout_16.addWidget(self.pushButton_13)
        spacerItem10 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_16.addItem(spacerItem10)
        self.pushButton_14 = QtWidgets.QPushButton(self.widget_16)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_14.sizePolicy().hasHeightForWidth())
        self.pushButton_14.setSizePolicy(sizePolicy)
        self.pushButton_14.setMinimumSize(QtCore.QSize(70, 0))
        self.pushButton_14.setStyleSheet("background-color: #f4f4f4;\n"
"color: black;\n"
"   \n"
"padding: 5px 10px;\n"
"\n"
"border-left:0px;\n"
"border-top:0px;\n"
" border-right: 2px solid #a3a3a3;  /* 右边边框 */\n"
"    border-bottom: 2px solid #a3a3a3; /* 下边边框 */\n"
"margin-top: 0px;")
        self.pushButton_14.setObjectName("pushButton_14")
        self.horizontalLayout_16.addWidget(self.pushButton_14)
        spacerItem11 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_16.addItem(spacerItem11)
        self.pushButton_15 = QtWidgets.QPushButton(self.widget_16)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_15.sizePolicy().hasHeightForWidth())
        self.pushButton_15.setSizePolicy(sizePolicy)
        self.pushButton_15.setMinimumSize(QtCore.QSize(70, 0))
        self.pushButton_15.setStyleSheet("background-color: #f4f4f4;\n"
"color: black;\n"
"   \n"
"padding: 5px 10px;\n"
"\n"
"border-left:0px;\n"
"border-top:0px;\n"
" border-right: 2px solid #a3a3a3;  /* 右边边框 */\n"
"    border-bottom: 2px solid #a3a3a3; /* 下边边框 */\n"
"margin-top: 0px;")
        self.pushButton_15.setObjectName("pushButton_15")
        self.horizontalLayout_16.addWidget(self.pushButton_15)
        spacerItem12 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_16.addItem(spacerItem12)
        self.label_44 = QtWidgets.QLabel(self.widget_16)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_44.sizePolicy().hasHeightForWidth())
        self.label_44.setSizePolicy(sizePolicy)
        self.label_44.setMinimumSize(QtCore.QSize(60, 0))
        self.label_44.setStyleSheet("border:none;\n"
"margin-top: 0px;\n"
"")
        self.label_44.setObjectName("label_44")
        self.horizontalLayout_16.addWidget(self.label_44)
        self.lineEdit_15 = QtWidgets.QLineEdit(self.widget_16)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_15.sizePolicy().hasHeightForWidth())
        self.lineEdit_15.setSizePolicy(sizePolicy)
        self.lineEdit_15.setMinimumSize(QtCore.QSize(230, 0))
        self.lineEdit_15.setStyleSheet("background-color: #f9f9f9;\n"
"padding: 5px 10px;\n"
"border:none;\n"
"margin-top: 0px;")
        self.lineEdit_15.setObjectName("lineEdit_15")
        self.horizontalLayout_16.addWidget(self.lineEdit_15)
        self.verticalLayout_14.addWidget(self.widget_16)
        self.verticalLayout_13.addWidget(self.widget_3)
        self.verticalLayout_2.addWidget(self.SingleMachine_2)
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupTarget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy)
        self.groupBox_5.setMinimumSize(QtCore.QSize(0, 440))
        self.groupBox_5.setStyleSheet("font: 15pt \"Adobe 黑体 Std R\";\n"
"border-color: rgb(249, 249, 249);\n"
"border: 3px solid #f9f9f9;      /* 边框粗细+颜色 */\n"
"border-radius: 8px;         /* 圆角半径 */\n"
"margin-top: 1ex;\n"
"\n"
"color:white\n"
"")
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_16.setContentsMargins(-1, 11, -1, 3)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.widget_14 = QtWidgets.QWidget(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_14.sizePolicy().hasHeightForWidth())
        self.widget_14.setSizePolicy(sizePolicy)
        self.widget_14.setMinimumSize(QtCore.QSize(0, 260))
        self.widget_14.setStyleSheet("border-color: rgb(173, 178, 181);\n"
"background-color:#d3d3d3;\n"
"border-radius: 0px; \n"
"color:black;\n"
"font: 12pt \"Adobe 黑体 Std R\";\n"
"\n"
"")
        self.widget_14.setObjectName("widget_14")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.widget_14)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.widget_22 = QtWidgets.QWidget(self.widget_14)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_22.sizePolicy().hasHeightForWidth())
        self.widget_22.setSizePolicy(sizePolicy)
        self.widget_22.setMinimumSize(QtCore.QSize(0, 45))
        self.widget_22.setStyleSheet("border:none\n"
"")
        self.widget_22.setObjectName("widget_22")
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout(self.widget_22)
        self.horizontalLayout_20.setContentsMargins(-1, 5, -1, 0)
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.pushButton = QtWidgets.QPushButton(self.widget_22)
        self.pushButton.setMinimumSize(QtCore.QSize(250, 0))
        self.pushButton.setStyleSheet("background-color: #f4f4f4;\n"
"color: black;\n"
"   \n"
"padding: 5px 10px;\n"
"\n"
"border-left:0px;\n"
"border-top:0px;\n"
" border-right: 2px solid #a3a3a3;  /* 右边边框 */\n"
"    border-bottom: 2px solid #a3a3a3; /* 下边边框 */\n"
"margin-top: 0px;")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_20.addWidget(self.pushButton)
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_20.addItem(spacerItem13)
        self.label_46 = QtWidgets.QLabel(self.widget_22)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_46.sizePolicy().hasHeightForWidth())
        self.label_46.setSizePolicy(sizePolicy)
        self.label_46.setMinimumSize(QtCore.QSize(30, 30))
        self.label_46.setStyleSheet("background-color: rgb(88, 214, 92);\n"
"border-radius: 15px; \n"
"border: 1px solid gray;\n"
"margin-top: 0px;\n"
"")
        self.label_46.setText("")
        self.label_46.setObjectName("label_46")
        self.horizontalLayout_20.addWidget(self.label_46)
        spacerItem14 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_20.addItem(spacerItem14)
        self.lineEdit_31 = QtWidgets.QLineEdit(self.widget_22)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_31.sizePolicy().hasHeightForWidth())
        self.lineEdit_31.setSizePolicy(sizePolicy)
        self.lineEdit_31.setMinimumSize(QtCore.QSize(340, 35))
        self.lineEdit_31.setStyleSheet("background-color: #f9f9f9;\n"
"padding: 5px 10px;\n"
"border:none;\n"
"margin-top: 0px;")
        self.lineEdit_31.setObjectName("lineEdit_31")
        self.horizontalLayout_20.addWidget(self.lineEdit_31)
        self.verticalLayout_12.addWidget(self.widget_22)
        self.widget_23 = QtWidgets.QWidget(self.widget_14)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_23.sizePolicy().hasHeightForWidth())
        self.widget_23.setSizePolicy(sizePolicy)
        self.widget_23.setMinimumSize(QtCore.QSize(0, 45))
        self.widget_23.setStyleSheet("border:none\n"
"")
        self.widget_23.setObjectName("widget_23")
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout(self.widget_23)
        self.horizontalLayout_21.setContentsMargins(-1, 5, -1, 0)
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.pushButton_3 = QtWidgets.QPushButton(self.widget_23)
        self.pushButton_3.setMinimumSize(QtCore.QSize(250, 0))
        self.pushButton_3.setStyleSheet("background-color: #f4f4f4;\n"
"color: black;\n"
"   \n"
"padding: 5px 10px;\n"
"\n"
"border-left:0px;\n"
"border-top:0px;\n"
" border-right: 2px solid #a3a3a3;  /* 右边边框 */\n"
"    border-bottom: 2px solid #a3a3a3; /* 下边边框 */\n"
"margin-top: 0px;")
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_21.addWidget(self.pushButton_3)
        spacerItem15 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_21.addItem(spacerItem15)
        self.label_50 = QtWidgets.QLabel(self.widget_23)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_50.sizePolicy().hasHeightForWidth())
        self.label_50.setSizePolicy(sizePolicy)
        self.label_50.setMinimumSize(QtCore.QSize(30, 30))
        self.label_50.setStyleSheet("background-color: rgb(88, 214, 92);\n"
"border-radius: 15px; \n"
"border: 1px solid gray;\n"
"margin-top: 0px;\n"
"")
        self.label_50.setText("")
        self.label_50.setObjectName("label_50")
        self.horizontalLayout_21.addWidget(self.label_50)
        spacerItem16 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_21.addItem(spacerItem16)
        self.lineEdit_32 = QtWidgets.QLineEdit(self.widget_23)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_32.sizePolicy().hasHeightForWidth())
        self.lineEdit_32.setSizePolicy(sizePolicy)
        self.lineEdit_32.setMinimumSize(QtCore.QSize(340, 35))
        self.lineEdit_32.setStyleSheet("background-color: #f9f9f9;\n"
"padding: 5px 10px;\n"
"border:none;\n"
"margin-top: 0px;")
        self.lineEdit_32.setObjectName("lineEdit_32")
        self.horizontalLayout_21.addWidget(self.lineEdit_32)
        self.verticalLayout_12.addWidget(self.widget_23)
        self.widget_24 = QtWidgets.QWidget(self.widget_14)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_24.sizePolicy().hasHeightForWidth())
        self.widget_24.setSizePolicy(sizePolicy)
        self.widget_24.setMinimumSize(QtCore.QSize(0, 45))
        self.widget_24.setStyleSheet("border:none\n"
"")
        self.widget_24.setObjectName("widget_24")
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout(self.widget_24)
        self.horizontalLayout_22.setContentsMargins(-1, 5, -1, 0)
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        self.pushButton_4 = QtWidgets.QPushButton(self.widget_24)
        self.pushButton_4.setMinimumSize(QtCore.QSize(250, 0))
        self.pushButton_4.setStyleSheet("background-color: #f4f4f4;\n"
"color: black;\n"
"   \n"
"padding: 5px 10px;\n"
"\n"
"border-left:0px;\n"
"border-top:0px;\n"
" border-right: 2px solid #a3a3a3;  /* 右边边框 */\n"
"    border-bottom: 2px solid #a3a3a3; /* 下边边框 */\n"
"margin-top: 0px;")
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_22.addWidget(self.pushButton_4)
        spacerItem17 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_22.addItem(spacerItem17)
        self.label_52 = QtWidgets.QLabel(self.widget_24)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_52.sizePolicy().hasHeightForWidth())
        self.label_52.setSizePolicy(sizePolicy)
        self.label_52.setMinimumSize(QtCore.QSize(30, 30))
        self.label_52.setStyleSheet("background-color: rgb(88, 214, 92);\n"
"border-radius: 15px; \n"
"border: 1px solid gray;\n"
"margin-top: 0px;\n"
"")
        self.label_52.setText("")
        self.label_52.setObjectName("label_52")
        self.horizontalLayout_22.addWidget(self.label_52)
        spacerItem18 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_22.addItem(spacerItem18)
        self.lineEdit_33 = QtWidgets.QLineEdit(self.widget_24)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_33.sizePolicy().hasHeightForWidth())
        self.lineEdit_33.setSizePolicy(sizePolicy)
        self.lineEdit_33.setMinimumSize(QtCore.QSize(340, 35))
        self.lineEdit_33.setStyleSheet("background-color: #f9f9f9;\n"
"padding: 5px 10px;\n"
"border:none;\n"
"margin-top: 0px;")
        self.lineEdit_33.setObjectName("lineEdit_33")
        self.horizontalLayout_22.addWidget(self.lineEdit_33)
        self.verticalLayout_12.addWidget(self.widget_24)
        self.widget_28 = QtWidgets.QWidget(self.widget_14)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_28.sizePolicy().hasHeightForWidth())
        self.widget_28.setSizePolicy(sizePolicy)
        self.widget_28.setMinimumSize(QtCore.QSize(0, 45))
        self.widget_28.setStyleSheet("border:none\n"
"")
        self.widget_28.setObjectName("widget_28")
        self.horizontalLayout_26 = QtWidgets.QHBoxLayout(self.widget_28)
        self.horizontalLayout_26.setContentsMargins(-1, 5, -1, 0)
        self.horizontalLayout_26.setObjectName("horizontalLayout_26")
        self.pushButton_5 = QtWidgets.QPushButton(self.widget_28)
        self.pushButton_5.setMinimumSize(QtCore.QSize(250, 0))
        self.pushButton_5.setStyleSheet("background-color: #f4f4f4;\n"
"color: black;\n"
"   \n"
"padding: 5px 10px;\n"
"\n"
"border-left:0px;\n"
"border-top:0px;\n"
" border-right: 2px solid #a3a3a3;  /* 右边边框 */\n"
"    border-bottom: 2px solid #a3a3a3; /* 下边边框 */\n"
"margin-top: 0px;")
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_26.addWidget(self.pushButton_5)
        spacerItem19 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_26.addItem(spacerItem19)
        self.label_60 = QtWidgets.QLabel(self.widget_28)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_60.sizePolicy().hasHeightForWidth())
        self.label_60.setSizePolicy(sizePolicy)
        self.label_60.setMinimumSize(QtCore.QSize(30, 30))
        self.label_60.setStyleSheet("background-color: rgb(88, 214, 92);\n"
"border-radius: 15px; \n"
"border: 1px solid gray;\n"
"margin-top: 0px;\n"
"")
        self.label_60.setText("")
        self.label_60.setObjectName("label_60")
        self.horizontalLayout_26.addWidget(self.label_60)
        spacerItem20 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_26.addItem(spacerItem20)
        self.lineEdit_37 = QtWidgets.QLineEdit(self.widget_28)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_37.sizePolicy().hasHeightForWidth())
        self.lineEdit_37.setSizePolicy(sizePolicy)
        self.lineEdit_37.setMinimumSize(QtCore.QSize(340, 35))
        self.lineEdit_37.setStyleSheet("background-color: #f9f9f9;\n"
"padding: 5px 10px;\n"
"border:none;\n"
"margin-top: 0px;")
        self.lineEdit_37.setObjectName("lineEdit_37")
        self.horizontalLayout_26.addWidget(self.lineEdit_37)
        self.verticalLayout_12.addWidget(self.widget_28)
        self.widget_27 = QtWidgets.QWidget(self.widget_14)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_27.sizePolicy().hasHeightForWidth())
        self.widget_27.setSizePolicy(sizePolicy)
        self.widget_27.setMinimumSize(QtCore.QSize(0, 45))
        self.widget_27.setStyleSheet("border:none\n"
"")
        self.widget_27.setObjectName("widget_27")
        self.horizontalLayout_25 = QtWidgets.QHBoxLayout(self.widget_27)
        self.horizontalLayout_25.setContentsMargins(-1, 5, -1, 0)
        self.horizontalLayout_25.setObjectName("horizontalLayout_25")
        self.pushButton_16 = QtWidgets.QPushButton(self.widget_27)
        self.pushButton_16.setMinimumSize(QtCore.QSize(250, 0))
        self.pushButton_16.setStyleSheet("background-color: #f4f4f4;\n"
"color: black;\n"
"   \n"
"padding: 5px 10px;\n"
"\n"
"border-left:0px;\n"
"border-top:0px;\n"
" border-right: 2px solid #a3a3a3;  /* 右边边框 */\n"
"    border-bottom: 2px solid #a3a3a3; /* 下边边框 */\n"
"margin-top: 0px;")
        self.pushButton_16.setObjectName("pushButton_16")
        self.horizontalLayout_25.addWidget(self.pushButton_16)
        spacerItem21 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_25.addItem(spacerItem21)
        self.label_58 = QtWidgets.QLabel(self.widget_27)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_58.sizePolicy().hasHeightForWidth())
        self.label_58.setSizePolicy(sizePolicy)
        self.label_58.setMinimumSize(QtCore.QSize(30, 30))
        self.label_58.setStyleSheet("background-color: rgb(88, 214, 92);\n"
"border-radius: 15px; \n"
"border: 1px solid gray;\n"
"margin-top: 0px;\n"
"")
        self.label_58.setText("")
        self.label_58.setObjectName("label_58")
        self.horizontalLayout_25.addWidget(self.label_58)
        spacerItem22 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_25.addItem(spacerItem22)
        self.lineEdit_36 = QtWidgets.QLineEdit(self.widget_27)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_36.sizePolicy().hasHeightForWidth())
        self.lineEdit_36.setSizePolicy(sizePolicy)
        self.lineEdit_36.setMinimumSize(QtCore.QSize(340, 35))
        self.lineEdit_36.setStyleSheet("background-color: #f9f9f9;\n"
"padding: 5px 10px;\n"
"border:none;\n"
"margin-top: 0px;")
        self.lineEdit_36.setObjectName("lineEdit_36")
        self.horizontalLayout_25.addWidget(self.lineEdit_36)
        self.verticalLayout_12.addWidget(self.widget_27)
        self.widget_26 = QtWidgets.QWidget(self.widget_14)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_26.sizePolicy().hasHeightForWidth())
        self.widget_26.setSizePolicy(sizePolicy)
        self.widget_26.setMinimumSize(QtCore.QSize(0, 45))
        self.widget_26.setStyleSheet("border:none\n"
"")
        self.widget_26.setObjectName("widget_26")
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout(self.widget_26)
        self.horizontalLayout_24.setContentsMargins(-1, 5, -1, 0)
        self.horizontalLayout_24.setObjectName("horizontalLayout_24")
        self.pushButton_17 = QtWidgets.QPushButton(self.widget_26)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_17.sizePolicy().hasHeightForWidth())
        self.pushButton_17.setSizePolicy(sizePolicy)
        self.pushButton_17.setMinimumSize(QtCore.QSize(250, 0))
        self.pushButton_17.setStyleSheet("background-color: #f4f4f4;\n"
"color: black;\n"
"   \n"
"padding: 5px 10px;\n"
"\n"
"border-left:0px;\n"
"border-top:0px;\n"
" border-right: 2px solid #a3a3a3;  /* 右边边框 */\n"
"    border-bottom: 2px solid #a3a3a3; /* 下边边框 */\n"
"margin-top: 0px;")
        self.pushButton_17.setObjectName("pushButton_17")
        self.horizontalLayout_24.addWidget(self.pushButton_17)
        spacerItem23 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_24.addItem(spacerItem23)
        self.label_56 = QtWidgets.QLabel(self.widget_26)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_56.sizePolicy().hasHeightForWidth())
        self.label_56.setSizePolicy(sizePolicy)
        self.label_56.setMinimumSize(QtCore.QSize(30, 30))
        self.label_56.setStyleSheet("background-color: rgb(88, 214, 92);\n"
"border-radius: 15px; \n"
"border: 1px solid gray;\n"
"margin-top: 0px;\n"
"")
        self.label_56.setText("")
        self.label_56.setObjectName("label_56")
        self.horizontalLayout_24.addWidget(self.label_56)
        spacerItem24 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_24.addItem(spacerItem24)
        self.lineEdit_35 = QtWidgets.QLineEdit(self.widget_26)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_35.sizePolicy().hasHeightForWidth())
        self.lineEdit_35.setSizePolicy(sizePolicy)
        self.lineEdit_35.setMinimumSize(QtCore.QSize(340, 35))
        self.lineEdit_35.setStyleSheet("background-color: #f9f9f9;\n"
"padding: 5px 10px;\n"
"border:none;\n"
"margin-top: 0px;")
        self.lineEdit_35.setObjectName("lineEdit_35")
        self.horizontalLayout_24.addWidget(self.lineEdit_35)
        self.verticalLayout_12.addWidget(self.widget_26)
        self.widget_25 = QtWidgets.QWidget(self.widget_14)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_25.sizePolicy().hasHeightForWidth())
        self.widget_25.setSizePolicy(sizePolicy)
        self.widget_25.setMinimumSize(QtCore.QSize(0, 45))
        self.widget_25.setStyleSheet("border:none\n"
"")
        self.widget_25.setObjectName("widget_25")
        self.horizontalLayout_23 = QtWidgets.QHBoxLayout(self.widget_25)
        self.horizontalLayout_23.setContentsMargins(-1, 5, -1, 0)
        self.horizontalLayout_23.setObjectName("horizontalLayout_23")
        self.pushButton_18 = QtWidgets.QPushButton(self.widget_25)
        self.pushButton_18.setMinimumSize(QtCore.QSize(250, 0))
        self.pushButton_18.setStyleSheet("background-color: #f4f4f4;\n"
"color: black;\n"
"   \n"
"padding: 5px 10px;\n"
"\n"
"border-left:0px;\n"
"border-top:0px;\n"
" border-right: 2px solid #a3a3a3;  /* 右边边框 */\n"
"    border-bottom: 2px solid #a3a3a3; /* 下边边框 */\n"
"margin-top: 0px;")
        self.pushButton_18.setObjectName("pushButton_18")
        self.horizontalLayout_23.addWidget(self.pushButton_18)
        spacerItem25 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_23.addItem(spacerItem25)
        self.label_54 = QtWidgets.QLabel(self.widget_25)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_54.sizePolicy().hasHeightForWidth())
        self.label_54.setSizePolicy(sizePolicy)
        self.label_54.setMinimumSize(QtCore.QSize(30, 30))
        self.label_54.setStyleSheet("background-color: rgb(88, 214, 92);\n"
"border-radius: 15px; \n"
"border: 1px solid gray;\n"
"margin-top: 0px;\n"
"")
        self.label_54.setText("")
        self.label_54.setObjectName("label_54")
        self.horizontalLayout_23.addWidget(self.label_54)
        spacerItem26 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_23.addItem(spacerItem26)
        self.lineEdit_34 = QtWidgets.QLineEdit(self.widget_25)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_34.sizePolicy().hasHeightForWidth())
        self.lineEdit_34.setSizePolicy(sizePolicy)
        self.lineEdit_34.setMinimumSize(QtCore.QSize(340, 35))
        self.lineEdit_34.setStyleSheet("background-color: #f9f9f9;\n"
"padding: 5px 10px;\n"
"border:none;\n"
"margin-top: 0px;")
        self.lineEdit_34.setObjectName("lineEdit_34")
        self.horizontalLayout_23.addWidget(self.lineEdit_34)
        self.verticalLayout_12.addWidget(self.widget_25)
        self.widget_21 = QtWidgets.QWidget(self.widget_14)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_21.sizePolicy().hasHeightForWidth())
        self.widget_21.setSizePolicy(sizePolicy)
        self.widget_21.setMinimumSize(QtCore.QSize(0, 45))
        self.widget_21.setStyleSheet("border:none\n"
"")
        self.widget_21.setObjectName("widget_21")
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout(self.widget_21)
        self.horizontalLayout_19.setContentsMargins(-1, 5, -1, 0)
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.pushButton_19 = QtWidgets.QPushButton(self.widget_21)
        self.pushButton_19.setMinimumSize(QtCore.QSize(250, 0))
        self.pushButton_19.setStyleSheet("background-color: #f4f4f4;\n"
"color: black;\n"
"   \n"
"padding: 5px 10px;\n"
"\n"
"border-left:0px;\n"
"border-top:0px;\n"
" border-right: 2px solid #a3a3a3;  /* 右边边框 */\n"
"    border-bottom: 2px solid #a3a3a3; /* 下边边框 */\n"
"margin-top: 0px;")
        self.pushButton_19.setObjectName("pushButton_19")
        self.horizontalLayout_19.addWidget(self.pushButton_19)
        spacerItem27 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_19.addItem(spacerItem27)
        self.label_45 = QtWidgets.QLabel(self.widget_21)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_45.sizePolicy().hasHeightForWidth())
        self.label_45.setSizePolicy(sizePolicy)
        self.label_45.setMinimumSize(QtCore.QSize(30, 30))
        self.label_45.setStyleSheet("background-color: rgb(88, 214, 92);\n"
"border-radius: 15px; \n"
"border: 1px solid gray;\n"
"margin-top: 0px;\n"
"")
        self.label_45.setText("")
        self.label_45.setObjectName("label_45")
        self.horizontalLayout_19.addWidget(self.label_45)
        spacerItem28 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_19.addItem(spacerItem28)
        self.lineEdit_30 = QtWidgets.QLineEdit(self.widget_21)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_30.sizePolicy().hasHeightForWidth())
        self.lineEdit_30.setSizePolicy(sizePolicy)
        self.lineEdit_30.setMinimumSize(QtCore.QSize(340, 35))
        self.lineEdit_30.setStyleSheet("background-color: #f9f9f9;\n"
"padding: 5px 10px;\n"
"border:none;\n"
"margin-top: 0px;")
        self.lineEdit_30.setObjectName("lineEdit_30")
        self.horizontalLayout_19.addWidget(self.lineEdit_30)
        self.verticalLayout_12.addWidget(self.widget_21)
        self.verticalLayout_16.addWidget(self.widget_14)
        self.verticalLayout_2.addWidget(self.groupBox_5)
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupTarget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setMinimumSize(QtCore.QSize(0, 50))
        self.groupBox_4.setStyleSheet("font: 15pt \"Adobe 黑体 Std R\";\n"
"border-color: rgb(249, 249, 249);\n"
"border: 3px solid #f9f9f9;      /* 边框粗细+颜色 */\n"
"border-radius: 8px;         /* 圆角半径 */\n"
"margin-top: 1ex;\n"
"color:white\n"
"")
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_8.setContentsMargins(-1, 9, -1, 5)
        self.verticalLayout_8.setSpacing(18)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.logText_2 = QtWidgets.QPlainTextEdit(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logText_2.sizePolicy().hasHeightForWidth())
        self.logText_2.setSizePolicy(sizePolicy)
        self.logText_2.setMinimumSize(QtCore.QSize(800, 60))
        self.logText_2.setMaximumSize(QtCore.QSize(800, 1000))
        font = QtGui.QFont()
        font.setFamily("Adobe 黑体 Std R")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.logText_2.setFont(font)
        self.logText_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.logText_2.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.logText_2.setReadOnly(True)
        self.logText_2.setBackgroundVisible(False)
        self.logText_2.setCenterOnScroll(False)
        self.logText_2.setObjectName("logText_2")
        self.verticalLayout_8.addWidget(self.logText_2)
        self.verticalLayout_2.addWidget(self.groupBox_4)
        self.horizontalLayout_5.addWidget(self.groupTarget)
        self.groupMonitor = QtWidgets.QGroupBox(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupMonitor.sizePolicy().hasHeightForWidth())
        self.groupMonitor.setSizePolicy(sizePolicy)
        self.groupMonitor.setMinimumSize(QtCore.QSize(680, 0))
        self.groupMonitor.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.groupMonitor.setFont(font)
        self.groupMonitor.setStyleSheet("")
        self.groupMonitor.setTitle("")
        self.groupMonitor.setObjectName("groupMonitor")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupMonitor)
        self.verticalLayout.setContentsMargins(20, -1, -1, 4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupMonitor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setMinimumSize(QtCore.QSize(0, 375))
        self.groupBox_3.setStyleSheet("font: 15pt \"Adobe 黑体 Std R\";\n"
"border-color: rgb(249, 249, 249);\n"
"border: 3px solid #f9f9f9;      /* 边框粗细+颜色 */\n"
"border-radius: 8px;         /* 圆角半径 */\n"
"margin-top: 1ex;\n"
"color:white\n"
"")
        self.groupBox_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.VisionPictureRGB_2 = QtWidgets.QLabel(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.VisionPictureRGB_2.sizePolicy().hasHeightForWidth())
        self.VisionPictureRGB_2.setSizePolicy(sizePolicy)
        self.VisionPictureRGB_2.setMinimumSize(QtCore.QSize(467, 336))
        self.VisionPictureRGB_2.setStyleSheet("border-radius: 0px; \n"
"border:none;\n"
"background-color: rgb(255, 255, 255);")
        self.VisionPictureRGB_2.setText("")
        self.VisionPictureRGB_2.setAlignment(QtCore.Qt.AlignCenter)
        self.VisionPictureRGB_2.setObjectName("VisionPictureRGB_2")
        self.horizontalLayout_7.addWidget(self.VisionPictureRGB_2)
        self.widget_4 = QtWidgets.QWidget(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy)
        self.widget_4.setMinimumSize(QtCore.QSize(400, 0))
        self.widget_4.setStyleSheet("border-color: rgb(173, 178, 181);\n"
"background-color:#d3d3d3;\n"
"border-radius: 0px; \n"
"color:black;\n"
"font: 14pt \"Adobe 黑体 Std R\";\n"
"")
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget_10 = QtWidgets.QWidget(self.widget_4)
        self.widget_10.setStyleSheet("border:none\n"
"")
        self.widget_10.setObjectName("widget_10")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.widget_10)
        self.verticalLayout_7.setContentsMargins(-1, 0, -1, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label = QtWidgets.QLabel(self.widget_10)
        self.label.setObjectName("label")
        self.verticalLayout_7.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.widget_10)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_7.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.widget_10)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_7.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(self.widget_10)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_7.addWidget(self.label_4)
        self.label_6 = QtWidgets.QLabel(self.widget_10)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_7.addWidget(self.label_6)
        self.label_32 = QtWidgets.QLabel(self.widget_10)
        self.label_32.setObjectName("label_32")
        self.verticalLayout_7.addWidget(self.label_32)
        self.horizontalLayout.addWidget(self.widget_10)
        self.widget_19 = QtWidgets.QWidget(self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_19.sizePolicy().hasHeightForWidth())
        self.widget_19.setSizePolicy(sizePolicy)
        self.widget_19.setStyleSheet("border:none\n"
"")
        self.widget_19.setObjectName("widget_19")
        self.verticalLayout_20 = QtWidgets.QVBoxLayout(self.widget_19)
        self.verticalLayout_20.setContentsMargins(0, 7, 0, 0)
        self.verticalLayout_20.setSpacing(7)
        self.verticalLayout_20.setObjectName("verticalLayout_20")
        self.lineEdit_24 = QtWidgets.QLineEdit(self.widget_19)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_24.sizePolicy().hasHeightForWidth())
        self.lineEdit_24.setSizePolicy(sizePolicy)
        self.lineEdit_24.setMinimumSize(QtCore.QSize(100, 0))
        self.lineEdit_24.setStyleSheet("background-color: #f9f9f9;\n"
"padding: 5px 10px;\n"
"border:none;\n"
"margin-top: 0px;")
        self.lineEdit_24.setObjectName("lineEdit_24")
        self.verticalLayout_20.addWidget(self.lineEdit_24)
        self.lineEdit_25 = QtWidgets.QLineEdit(self.widget_19)
        self.lineEdit_25.setStyleSheet("background-color: #f9f9f9;\n"
"padding: 5px 10px;\n"
"border:none;\n"
"margin-top: 0px;")
        self.lineEdit_25.setObjectName("lineEdit_25")
        self.verticalLayout_20.addWidget(self.lineEdit_25)
        self.lineEdit_26 = QtWidgets.QLineEdit(self.widget_19)
        self.lineEdit_26.setStyleSheet("background-color: #f9f9f9;\n"
"padding: 5px 10px;\n"
"border:none;\n"
"margin-top: 0px;")
        self.lineEdit_26.setObjectName("lineEdit_26")
        self.verticalLayout_20.addWidget(self.lineEdit_26)
        self.lineEdit_27 = QtWidgets.QLineEdit(self.widget_19)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_27.sizePolicy().hasHeightForWidth())
        self.lineEdit_27.setSizePolicy(sizePolicy)
        self.lineEdit_27.setStyleSheet("background-color: #f9f9f9;\n"
"padding: 5px 10px;\n"
"border:none;\n"
"margin-top: 0px;")
        self.lineEdit_27.setObjectName("lineEdit_27")
        self.verticalLayout_20.addWidget(self.lineEdit_27)
        self.lineEdit_28 = QtWidgets.QLineEdit(self.widget_19)
        self.lineEdit_28.setStyleSheet("background-color: #f9f9f9;\n"
"padding: 5px 10px;\n"
"border:none;\n"
"margin-top: 0px;")
        self.lineEdit_28.setObjectName("lineEdit_28")
        self.verticalLayout_20.addWidget(self.lineEdit_28)
        self.lineEdit_29 = QtWidgets.QLineEdit(self.widget_19)
        self.lineEdit_29.setStyleSheet("background-color: #f9f9f9;\n"
"padding: 5px 10px;\n"
"border:none;\n"
"margin-top: 0px;")
        self.lineEdit_29.setObjectName("lineEdit_29")
        self.verticalLayout_20.addWidget(self.lineEdit_29)
        self.horizontalLayout.addWidget(self.widget_19)
        self.widget_12 = QtWidgets.QWidget(self.widget_4)
        self.widget_12.setStyleSheet("border:none\n"
"")
        self.widget_12.setObjectName("widget_12")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.widget_12)
        self.verticalLayout_17.setContentsMargins(-1, 0, -1, 0)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.label_37 = QtWidgets.QLabel(self.widget_12)
        self.label_37.setObjectName("label_37")
        self.verticalLayout_17.addWidget(self.label_37)
        self.label_38 = QtWidgets.QLabel(self.widget_12)
        self.label_38.setObjectName("label_38")
        self.verticalLayout_17.addWidget(self.label_38)
        self.label_39 = QtWidgets.QLabel(self.widget_12)
        self.label_39.setObjectName("label_39")
        self.verticalLayout_17.addWidget(self.label_39)
        self.label_40 = QtWidgets.QLabel(self.widget_12)
        self.label_40.setObjectName("label_40")
        self.verticalLayout_17.addWidget(self.label_40)
        self.label_41 = QtWidgets.QLabel(self.widget_12)
        self.label_41.setObjectName("label_41")
        self.verticalLayout_17.addWidget(self.label_41)
        self.label_33 = QtWidgets.QLabel(self.widget_12)
        self.label_33.setObjectName("label_33")
        self.verticalLayout_17.addWidget(self.label_33)
        self.horizontalLayout.addWidget(self.widget_12)
        self.widget_18 = QtWidgets.QWidget(self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_18.sizePolicy().hasHeightForWidth())
        self.widget_18.setSizePolicy(sizePolicy)
        self.widget_18.setStyleSheet("border:none\n"
"")
        self.widget_18.setObjectName("widget_18")
        self.verticalLayout_19 = QtWidgets.QVBoxLayout(self.widget_18)
        self.verticalLayout_19.setContentsMargins(0, 7, 0, 0)
        self.verticalLayout_19.setSpacing(7)
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        self.lineEdit_18 = QtWidgets.QLineEdit(self.widget_18)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_18.sizePolicy().hasHeightForWidth())
        self.lineEdit_18.setSizePolicy(sizePolicy)
        self.lineEdit_18.setMinimumSize(QtCore.QSize(100, 0))
        self.lineEdit_18.setStyleSheet("background-color: #f9f9f9;\n"
"padding: 5px 10px;\n"
"border:none;\n"
"margin-top: 0px;")
        self.lineEdit_18.setObjectName("lineEdit_18")
        self.verticalLayout_19.addWidget(self.lineEdit_18)
        self.lineEdit_19 = QtWidgets.QLineEdit(self.widget_18)
        self.lineEdit_19.setStyleSheet("background-color: #f9f9f9;\n"
"padding: 5px 10px;\n"
"border:none;\n"
"margin-top: 0px;")
        self.lineEdit_19.setObjectName("lineEdit_19")
        self.verticalLayout_19.addWidget(self.lineEdit_19)
        self.lineEdit_20 = QtWidgets.QLineEdit(self.widget_18)
        self.lineEdit_20.setStyleSheet("background-color: #f9f9f9;\n"
"padding: 5px 10px;\n"
"border:none;\n"
"margin-top: 0px;")
        self.lineEdit_20.setObjectName("lineEdit_20")
        self.verticalLayout_19.addWidget(self.lineEdit_20)
        self.lineEdit_21 = QtWidgets.QLineEdit(self.widget_18)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_21.sizePolicy().hasHeightForWidth())
        self.lineEdit_21.setSizePolicy(sizePolicy)
        self.lineEdit_21.setStyleSheet("background-color: #f9f9f9;\n"
"padding: 5px 10px;\n"
"border:none;\n"
"margin-top: 0px;")
        self.lineEdit_21.setObjectName("lineEdit_21")
        self.verticalLayout_19.addWidget(self.lineEdit_21)
        self.lineEdit_22 = QtWidgets.QLineEdit(self.widget_18)
        self.lineEdit_22.setStyleSheet("background-color: #f9f9f9;\n"
"padding: 5px 10px;\n"
"border:none;\n"
"margin-top: 0px;")
        self.lineEdit_22.setObjectName("lineEdit_22")
        self.verticalLayout_19.addWidget(self.lineEdit_22)
        self.lineEdit_23 = QtWidgets.QLineEdit(self.widget_18)
        self.lineEdit_23.setStyleSheet("background-color: #f9f9f9;\n"
"padding: 5px 10px;\n"
"border:none;\n"
"margin-top: 0px;")
        self.lineEdit_23.setObjectName("lineEdit_23")
        self.verticalLayout_19.addWidget(self.lineEdit_23)
        self.horizontalLayout.addWidget(self.widget_18)
        self.horizontalLayout_7.addWidget(self.widget_4)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.groupBox_31 = QtWidgets.QGroupBox(self.groupMonitor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_31.sizePolicy().hasHeightForWidth())
        self.groupBox_31.setSizePolicy(sizePolicy)
        self.groupBox_31.setStyleSheet("font: 15pt \"Adobe 黑体 Std R\";\n"
"border-color: rgb(249, 249, 249);\n"
"border: 3px solid #f9f9f9;      /* 边框粗细+颜色 */\n"
"border-radius: 8px;         /* 圆角半径 */\n"
"margin-top: 1ex;\n"
"color:white\n"
"")
        self.groupBox_31.setObjectName("groupBox_31")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_31)
        self.verticalLayout_3.setContentsMargins(-1, 25, -1, 5)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tableWidget_2 = QtWidgets.QTableWidget(self.groupBox_31)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget_2.sizePolicy().hasHeightForWidth())
        self.tableWidget_2.setSizePolicy(sizePolicy)
        self.tableWidget_2.setMinimumSize(QtCore.QSize(0, 25))
        self.tableWidget_2.setStyleSheet("\n"
"background-color:rgb(255, 255, 255);\n"
"border-radius: 0px; \n"
"color:black;\n"
"font: 14pt \"Adobe 黑体 Std R\";\n"
"\n"
"margin-top: 0ex;\n"
"border: 0px ;      /* 边框粗细+颜色 */\n"
"\n"
"\n"
"\n"
"")
        self.tableWidget_2.setInputMethodHints(QtCore.Qt.ImhNone)
        self.tableWidget_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tableWidget_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.tableWidget_2.setLineWidth(100)
        self.tableWidget_2.setMidLineWidth(100)
        self.tableWidget_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidget_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidget_2.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.tableWidget_2.setAutoScroll(True)
        self.tableWidget_2.setDragEnabled(False)
        self.tableWidget_2.setAlternatingRowColors(True)
        self.tableWidget_2.setGridStyle(QtCore.Qt.DashLine)
        self.tableWidget_2.setRowCount(13)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(5)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(85, 255, 127))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.tableWidget_2.setItem(2, 0, item)
        self.tableWidget_2.horizontalHeader().setVisible(True)
        self.tableWidget_2.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_2.horizontalHeader().setDefaultSectionSize(150)
        self.tableWidget_2.horizontalHeader().setHighlightSections(True)
        self.tableWidget_2.horizontalHeader().setMinimumSectionSize(33)
        self.tableWidget_2.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget_2.horizontalHeader().setStretchLastSection(False)
        self.tableWidget_2.verticalHeader().setVisible(True)
        self.tableWidget_2.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget_2.verticalHeader().setDefaultSectionSize(44)
        self.tableWidget_2.verticalHeader().setHighlightSections(False)
        self.tableWidget_2.verticalHeader().setMinimumSectionSize(39)
        self.tableWidget_2.verticalHeader().setSortIndicatorShown(False)
        self.tableWidget_2.verticalHeader().setStretchLastSection(False)
        self.verticalLayout_3.addWidget(self.tableWidget_2)
        self.verticalLayout.addWidget(self.groupBox_31)
        self.groupBox = QtWidgets.QGroupBox(self.groupMonitor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setStyleSheet("font: 15pt \"Adobe 黑体 Std R\";\n"
"border-color: rgb(249, 249, 249);\n"
"border: 3px solid #f9f9f9;      /* 边框粗细+颜色 */\n"
"border-radius: 8px;         /* 圆角半径 */\n"
"margin-top: 1ex;\n"
"color:white\n"
"")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_6.setContentsMargins(-1, -1, -1, 5)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.widget_5 = QtWidgets.QWidget(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_5.sizePolicy().hasHeightForWidth())
        self.widget_5.setSizePolicy(sizePolicy)
        self.widget_5.setStyleSheet("border-color: rgb(173, 178, 181);\n"
"background-color:#d3d3d3;\n"
"border-radius: 0px; \n"
"color:black;\n"
"font: 14pt \"Adobe 黑体 Std R\";\n"
"\n"
"")
        self.widget_5.setObjectName("widget_5")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.widget_5)
        self.verticalLayout_11.setContentsMargins(-1, 16, -1, 2)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.widget_6 = QtWidgets.QWidget(self.widget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_6.sizePolicy().hasHeightForWidth())
        self.widget_6.setSizePolicy(sizePolicy)
        self.widget_6.setMinimumSize(QtCore.QSize(0, 0))
        self.widget_6.setStyleSheet("border:none;\n"
"margin-top: 0px;\n"
"\n"
"")
        self.widget_6.setObjectName("widget_6")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_6)
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_14 = QtWidgets.QLabel(self.widget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        self.label_14.setStyleSheet("")
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_4.addWidget(self.label_14)
        self.label_15 = QtWidgets.QLabel(self.widget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        self.label_15.setStyleSheet("")
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_4.addWidget(self.label_15)
        self.label_16 = QtWidgets.QLabel(self.widget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy)
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_4.addWidget(self.label_16)
        self.label_17 = QtWidgets.QLabel(self.widget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy)
        self.label_17.setAlignment(QtCore.Qt.AlignCenter)
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_4.addWidget(self.label_17)
        self.label_18 = QtWidgets.QLabel(self.widget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy)
        self.label_18.setAlignment(QtCore.Qt.AlignCenter)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_4.addWidget(self.label_18)
        self.label_19 = QtWidgets.QLabel(self.widget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy)
        self.label_19.setMinimumSize(QtCore.QSize(0, 0))
        self.label_19.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_19.setLineWidth(1)
        self.label_19.setAlignment(QtCore.Qt.AlignCenter)
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_4.addWidget(self.label_19)
        self.verticalLayout_11.addWidget(self.widget_6)
        self.widget_7 = QtWidgets.QWidget(self.widget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_7.sizePolicy().hasHeightForWidth())
        self.widget_7.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Adobe 黑体 Std R")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.widget_7.setFont(font)
        self.widget_7.setStyleSheet("border:none;\n"
"margin-top: 0px;\n"
"\n"
"")
        self.widget_7.setObjectName("widget_7")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.widget_7)
        self.horizontalLayout_6.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_6.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem29 = QtWidgets.QSpacerItem(45, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem29)
        self.label_20 = QtWidgets.QLabel(self.widget_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy)
        self.label_20.setMinimumSize(QtCore.QSize(30, 30))
        self.label_20.setStyleSheet("background-color: rgb(88, 214, 92);\n"
"border-radius: 15px; \n"
"border: 1px solid gray;\n"
"margin-top: 0px;\n"
"")
        self.label_20.setText("")
        self.label_20.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_20.setObjectName("label_20")
        self.horizontalLayout_6.addWidget(self.label_20)
        spacerItem30 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem30)
        self.label_21 = QtWidgets.QLabel(self.widget_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy)
        self.label_21.setMinimumSize(QtCore.QSize(30, 30))
        self.label_21.setStyleSheet("background-color: rgb(88, 214, 92);\n"
"border-radius: 15px; \n"
"border: 1px solid gray;\n"
"margin-top: 0px;\n"
"")
        self.label_21.setText("")
        self.label_21.setAlignment(QtCore.Qt.AlignCenter)
        self.label_21.setObjectName("label_21")
        self.horizontalLayout_6.addWidget(self.label_21)
        spacerItem31 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem31)
        self.label_22 = QtWidgets.QLabel(self.widget_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy)
        self.label_22.setMinimumSize(QtCore.QSize(30, 30))
        self.label_22.setStyleSheet("background-color: rgb(88, 214, 92);\n"
"border-radius: 15px; \n"
"border: 1px solid gray;\n"
"margin-top: 0px;\n"
"")
        self.label_22.setText("")
        self.label_22.setAlignment(QtCore.Qt.AlignCenter)
        self.label_22.setObjectName("label_22")
        self.horizontalLayout_6.addWidget(self.label_22)
        spacerItem32 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem32)
        self.label_23 = QtWidgets.QLabel(self.widget_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy)
        self.label_23.setMinimumSize(QtCore.QSize(30, 30))
        self.label_23.setStyleSheet("background-color: rgb(88, 214, 92);\n"
"border-radius: 15px; \n"
"border: 1px solid gray;\n"
"margin-top: 0px;\n"
"")
        self.label_23.setText("")
        self.label_23.setAlignment(QtCore.Qt.AlignCenter)
        self.label_23.setObjectName("label_23")
        self.horizontalLayout_6.addWidget(self.label_23)
        spacerItem33 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem33)
        self.label_24 = QtWidgets.QLabel(self.widget_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_24.sizePolicy().hasHeightForWidth())
        self.label_24.setSizePolicy(sizePolicy)
        self.label_24.setMinimumSize(QtCore.QSize(30, 30))
        self.label_24.setStyleSheet("background-color: rgb(88, 214, 92);\n"
"border-radius: 15px; \n"
"border: 1px solid gray;\n"
"margin-top: 0px;\n"
"")
        self.label_24.setText("")
        self.label_24.setAlignment(QtCore.Qt.AlignCenter)
        self.label_24.setObjectName("label_24")
        self.horizontalLayout_6.addWidget(self.label_24)
        spacerItem34 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem34)
        self.label_25 = QtWidgets.QLabel(self.widget_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_25.sizePolicy().hasHeightForWidth())
        self.label_25.setSizePolicy(sizePolicy)
        self.label_25.setMinimumSize(QtCore.QSize(30, 30))
        self.label_25.setStyleSheet("background-color: rgb(88, 214, 92);\n"
"border-radius: 15px; \n"
"border: 1px solid gray;\n"
"margin-top: 0px;\n"
"")
        self.label_25.setText("")
        self.label_25.setAlignment(QtCore.Qt.AlignCenter)
        self.label_25.setObjectName("label_25")
        self.horizontalLayout_6.addWidget(self.label_25)
        spacerItem35 = QtWidgets.QSpacerItem(45, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem35)
        self.verticalLayout_11.addWidget(self.widget_7)
        self.widget_9 = QtWidgets.QWidget(self.widget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_9.sizePolicy().hasHeightForWidth())
        self.widget_9.setSizePolicy(sizePolicy)
        self.widget_9.setStyleSheet("border:none;\n"
"margin-top: 0px;\n"
"")
        self.widget_9.setObjectName("widget_9")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.widget_9)
        self.horizontalLayout_8.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_7 = QtWidgets.QLabel(self.widget_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_8.addWidget(self.label_7)
        self.label_8 = QtWidgets.QLabel(self.widget_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_8.addWidget(self.label_8)
        self.label_9 = QtWidgets.QLabel(self.widget_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_8.addWidget(self.label_9)
        self.label_10 = QtWidgets.QLabel(self.widget_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_8.addWidget(self.label_10)
        self.label_11 = QtWidgets.QLabel(self.widget_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_8.addWidget(self.label_11)
        self.label_12 = QtWidgets.QLabel(self.widget_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_8.addWidget(self.label_12)
        self.verticalLayout_11.addWidget(self.widget_9)
        self.widget_8 = QtWidgets.QWidget(self.widget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_8.sizePolicy().hasHeightForWidth())
        self.widget_8.setSizePolicy(sizePolicy)
        self.widget_8.setStyleSheet("border:none;\n"
"margin-top: 0px;\n"
"")
        self.widget_8.setObjectName("widget_8")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.widget_8)
        self.horizontalLayout_10.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        spacerItem36 = QtWidgets.QSpacerItem(45, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem36)
        self.label_26 = QtWidgets.QLabel(self.widget_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_26.sizePolicy().hasHeightForWidth())
        self.label_26.setSizePolicy(sizePolicy)
        self.label_26.setMinimumSize(QtCore.QSize(30, 30))
        self.label_26.setStyleSheet("background-color: rgb(88, 214, 92);\n"
"border-radius: 15px; \n"
"border: 1px solid gray;\n"
"margin-top: 0px;\n"
"")
        self.label_26.setText("")
        self.label_26.setAlignment(QtCore.Qt.AlignCenter)
        self.label_26.setObjectName("label_26")
        self.horizontalLayout_10.addWidget(self.label_26)
        spacerItem37 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem37)
        self.label_27 = QtWidgets.QLabel(self.widget_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_27.sizePolicy().hasHeightForWidth())
        self.label_27.setSizePolicy(sizePolicy)
        self.label_27.setMinimumSize(QtCore.QSize(30, 30))
        self.label_27.setStyleSheet("background-color: rgb(88, 214, 92);\n"
"border-radius: 15px; \n"
"border: 1px solid gray;\n"
"margin-top: 0px;\n"
"")
        self.label_27.setText("")
        self.label_27.setAlignment(QtCore.Qt.AlignCenter)
        self.label_27.setObjectName("label_27")
        self.horizontalLayout_10.addWidget(self.label_27)
        spacerItem38 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem38)
        self.label_28 = QtWidgets.QLabel(self.widget_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_28.sizePolicy().hasHeightForWidth())
        self.label_28.setSizePolicy(sizePolicy)
        self.label_28.setMinimumSize(QtCore.QSize(30, 30))
        self.label_28.setStyleSheet("background-color: rgb(88, 214, 92);\n"
"border-radius: 15px; \n"
"border: 1px solid gray;\n"
"margin-top: 0px;\n"
"")
        self.label_28.setText("")
        self.label_28.setAlignment(QtCore.Qt.AlignCenter)
        self.label_28.setObjectName("label_28")
        self.horizontalLayout_10.addWidget(self.label_28)
        spacerItem39 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem39)
        self.label_29 = QtWidgets.QLabel(self.widget_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_29.sizePolicy().hasHeightForWidth())
        self.label_29.setSizePolicy(sizePolicy)
        self.label_29.setMinimumSize(QtCore.QSize(30, 30))
        self.label_29.setStyleSheet("background-color: rgb(88, 214, 92);\n"
"border-radius: 15px; \n"
"border: 1px solid gray;\n"
"margin-top: 0px;\n"
"")
        self.label_29.setText("")
        self.label_29.setAlignment(QtCore.Qt.AlignCenter)
        self.label_29.setObjectName("label_29")
        self.horizontalLayout_10.addWidget(self.label_29)
        spacerItem40 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem40)
        self.label_30 = QtWidgets.QLabel(self.widget_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_30.sizePolicy().hasHeightForWidth())
        self.label_30.setSizePolicy(sizePolicy)
        self.label_30.setMinimumSize(QtCore.QSize(30, 30))
        self.label_30.setStyleSheet("background-color: rgb(88, 214, 92);\n"
"border-radius: 15px; \n"
"border: 1px solid gray;\n"
"margin-top: 0px;\n"
"\n"
"")
        self.label_30.setText("")
        self.label_30.setAlignment(QtCore.Qt.AlignCenter)
        self.label_30.setObjectName("label_30")
        self.horizontalLayout_10.addWidget(self.label_30)
        spacerItem41 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem41)
        self.label_31 = QtWidgets.QLabel(self.widget_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_31.sizePolicy().hasHeightForWidth())
        self.label_31.setSizePolicy(sizePolicy)
        self.label_31.setMinimumSize(QtCore.QSize(30, 30))
        self.label_31.setStyleSheet("background-color: rgb(88, 214, 92);\n"
"border-radius: 15px; \n"
"border: 1px solid gray;\n"
"margin-top: 0px;\n"
"")
        self.label_31.setText("")
        self.label_31.setAlignment(QtCore.Qt.AlignCenter)
        self.label_31.setObjectName("label_31")
        self.horizontalLayout_10.addWidget(self.label_31)
        spacerItem42 = QtWidgets.QSpacerItem(45, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem42)
        self.verticalLayout_11.addWidget(self.widget_8)
        self.verticalLayout_6.addWidget(self.widget_5)
        self.verticalLayout.addWidget(self.groupBox)
        self.horizontalLayout_5.addWidget(self.groupMonitor)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        self.verticalLayout_5.setStretch(0, 1)
        self.gridLayout_6.addLayout(self.verticalLayout_5, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.open_camera_flag = False
        # 初始化连接
        self.tc3 = TwinCat3_ADSserver()

    def add_adsvars(self):
        # 添加要监控的变量
        for i in range(7):
            self.tc3.add_variable(f"MAIN.axis_pos[{i+1}]", pyads.PLCTYPE_LREAL, self.value_changed)

    # 定义回调函数
    def value_changed(self, name, value):
        print(f"变量更新: {name} = {value}")

    def update_image(self, image):
        # Update the image_label with a new image
        self.VisionPictureRGB_2.setPixmap(QPixmap.fromImage(image))

    def open_connect(self):
        self.tc3.connect()
        print("已连接twincat")
        self.add_adsvars()
        self.tc3.start_thread()


    def open_camera(self):
        if self.open_camera_flag:
            self.thread.stop_camera()
            self.open_camera_flag = False
            self.pushButton_8.setText("开启相机")
            self.VisionPictureRGB_2.setPixmap(QPixmap(""))
        else:
            self.thread = VideoThread()
            # Connect the signal from the thread to the update_image slot
            self.thread.change_pixmap_signal.connect(self.update_image)
            self.thread.start_camera()
            self.open_camera_flag = True
            self.pushButton_8.setText("关闭相机")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "空间碎片抓捕地面实验系统"))
        self.label_5.setText(_translate("MainWindow", "空 间 碎 片 抓 捕 实 验 系 统"))
        self.SingleMachine.setTitle(_translate("MainWindow", "总体控制"))
        self.pushButton_6.setText(_translate("MainWindow", "启动"))
        self.pushButton_8.setText(_translate("MainWindow", "开启相机"))
        self.pushButton_2.setText(_translate("MainWindow", "开启电机"))
        self.pushButton_7.setText(_translate("MainWindow", "开启六维力"))
        self.label_36.setText(_translate("MainWindow", "IP:"))
        self.SingleMachine_2.setTitle(_translate("MainWindow", "单机调试"))
        self.pushButton_9.setText(_translate("MainWindow", "启动"))
        self.pushButton_10.setText(_translate("MainWindow", "正转"))
        self.pushButton_11.setText(_translate("MainWindow", "反转"))
        self.label_43.setText(_translate("MainWindow", "位置"))
        self.pushButton_12.setText(_translate("MainWindow", "停止"))
        self.pushButton_13.setText(_translate("MainWindow", "复位"))
        self.pushButton_14.setText(_translate("MainWindow", "回零"))
        self.pushButton_15.setText(_translate("MainWindow", "移动"))
        self.label_44.setText(_translate("MainWindow", "速度"))
        self.groupBox_5.setTitle(_translate("MainWindow", "分系统流程"))
        self.pushButton.setText(_translate("MainWindow", "机构展开"))
        self.pushButton_3.setText(_translate("MainWindow", "捕获舱门打开"))
        self.pushButton_4.setText(_translate("MainWindow", "目标抓捕"))
        self.pushButton_5.setText(_translate("MainWindow", "捕获舱门关闭"))
        self.pushButton_16.setText(_translate("MainWindow", "转移对接"))
        self.pushButton_17.setText(_translate("MainWindow", "转移舱门打开"))
        self.pushButton_18.setText(_translate("MainWindow", "机构收拢"))
        self.pushButton_19.setText(_translate("MainWindow", "目标推送"))
        self.groupBox_4.setTitle(_translate("MainWindow", "日志"))
        self.groupBox_3.setTitle(_translate("MainWindow", "采集图像"))
        self.label.setText(_translate("MainWindow", "X"))
        self.label_2.setText(_translate("MainWindow", "Y"))
        self.label_3.setText(_translate("MainWindow", "Z"))
        self.label_4.setText(_translate("MainWindow", "Rr"))
        self.label_6.setText(_translate("MainWindow", "Rp"))
        self.label_32.setText(_translate("MainWindow", "Ry"))
        self.label_37.setText(_translate("MainWindow", "Fx"))
        self.label_38.setText(_translate("MainWindow", "Fy"))
        self.label_39.setText(_translate("MainWindow", "Fz"))
        self.label_40.setText(_translate("MainWindow", "Tx"))
        self.label_41.setText(_translate("MainWindow", "Ty"))
        self.label_33.setText(_translate("MainWindow", "Tz"))
        self.groupBox_31.setTitle(_translate("MainWindow", "电机"))
        self.tableWidget_2.setSortingEnabled(False)
        item = self.tableWidget_2.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "捕获电机1"))
        item = self.tableWidget_2.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "捕获电机2"))
        item = self.tableWidget_2.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "捕获电机3"))
        item = self.tableWidget_2.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "捕获电机4"))
        item = self.tableWidget_2.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "捕获电机5"))
        item = self.tableWidget_2.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "捕获电机6"))
        item = self.tableWidget_2.verticalHeaderItem(6)
        item.setText(_translate("MainWindow", "关节电机1"))
        item = self.tableWidget_2.verticalHeaderItem(7)
        item.setText(_translate("MainWindow", "关节电机2"))
        item = self.tableWidget_2.verticalHeaderItem(8)
        item.setText(_translate("MainWindow", "关节电机3"))
        item = self.tableWidget_2.verticalHeaderItem(9)
        item.setText(_translate("MainWindow", "关节电机4"))
        item = self.tableWidget_2.verticalHeaderItem(10)
        item.setText(_translate("MainWindow", "关节电机5"))
        item = self.tableWidget_2.verticalHeaderItem(11)
        item.setText(_translate("MainWindow", "关节电机6"))
        item = self.tableWidget_2.verticalHeaderItem(12)
        item.setText(_translate("MainWindow", "关节电机7"))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "电机编号"))
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "电机状态"))
        item = self.tableWidget_2.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "电机转速"))
        item = self.tableWidget_2.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "移动距离"))
        item = self.tableWidget_2.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "报警号"))
        __sortingEnabled = self.tableWidget_2.isSortingEnabled()
        self.tableWidget_2.setSortingEnabled(False)
        self.tableWidget_2.setSortingEnabled(__sortingEnabled)
        self.groupBox.setTitle(_translate("MainWindow", "到位开关"))
        self.label_14.setText(_translate("MainWindow", "B1"))
        self.label_15.setText(_translate("MainWindow", "B2"))
        self.label_16.setText(_translate("MainWindow", "B3"))
        self.label_17.setText(_translate("MainWindow", "B4"))
        self.label_18.setText(_translate("MainWindow", "B5"))
        self.label_19.setText(_translate("MainWindow", "B6"))
        self.label_7.setText(_translate("MainWindow", "B7"))
        self.label_8.setText(_translate("MainWindow", "B8"))
        self.label_9.setText(_translate("MainWindow", "B9"))
        self.label_10.setText(_translate("MainWindow", "B10"))
        self.label_11.setText(_translate("MainWindow", "B11"))
        self.label_12.setText(_translate("MainWindow", "B12"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))




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

                img_color = cv2.resize(img_color, (467, 336))  # 注意参数是 (width, height)

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