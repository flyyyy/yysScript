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
end_battle = [[50, 137, 200, 475], [1000, 122, 1107, 486]]
close_window = [1109, 8, 1140, 26]
menu_area = [440, 9, 993, 24]
cancel_xuanshang = [693, 132, 716, 155]
quit_game = [889, 589, 960, 606]

def check_bound(nx, ny, All_window, window):
    nx = max(nx, All_window[0] + window[0])
    ny = max(ny, All_window[1] + window[1])
    nx = min(nx, All_window[0] + window[2])
    ny = min(ny, All_window[1] + window[3])
    return nx, ny

def move_click(window, All_window, click_time, time_l, time_r, hwnd):
        dx = random.randint(0, window[2] - window[0])
        dy = random.randint(0, window[3] - window[1])
        x = All_window[0] + window[0] + dx
        y = All_window[1] + window[1] + dy
        for i in range(click_time):
            dx = random.randint(-5, 5)
            dy = random.randint(-5, 5)
            nx = x + dx
            ny = y + dy
            nx, ny = check_bound(nx, ny, All_window, window)
            #win32api.SetCursorPos((nx, ny))
            #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, nx, ny, 0, 0)
            #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, nx, ny, 0, 0)
            tmp = win32api.MAKELONG(826, 5) 
            print(nx-All_window[0]-8, ny-All_window[1]-2)
            win32gui.SendMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0) 
            win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, tmp) 
            time.sleep(random.uniform(0.2, 0.2))
            win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, tmp)
            time.sleep(random.uniform(time_l, time_r))
        return 0

def get_window_info():
    wdname = u'阴阳师-网易游戏'
    handle = win32gui.FindWindow(0, wdname)
    #print(handle)
    if handle == 0:
        return None
    else:
        return handle, win32gui.GetWindowRect(handle)


driver_hwnd, driver_window = get_window_info()
print(driver_hwnd, driver_window)

#move_click(start_battle, driver_window, 2, 0.15, 0.2, driver_hwnd)
#move_click(menu_area, driver_window, 2, 0, 0.1, driver_hwnd)
#move_click(close_window, driver_window, 1, 0.4, 0.5, driver_hwnd)
#move_click(menu_area, driver_window, 1, 0, 0.1, driver_hwnd)


def check(img_now, img_compare):
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
    print(len(good), len(des2))
    if 5 * len(good) >= 2 * len(des2):
        return True
    return False

img_now = Image.open('test3.jpg')
print(check(img_now, 'battle_begin.jpg'))