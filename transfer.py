import pyautogui

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
        elif utt in i:
            print('い')
            pyautogui.hotkey('i')
        elif utt in u:
            print('う')
            pyautogui.hotkey('u')
        elif utt in e:
            print('え')
            pyautogui.hotkey('e')
        elif utt in o:
            print('お')
            pyautogui.hotkey('o')
        elif utt in n:
            print('ん')
            pyautogui.hotkey('n')
        else:
            #一つ前の音にする
            transferUtterance(butt)
            utt = butt
        butt = utt

if __name__ == "__main__":
    transferUtterance('あいうえおーかきくけこん')

