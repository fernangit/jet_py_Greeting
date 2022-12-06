import pyautogui
import time

a = 'あかさたなはまやらわがざだばぁゃアカサタナハマヤラワガザダバァャ'
i = 'いきしちにひみりぎじぢびぃイキシチニヒミリギジヂビィ'
u = 'うくすつぬふむゆるぐずづぶぅゅっウクスツヌフムユルグズヅブゥュッ'
e = 'えけせてねへめれげぜでべぇエケセテネヘメレゲゼデベェ'
o = 'おこそとのほもよろごぞどぼぉょオコソトノホモヨロゴゾドボォョ'
n = 'んン'

def transferUtterance(utterance):
    list(utterance)
    butt = ''
    for num in range(len(utterance)):
        utt = utterance[num]
        if utt in a:
            print('あ')
            pyautogui.hotkey('a')
            time.sleep(0.2)
        elif utt in i:
            print('い')
            pyautogui.hotkey('i')
            time.sleep(0.2)
        elif utt in u:
            print('う')
            pyautogui.hotkey('u')
            time.sleep(0.2)
        elif utt in e:
            print('え')
            pyautogui.hotkey('e')
            time.sleep(0.2)
        elif utt in o:
            print('お')
            pyautogui.hotkey('o')
            time.sleep(0.2)
        elif utt in n:
            print('ん')
            pyautogui.hotkey('n')
            time.sleep(0.2)
        else:
            #一つ前の音にする
            transferUtterance(butt)
            utt = butt
            time.sleep(0.2)
        butt = utt

if __name__ == "__main__":
    transferUtterance('あいうえおーかきくけこん')

