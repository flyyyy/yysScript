# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'go.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject, Qt, pyqtSlot
import sys
import win32api
import win32gui
import win32con
import time
import random
from PIL import Image
from PIL import ImageGrab
from enum import Enum
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from my_go import my_go_Thread

class state(Enum):
    battle_begin = 1
    battle_ing = 2
    battle_end = 3

window_width = 1152
window_height = 679
single_battle = [800, 450, 908, 496]
start_battle = [861, 540, 1011, 588]
end_battle = [[11, 300, 410, 666], [700, 300, 1125, 504]]
close_window = [1109, 8, 1140, 26]
menu_area = [35, 6, 993, 29]


class Ui_go(QObject):

    append_log_signal = pyqtSignal(str)

    def setupUi(self, go):
        go.setObjectName("go")
        go.resize(480, 640)

        self.driver_hwnd = 0
        self.driver_window = []
        self.passenger_hwnd = 0
        self.passenger_window = []
        self.int_loop_time = 0

        self.driver_handle = QtWidgets.QPushButton(go)
        self.driver_handle.setGeometry(QtCore.QRect(240, 70, 75, 23))
        self.driver_handle.setObjectName("driver_handle")
        self.passenger_handle = QtWidgets.QPushButton(go)
        self.passenger_handle.setGeometry(QtCore.QRect(240, 120, 75, 23))
        self.passenger_handle.setObjectName("passenger_handle")
        self.driver_info = QtWidgets.QLabel(go)
        self.driver_info.setGeometry(QtCore.QRect(50, 70, 141, 31))
        self.driver_info.setObjectName("driver_info")
        self.passenger_info = QtWidgets.QLabel(go)
        self.passenger_info.setGeometry(QtCore.QRect(50, 120, 141, 31))
        self.passenger_info.setObjectName("passenger_info")
        self.loop_time = QtWidgets.QPushButton(go)
        self.loop_time.setGeometry(QtCore.QRect(240, 170, 75, 23))
        self.loop_time.setObjectName("loop_time")
        self.loop_time_input = QtWidgets.QLineEdit(go)
        self.loop_time_input.setGeometry(QtCore.QRect(50, 170, 113, 20))
        self.loop_time_input.setObjectName("loop_time_input")
        self.messagebox = QtWidgets.QPlainTextEdit(go)
        self.messagebox.setGeometry(QtCore.QRect(40, 300, 391, 321))
        self.messagebox.setObjectName("messagebox")

        self.driver_handle.clicked.connect(self.driver_click)
        self.passenger_handle.clicked.connect(self.passenger_click)
        self.loop_time.clicked.connect(self.loop_time_click)

        self.retranslateUi(go)
        QtCore.QMetaObject.connectSlotsByName(go)

    def driver_click(self):
        self.driver_hwnd, self.driver_window = self.get_window_info()
        self.driver_info.setText("%s %s %s %s" % (self.driver_window[0], self.driver_window[1], self.driver_window[2], self.driver_window[3]))

    def passenger_click(self):
        self.passenger_hwnd, self.passenger_window = self.get_window_info()
        self.passenger_info.setText("%s %s %s %s" % (self.passenger_window[0], self.passenger_window[1], self.passenger_window[2], self.passenger_window[3]))

    def loop_time_click(self):
        self.int_loop_time = int(self.loop_time_input.text())
        self.my_go_thread = my_go_Thread(self.driver_hwnd, self.driver_window, self.passenger_hwnd, self.passenger_window, self.int_loop_time)
        self.my_go_thread.signal_text.connect(self.append_text)
        self.my_go_thread.start()

    def append_text(self, text):
        self.messagebox.appendPlainText(text)

    def get_window_info(self):
        wdname = u'阴阳师-网易游戏'
        handle = win32gui.FindWindow(0, wdname)
        # print(handle)
        if handle == 0:
            return None
        else:
            return handle, win32gui.GetWindowRect(handle)

    def retranslateUi(self, go):
        _translate = QtCore.QCoreApplication.translate
        go.setWindowTitle(_translate("go", "Dialog"))
        self.driver_handle.setText(_translate("go", "driver"))
        self.passenger_handle.setText(_translate("go", "passenger"))
        self.driver_info.setText(_translate("go", "none"))
        self.passenger_info.setText(_translate("go", "none"))
        self.loop_time.setText(_translate("go", "次数"))


def main():
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    ui = Ui_go()
    ui.setupUi(dialog)
    dialog.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
