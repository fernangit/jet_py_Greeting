import os
import time
import random
import pyautogui
import play

motion_list = ['c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', '4']
#注：dance_listとsound_listの配列番号は対応させること
dance_list = ['2', '3', '5', '6', '7', '8', '9']
sound_list = ['',
              './source/いーあるふぁんくらぶ.wav',
              '',
              './source/アカリがやってきたぞっ.wav',
              '',
              '',
              '']

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
        if os.path.isfile(sound_list[1]) == True:
            #BGM再生
            play.play_sound(sound_list[1])
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
    if os.path.isfile(sound_list[1]) == True:
        play.play_sound(sound_list[1])
        #モーションズレ補正
        time.sleep(0.5)
    pyautogui.hotkey(dance_list[1])

