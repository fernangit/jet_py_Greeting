import random
import pyautogui

motion_list = ['c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', '4']
dance_list = ['2', '3', '5', '6', '7', '8', '9']

#起動時モーション
def set_first_motion():
    pyautogui.hotkey('b')

#Sleepモーション
def set_sleep_motion():
    pyautogui.hotkey('y')

#所定時刻の所定モーション呼び出し
def set_default_motion(now_time):
    if now_time.hour == 8 and now_time.minute == 30:
        #8:30 ラジオ体操
        pyautogui.hotkey('1')
    if now_time.hour == 12 and now_time.minute == 0:
        #12:00 ダンスの時間
        motion = random.randint(0, len(dance_list) - 1)
        pyautogui.hotkey(dance_list[motion])

#レベル対応モーション呼び出し
def set_level_motion(level):
    print('level:', level)
    if level > len(motion_list) - 1:
        level = len(motion_list) - 1
    pyautogui.hotkey(motion_list[level])

#モーション数
def get_motion_num():
    return len(motion_list)

