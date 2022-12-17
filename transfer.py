import pyautogui
import time
import math

a = 'あかさたなはまやらわがざだばぱぁゃアカサタナハマヤラワガザダバパァャｱｶｻﾀﾅﾊﾏﾔﾗﾜｶﾞｻﾞﾀﾞﾊﾞﾊﾟｧｬ'
i = 'いきしちにひみりぎじぢびぴぃイキシチニヒミリギジヂビピィｲｷｼﾁﾆﾋﾐﾘｷﾞｼﾞﾁﾞﾋﾞﾋﾟｨ'
u = 'うくすつぬふむゆるぐずづぷぶぅゅっウクスツヌフムユルグズヅブプゥュッｳｸｽﾂﾇﾌﾑﾕﾙｸﾞｽﾞﾂﾞﾌﾞﾌﾟｩｭｯ'
e = 'えけせてねへめれげぜでべぺぇエケセテネヘメレゲゼデベペェｴｹｾﾃﾈﾍﾒﾚｹﾞｾﾞﾃﾞﾍﾞﾍﾟｪ'
o = 'おこそとのほもよろごぞどぽぼぉょオコソトノホモヨロゴゾドボポォョｵｺｿﾄﾉﾎﾓﾖﾛｺﾞｿﾞﾄﾞﾎﾞﾎﾟｫｮ'
n = 'んン'

def transfer_utterance(utterance):
    list(utterance)
    butt = ''
    for num in range(len(utterance)):
        utt = utterance[num]
        if utt in a:
            print('あ')
            pyautogui.hotkey('a')
            time.sleep(0.1)
        elif utt in i:
            print('い')
            pyautogui.hotkey('i')
            time.sleep(0.1)
        elif utt in u:
            print('う')
            pyautogui.hotkey('u')
            time.sleep(0.1)
        elif utt in e:
            print('え')
            pyautogui.hotkey('e')
            time.sleep(0.1)
        elif utt in o:
            print('お')
            pyautogui.hotkey('o')
            time.sleep(0.1)
        elif utt in n:
            print('ん')
            pyautogui.hotkey('n')
            time.sleep(0.1)
        else:
            #一つ前の音にする
            transfer_utterance(butt)
            utt = butt
            time.sleep(0.1)
        butt = utt

def transfer_percentage(per, thresh, motion_num):
    #小数点以下は切り捨て
    base = math.floor((per - thresh) * 100)
    print('level base:', base)
    if base <= 0:
        #0以下(類似度がthreshより小)
        level = 0
    elif base <= 10:
        #10以下(71%〜80％)
        level = 1
    else:
        #10より大(81%〜100%)
        level = base - 10
        #高レベルの補正
        if level > motion_num - 1:
            level = motion_num - 1

    return level

if __name__ == "__main__":
    transfer_utterance('あいうえおーかきくけこん')

