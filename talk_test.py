import transfer
import jtalk
import time
import random
import utterance
import pyautogui

motionlist = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'y', 'z']

#ブラウザ起動しておく

jtalk.jtalk('おはようございます')
transfer.transferUtterance('おはようございます')
time.sleep(3)

jtalk.jtalk('こんにちわ')
transfer.transferUtterance('こんにちわ')
time.sleep(3)

jtalk.jtalk('こんばんわ')
transfer.transferUtterance('こんばんわ')
time.sleep(3)

jtalk.jtalk('おつかれさまです')
transfer.transferUtterance('おつかれさまです')
time.sleep(3)

jtalk.jtalk('めめたあ')
transfer.transferUtterance('めめたあ')
time.sleep(3)

jtalk.jtalk('ひでぶっっ')
transfer.transferUtterance('ひでぶっっ')
time.sleep(3)

while(True):
    #独り言再生
    monologue = random.randint(0, len(utterance.mono_lst) - 1)
    jtalk.jtalk(utterance.mono_lst[monologue])
    print(monologue, utterance.mono_lst[monologue])
    #モーションズレ補正
    time.sleep(0.5)
    if monologue < len(motionlist) :
        #モーション
        pyautogui.hotkey(motionlist[monologue])
    else:
        #口パク
        transfer.transferUtterance(utterance.mono_lst[monologue])

    time.sleep(3)
