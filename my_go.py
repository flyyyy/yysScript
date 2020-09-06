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
import psutil
from matplotlib import pyplot as plt

class state(Enum):
    battle_begin = 1
    battle_ing = 2
    battle_end = 3

window_width = 1152
window_height = 679
single_battle = [800, 450, 908, 496]
start_battle = [1050, 566, 1128, 655]
end_battle1 = [[50, 137, 200, 475], [1000, 122, 1107, 486]]
end_battle2 = [[50, 137, 200, 475], [1000, 122, 1107, 309]]
close_window = [1109, 8, 1140, 26]
menu_area = [440, 9, 993, 24]
cancel_xuanshang = [693, 132, 716, 155]
quit_game = [889, 589, 960, 606]

class my_go_Thread(QtCore.QThread):

    signal_text = pyqtSignal(str)

    def __init__(self, driver_hwnd, driver_window, passenger_hwnd, passenger_window, int_loop_time, parent=None):
        super(my_go_Thread, self).__init__(parent)
        
        self.driver_hwnd = driver_hwnd
        self.driver_window = driver_window
        self.passenger_hwnd = passenger_hwnd
        self.passenger_window = passenger_window
        self.int_loop_time = int_loop_time
        self.role = 0
        self.ready1 = 0
        self.ready2 = 0
        self.endbattle = 0

    def check_bound(self, nx, ny, All_window, window):
        nx = max(nx, All_window[0] + window[0])
        ny = max(ny, All_window[1] + window[1])
        nx = min(nx, All_window[0] + window[2])
        ny = min(ny, All_window[1] + window[3])
        return nx, ny

    def move_click_old(self, window, All_window, click_time, time_l, time_r):
        dx = random.randint(0, window[2] - window[0])
        dy = random.randint(0, window[3] - window[1])
        x = All_window[0] + window[0] + dx
        y = All_window[1] + window[1] + dy
        for i in range(click_time):
            dx = random.randint(-5, 5)
            dy = random.randint(-5, 5)
            nx = x + dx
            ny = y + dy
            nx, ny = self.check_bound(nx, ny, All_window, window)
            win32api.SetCursorPos((nx, ny))
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, nx, ny, 0, 0)
            time.sleep(random.uniform(0.1, 0.15))
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, nx, ny, 0, 0)
            time.sleep(random.uniform(time_l, time_r))
        return 0

    def move_click(self, window, All_window, click_time, time_l, time_r, hwnd):
        dx = random.randint(0, window[2] - window[0])
        dy = random.randint(0, window[3] - window[1])
        x = All_window[0] + window[0] + dx
        y = All_window[1] + window[1] + dy
        for i in range(click_time):
            dx = random.randint(-5, 5)
            dy = random.randint(-5, 5)
            nx = x + dx
            ny = y + dy
            nx, ny = self.check_bound(nx, ny, All_window, window)
            #win32api.SetCursorPos((nx, ny))
            #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, nx, ny, 0, 0)
            #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, nx, ny, 0, 0)
            client_pos = win32gui.ScreenToClient(hwnd, (nx, ny)) 
            tmp = win32api.MAKELONG(client_pos[0], client_pos[1]) 
            win32gui.SendMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0) 
            win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, tmp) 
            time.sleep(random.uniform(0.1, 0.15))
            win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, tmp)
            time.sleep(random.uniform(time_l, time_r))
        return 0

    def check(self, img_now, img_compare):
        img_end = Image.open(img_compare)
        img_now = cv.cvtColor(np.asarray(img_now), cv.COLOR_RGB2BGR)
        img_end = cv.cvtColor(np.asarray(img_end), cv.COLOR_RGB2BGR)

        sift = cv.xfeatures2d.SIFT_create()  # 创建sift检测器
        kp1, des1 = sift.detectAndCompute(img_now, None)
        kp2, des2 = sift.detectAndCompute(img_end, None)

        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        flann = cv.FlannBasedMatcher(index_params, search_params)
        mathces = flann.knnMatch(des1, des2, k=2)
        good = []
        # 过滤不合格的匹配结果，大于0.7的都舍弃
        for m, n in mathces:
            if m.distance < 0.7 * n.distance:
                good.append(m)
        if 5 * len(good) >= 2 * len(des2):
            return True
        return False

    def switch(self, window):
        #if window == 0:
        #    self.move_click(menu_area, self.driver_window, 1, 0, 0.1, self.driver_hwnd)
        #else:
        #    self.move_click(menu_area, self.passenger_window, 1, 0, 0.1, self.passenger_hwnd)
        #self.log.emit("switch to %s\n" % window)
        self.role = window
        self.signal_text.emit("%s switch to %s\n" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ,window))

    def run(self):
        cnt = 0
        game_state = state.battle_begin
        self.switch(0)
        self.ready1 = 1
        self.ready2 = 1
        time_start = time.time()
        while (1):
            time_now = time.time()
            if time_now - time_start >= 600:
                break
            if self.role == 0:
                img_now = ImageGrab.grab((self.driver_window[0], self.driver_window[1], self.driver_window[2], self.driver_window[3]))
                if self.check(img_now, "xuanshang_icon.jpg"):
                    time_start = time.time()
                    self.move_click(cancel_xuanshang, self.driver_window, 1, 0, 0, self.driver_hwnd)
                    self.signal_text.emit("%s driver cancel one xuanshang\n" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                elif self.check(img_now, "passenger_begin.jpg"):
                    time_start = time.time()
                    self.ready1 = 1
                    if self.ready1 and self.ready2:
                        self.ready1 = 0
                        self.ready2 = 0
                        self.move_click(start_battle, self.driver_window, 3, 0.3, 0.3, self.driver_hwnd)
                        cnt += 1
                        self.signal_text.emit("%s %d driver_begin\n" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), cnt))
                    elif self.ready1 and self.ready2 == 0:
                        self.signal_text.emit("%s %d driver_ready\n" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), cnt))
                        self.switch(1)
                elif self.check(img_now, "battle_end_1.jpg"):
                    time_start = time.time()
                    click_time = random.randint(2, 3)
                    self.move_click(end_battle1[random.randint(0, 1)], self.driver_window, click_time, 0.15, 0.2, self.driver_hwnd)

                    click_time = random.randint(2, 3)
                    self.move_click(end_battle2[random.randint(0, 1)], self.passenger_window, click_time, 0.15, 0.2, self.passenger_hwnd)

                    self.signal_text.emit("%s %d driver_end1\n" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), cnt))
                elif self.check(img_now, "battle_end_2.jpg"):
                    time_start = time.time()
                    click_time = random.randint(2, 3)
                    self.move_click(end_battle1[random.randint(0, 1)], self.driver_window, click_time, 0.15, 0.2, self.driver_hwnd)

                    click_time = random.randint(2, 3)
                    self.move_click(end_battle2[random.randint(0, 1)], self.passenger_window, click_time, 0.15, 0.2, self.passenger_hwnd)
                    
                    self.signal_text.emit("%s %d driver_end2\n" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), cnt))
                    if cnt >= self.int_loop_time:
                        break
            else:
                img_now = ImageGrab.grab((self.passenger_window[0], self.passenger_window[1], self.passenger_window[2], self.passenger_window[3]))
                if self.check(img_now, "xuanshang_icon.jpg"):
                    time_start = time.time()
                    self.move_click(cancel_xuanshang, self.passenger_window, 1, 0, 0, self.passenger_hwnd)
                    self.signal_text.emit("%s passenger cancel one xuanshang\n" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                elif self.check(img_now, "passenger_begin.jpg"):
                    time_start = time.time()
                    self.ready2 = 1
                    self.signal_text.emit("%s %d passenger_ready\n" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), cnt))
                    self.switch(0)
                elif self.check(img_now, "battle_end_1.jpg"):
                    time_start = time.time()
                    click_time = random.randint(2, 3)
                    self.move_click(end_battle2[random.randint(0, 1)], self.passenger_window, click_time, 0.15, 0.2, self.passenger_hwnd)
                    self.signal_text.emit("%s %d passenger_end1\n" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), cnt))
                elif self.check(img_now, "battle_end_2.jpg"):
                    time_start = time.time()
                    click_time = random.randint(2, 3)
                    self.move_click(end_battle2[random.randint(0, 1)], self.passenger_window, click_time, 0.15, 0.2, self.passenger_hwnd)
                    self.signal_text.emit("%s %d passenger_end2\n" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), cnt))
            time.sleep(0.1)
        self.my_close()

    def my_close(self):
        all_window = [0, 0, 0, 0]

        self.move_click_old(close_window, self.driver_window, 1, 0.4, 0.5)
        self.move_click_old(quit_game, all_window, 3, 0.2, 0.3)
        self.switch(1)
        self.move_click_old(close_window, self.passenger_window, 1, 0.4, 0.5)
        self.move_click_old(quit_game, all_window, 3, 0.2, 0.3)
        self.signal_text.emit("close\n")
