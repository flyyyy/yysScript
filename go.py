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

class state(Enum):
    battle_begin = 1
    battle_ing = 2
    battle_end = 3

window_width = 1152
window_height = 679
single_battle = [800, 450, 908, 496]
start_battle = [861, 540, 1011, 588]
end_battle = [[11, 300, 410, 666], [700, 300, 1125, 504]]

def move_click(window, All_window, click_time):
    dx = random.randint(0, window[2] - window[0])
    dy = random.randint(0, window[3] - window[1])
    x = All_window[0] + window[0] + dx
    y = All_window[1] + window[1] + dy
    for i in range(click_time):
        dx = random.randint(-5, 5)
        dy = random.randint(-5, 5)
        nx = x + dx
        ny = y + dy
        win32api.SetCursorPos((nx, ny))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, nx, ny, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, nx, ny, 0, 0)
    return 0

def get_window_info():
    wdname = u'阴阳师-网易游戏'
    handle = win32gui.FindWindow(0, wdname)
    print(handle)
    if handle == 0:
        return None
    else:
        return win32gui.GetWindowRect(handle)

def check(img_now):
    img_end = Image.open("battle_end.jpg")
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
    if len(good) >= 200:
        return True
    return False

if __name__ == '__main__':

    gua_pi = get_window_info()

    game_state = state.battle_begin
    while(1):
        print(game_state)
        if game_state == state.battle_begin:
            move_click(single_battle, gua_pi, 1)
            game_state = state.battle_ing
        elif game_state == state.battle_end:
            click_time = random.randint(1, 3)
            move_click(end_battle[random.randint(0, 1)], gua_pi, click_time)
            time.sleep(0.08)
            game_state = state.battle_begin

        img_now = ImageGrab.grab((gua_pi[0], gua_pi[1], gua_pi[2], gua_pi[3]))
        if check(img_now):
            game_state = state.battle_end
        time.sleep(1)

