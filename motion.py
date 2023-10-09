# -*- coding: utf-8 -*-
import sys
import os
import time
import random
import pyautogui
import play

motion_list = ['c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', '4']
#注：dance_listとsound_listの配列番号は対応させること
dance_list = ['2', '3', '5', '6', '7', '8', '9']
sound_list = ['./source/sound2.wav',
              './source/sound3.wav',
              './source/sound5.wav',
              './source/sound6.wav',
              './source/sound7.wav',
              './source/sound8.wav',
              './source/sound9.wav']

#起動時モーション
def set_first_motion():
    pyautogui.hotkey('b')

#Sleepモーション
def set_sleep_motion():
    pyautogui.hotkey('y')

#所定時刻の所定モーション呼び出し
def set_default_motion(now_time):
    if now_time.hour == 8 and now_time.minute == 26 and now_time.second == 21:
        #8:26 ラジオ体操
        pyautogui.hotkey('1')
    if now_time.hour == 12 and now_time.minute == 30 and now_time.second == 0:
        #12:30 昼休み
        pyautogui.hotkey('b')
        play.play_sound('昼休み.wav')
    if now_time.hour == 17 and now_time.minute == 00 and now_time.second == 0:
        #17:00 ダンスの時間
        motion = random.randint(0, len(dance_list) - 1)
        if os.path.isfile(sound_list[motion]) == True:
            #BGM再生
            play.play_sound(sound_list[motion])
            #モーションズレ補正
            time.sleep(0.5)
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

if __name__ == '__main__':
    #args[1] = motionNo
    args = sys.argv
    if 1 <= len(args):
        print(args[1])
        time.sleep(1)
        if os.path.isfile(sound_list[int(args[1])]) == True:
            play.play_sound(sound_list[int(args[1])])
            #モーションズレ補正
            time.sleep(0.5)
        pyautogui.hotkey(dance_list[int(args[1])])
    else:
        print('Arguments are too short')

