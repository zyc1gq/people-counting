# -*- coding: cp936 -*-
import sys
from PyQt5.QtWidgets import (QWidget, QHBoxLayout,
                             QLabel, QApplication)
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QGridLayout
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QTextEdit, QGridLayout, QApplication)
from PyQt5 import QtCore, QtGui, QtWidgets
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize, QPoint, QRect, QModelIndex

import numpy as np
import time
from imutils.object_detection import non_max_suppression

import Person
import sqllink


# 前面的库包含的贼   乱。。。

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.timer_camera = QtCore.QTimer()
        self.slot_init()
        self.__flag_work = 0
        self.x = 0
        self.now_per = 0
        self.per_in = 0
        self.per_out = 0
        self.per_all_static = 0
        # 初始化上面数据的时候是不是可以从数据库读入？
        self.cap = cv2.VideoCapture()
        self.time=time.time()

    def initUI(self):
        last_all_per=sqllink.init()#初始化得到之前总人数
        self.per_all_static=last_all_per

        self.move(300, 200)
        self.setWindowTitle('人数统计系统')
        # 设置背景图片
        window_pale = QtGui.QPalette()
        self.pixmap = QPixmap('ui.jpg')
        window_pale.setBrush(self.backgroundRole(), QtGui.QBrush(self.pixmap))
        self.setPalette(window_pale)

        # 定义两个框
        self.label_show_camera = QtWidgets.QLabel()
        self.label_show_camera.setFixedSize(0.4 * self.pixmap.width(), 0.6 * self.pixmap.height())
        self.label_show_camera.setAutoFillBackground(0)

        self.label_move = QtWidgets.QLabel()
        self.label_move.setFixedSize(0.6 * self.pixmap.width(), self.pixmap.height())
        # 定义文本框
        self.Edit1 = QLineEdit()  # 修改总人数
        self.Edit1.hide()
        self.Edit2 = QLineEdit()  # 修改当前人数
        self.Edit2.hide()
        # 定义按钮
        self.btn1 = QPushButton(self)
        self.btn1.setText("修改总人数")
        self.btn1.setShortcut('Ctrl+A')
        self.btn1.setToolTip("确认将总人数修改为左边设定的值")
        self.btn1.resize(self.btn1.sizeHint())
        self.btn1.hide()

        # 定义按钮
        self.btn2 = QPushButton(self)
        self.btn2.setText("修改当前人数")
        self.btn2.setShortcut('Ctrl+N')
        self.btn2.setToolTip("确认将当前人数修改为左边设定的值")
        self.btn2.resize(self.btn2.sizeHint())
        self.btn2.hide()

        # 定义按钮
        self.btn3 = QPushButton(self)
        self.btn3.setText("开始检测")
        self.btn3.setShortcut('Ctrl+S')
        self.btn3.setToolTip("开始进行检测")
        self.btn3.resize(self.btn3.sizeHint())
        self.btn3.hide()

        # 定义按钮
        self.btn4 = QPushButton(self)
        self.btn4.setText("结束检测")
        self.btn4.setShortcut('Ctrl+C')
        self.btn4.setToolTip("结束检测")
        self.btn4.resize(self.btn4.sizeHint())
        self.btn4.hide()

        # 定义按钮
        self.btn5 = QPushButton('MENU', self)
        self.btn5.setCheckable(True)
        self.btn5.setShortcut('Ctrl+M')
        self.btn5.setFlat(1)
        self.btn5.setStyleSheet("QPushButton{background: transparent;}");  # 将按钮背景设为透明
        # 当按下btn5时，显示所有按钮和输入框，再次按下时隐藏所有按钮和输入框


        # 以下是布局
        wlayout = QtWidgets.QHBoxLayout()  # 水平

        hlayout = QtWidgets.QHBoxLayout()
        vlayout = QtWidgets.QVBoxLayout()
        glayout = QtWidgets.QGridLayout()

        awg = QtWidgets.QWidget()
        bwg = QtWidgets.QWidget()
        gwg = QtWidgets.QWidget()
        vwg = QtWidgets.QWidget()

        a = QtWidgets.QHBoxLayout()
        a.addWidget(self.label_show_camera)
        awg.setLayout(a)

        glayout.addWidget(self.Edit1, 1, 0)
        glayout.addWidget(self.Edit2, 2, 0)
        glayout.addWidget(self.btn1, 1, 1)
        glayout.addWidget(self.btn2, 2, 1)
        glayout.addWidget(self.btn3, 3, 0)
        glayout.addWidget(self.btn4, 3, 1)
        gwg.setLayout(glayout)

        vlayout.addWidget(awg)
        vlayout.addWidget(gwg)
        vwg.setLayout(vlayout)

        b = QtWidgets.QHBoxLayout()
        b.addWidget(self.label_move)
        bwg.setLayout(b)

        hlayout.addWidget(vwg)
        hlayout.addWidget(bwg)
        self.setLayout(hlayout)
        # 显示界面
        self.show()

    def slot_init(self):
        self.timer_camera.timeout.connect(self.show_camera)  # 计时结束时调用一次self.show_camera函数
        self.btn1.clicked.connect(self.btn1_click)
        self.btn2.clicked.connect(self.btn2_click)
        self.btn3.clicked.connect(self.button_open_camera_click)
        self.btn4.clicked.connect(self.button_close_camera_click)
        self.btn5.clicked[bool].connect(self.btn5_click)

    def button_open_camera_click(self):
        if self.timer_camera.isActive() == False:
            # self.cap = cv2.VideoCapture("test.mp4")
            # 打开摄像头 初始化和检测有关的所有变量
            self.persons = []
            self.pid = 0
            self.face_patterns = cv2.CascadeClassifier('cascades.xml')
            flag = self.cap.open(0)
            # self.width = self.cap.get(3)
            # self.hight = self.cap.get(4)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
            self.width = 1000
            self.hight = 520
            self.imgArea = self.width * self.hight
            self.areaTH = self.imgArea / 250
            self.areaTL = self.imgArea / 10
            self.font = cv2.FONT_HERSHEY_SIMPLEX
            # Lineas de entrada/salida
            self.line_up = int(2 * (self.hight / 5)) - 50
            self.line_down = int(3 * (self.hight / 5)) + 50

            self.up_limit = int(1 * (self.hight / 5)) - 50
            self.down_limit = int(4 * (self.hight / 5)) + 50
            """
            print(
                "h" + str(hight) + "  " + "w" + str(width) + "  " + "line_up" + str(line_up) + "  " + "line_down" + str(
                    line_down))
            print(str(up_limit) + "    " + str(down_limit))
            print("Red line y:", str(line_down))
            print("Blue line y:", str(line_up))
            """
            self.line_down_color = (255, 0, 0)
            self.line_up_color = (0, 0, 255)
            self.pt1 = [0, self.line_down]
            self.pt2 = [self.width, self.line_down]
            self.pts_L1 = np.array([self.pt1, self.pt2], np.int32)
            self.pts_L1 = self.pts_L1.reshape((-1, 1, 2))
            self.pt3 = [0, self.line_up]
            self.pt4 = [self.width, self.line_up]
            self.pts_L2 = np.array([self.pt3, self.pt4], np.int32)
            self.pts_L2 = self.pts_L2.reshape((-1, 1, 2))

            self.pt5 = [0, self.up_limit]
            self.pt6 = [self.width, self.up_limit]
            self.pts_L3 = np.array([self.pt5, self.pt6], np.int32)
            self.pts_L3 = self.pts_L3.reshape((-1, 1, 2))
            self.pt7 = [0, self.down_limit]
            self.pt8 = [self.width, self.down_limit]
            self.pts_L4 = np.array([self.pt7, self.pt8], np.int32)
            self.pts_L4 = self.pts_L4.reshape((-1, 1, 2))
            if flag == False:
                msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"请检测相机与电脑是否连接正确",
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)

            else:
                # 打开一个计时器
                self.timer_camera.start(30)
        else:
            pass

    def button_close_camera_click(self):
        # 关闭摄像头 停止定时器
        self.timer_camera.stop()
        self.cap.release()
        self.label_show_camera.clear()

    def btn2_click(self):
        # 从输入框获得当前人数 并更新界面（同时修改self.now_per和self.per_in）
        self.now_per = int(self.Edit2.text())
        self.per_in = int(self.Edit2.text())
        self.per_out = 0
        self.update()

    def btn1_click(self):
        # 从输入框获得总人数 并更新界面
        self.per_all_static = int(self.Edit1.text())
        self.update()

    def btn5_click(self, pressed):
        if pressed:
            # 按下btn5后显示所有按钮和输入框 快捷键ctrl+m
            self.Edit1.show()
            self.Edit2.show()
            self.btn1.show()
            self.btn2.show()
            self.btn3.show()
            self.btn4.show()
        else:
            # 隐藏所有按钮和输入框
            self.Edit1.hide()
            self.Edit2.hide()
            self.btn1.hide()
            self.btn2.hide()
            self.btn3.hide()
            self.btn4.hide()

    def show_camera(self):
        # 计时器每结束一次调用一次该函数

        flag, self.image = self.cap.read()

        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        # 人头统计
        # 以下代码为原detect_track.py中死循环中的部分


        self.now_per = self.per_in - self.per_out

        self.pid = self.pid % 1000

        try:
            self.image = cv2.resize(self.image, (1000, 520))
        except:
            print("测试结束")  # 一般是因为最后一帧无法处理？？？

        dets = self.face_patterns.detectMultiScale(self.image, scaleFactor=1.1, minNeighbors=3, minSize=(100, 100))
        rects = np.array([[x, y, w, h] for (x, y, w, h) in dets])
        detections = non_max_suppression(rects, probs=None, overlapThresh=0.6)

        for item in detections:
            (dx, dy, dw, dh) = item
            area = dw * dh
            if self.areaTH < area < self.areaTL:
                cx = int(dx + dw / 2)
                cy = int(dy + dh / 2)
                # print(str(cy)+"      "+str(dh))

                newrec = True
                if cy in range(self.up_limit, self.down_limit):
                    for i in self.persons:
                        if abs(cx - i.getX()) <= dw / 2 and abs(cy - i.getY()) <= dh / 2:
                            # el objeto esta cerca de uno que ya se detecto antes
                            newrec = False
                            i.updateCoords(cx, cy)  # actualiza coordenadas en el objeto and resets age
                            if i.going_UP(self.line_down, self.line_up):
                                self.per_all_static += 1  # 这个就在这里默默统计吧，可能一直用不上
                                self.per_in += 1
                                print("ID:", i.getId(), 'crossed going up at', time.strftime("%c"))
                            elif i.going_DOWN(self.line_down, self.line_up):
                                self.per_out += 1
                                print("ID:", i.getId(), 'crossed going down at', time.strftime("%c"))
                            break
                        if i.getState() == '1':
                            if i.getDir() == 'down' and i.getY() > self.down_limit:
                                i.setDone()
                            elif i.getDir() == 'up' and i.getY() < self.up_limit:
                                i.setDone()
                        if i.timedOut():
                            # sacar i de la lista persons
                            index = self.persons.index(i)
                            self.persons.pop(index)
                            del i  # liberar la memoria de i
                    if newrec:
                        p = Person.MyPerson(self.pid, cx, cy, 5)
                        self.persons.append(p)
                        self.pid += 1
                cv2.circle(self.image, (cx, cy), 5, (0, 0, 255), -1)
                self.image = cv2.rectangle(self.image, (dx, dy), (dx + dw, dy + dh), (0, 255, 0), 2)

        for pla, i in enumerate(self.persons):
            if i.getY() > self.down_limit or i.getY() < self.up_limit:
                del self.persons[pla]
            elif time.time() - i.getSP() >= 0.1:
                del self.persons[pla]
            else:
                cv2.putText(self.image, str(i.getId()), (i.getX(), i.getY()), self.font, 0.5, i.getRGB(), 1,
                            cv2.LINE_AA)

        str_up = 'UP: ' + str(self.per_in)
        str_down = 'DOWN: ' + str(self.per_out)
        self.image = cv2.polylines(self.image, [self.pts_L1], False, self.line_down_color, thickness=2)
        self.image = cv2.polylines(self.image, [self.pts_L2], False, self.line_up_color, thickness=2)
        self.image = cv2.polylines(self.image, [self.pts_L3], False, (255, 255, 255), thickness=1)
        self.image = cv2.polylines(self.image, [self.pts_L4], False, (255, 255, 255), thickness=1)
        cv2.putText(self.image, str_up, (10, 40), self.font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(self.image, str_up, (10, 40), self.font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.putText(self.image, str_down, (10, 90), self.font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(self.image, str_down, (10, 90), self.font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

        # 可以在这里添加数据库相关的代码

        # 在界面上显示
        self.image = cv2.resize(self.image, (640, 640))
        showImage = QtGui.QImage(self.image.data, self.image.shape[1], self.image.shape[0], QtGui.QImage.Format_RGB888)
        self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))
        self.update()  # 更新界面
        #if time.time()-self.now>=60:
        #    self.now=time.time()
         #   sqllink.insert(self.now_per,self.per_all_static)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        qp.end()

    def drawText(self, event, qp):
        self.text_1 = str(self.per_all_static)  # 当前人数
        self.text_2 = str(self.now_per)  # 总人数
        qp.setPen(QColor(168, 34, 3))
        qp.setFont(QFont('Impact', 100))
        qp.drawText(QRect(0.6*self.pixmap.width(), 0.5*self.pixmap.height(), 0.3 * self.pixmap.width(), 0.2 * self.pixmap.height()),
                    Qt.AlignHCenter | Qt.AlignVCenter, self.text_2)
        qp.drawText(QRect(0.6*self.pixmap.width(), 0.7*self.pixmap.height(), 0.3 * self.pixmap.width(), 0.2 * self.pixmap.height()),
                    Qt.AlignHCenter | Qt.AlignVCenter, self.text_1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
