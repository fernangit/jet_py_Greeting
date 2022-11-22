# -*- coding: utf-8 -*-
import os, sys, errno
import signal
import cv2 as cv

from datetime import datetime
import time
import random
import numpy as np

import jtalk
import utterance
import posedetect

#カメラの設定　デバイスIDは0
cap = cv.VideoCapture(0)

#WebGL起動　※サーバ起動済みであること
#アイドルモーション起動
time.sleep(3)

jtalk.jtalk('えむず　あいさつユニット　しどうっ')
d = datetime.now()
nxt_h = d.hour
nxt_m = random.randint(0, 59)

t_st = 0
while cv.waitKey(1) < 0:
    #画面キャプチャ
    hasFrame, frame = cap.read()
    frameCopy = np.copy(frame)
    if not hasFrame:
        cv.waitKey()
        break

    #OpenPose呼び出し
    points = posedetect.getpoints('gpu', hasFrame, frame)

    #Pointを検出したら挨拶
    print('points=', points)
    if len(points) > 0:
        #前回から5秒以上経過していたら挨拶
        if (time.time() - t_st) > 5:
            #挨拶モーション再生
            d = datetime.now()
            rnd = random.randint(0, 40)
            print(rnd)
            if (d.hour > 5) and (d.hour < 12):
                if rnd > (len(utterance.mng_lst) - 1):
                    jtalk.jtalk(utterance.morning)
                else:
                    jtalk.jtalk(utterance.mng_lst[rnd])
            else:
                if rnd > (len(utterance.evg_lst) - 1):
                    jtalk.jtalk(utterance.evening)
                else:
                    jtalk.jtalk(utterance.evg_lst[rnd])
            time.sleep(3)
            #アイドル動画再起動

            t_st = time.time()

            # 現在時刻読み込み
            d = datetime.now()
            #独り言
            if d.hour == nxt_h and d.minute == nxt_m:
                #モーション再生
                #独り言再生
                jtalk.jtalk(utterance.mono_lst[random.randint(0, len(utterance.mono_lst) - 1)])
                time.sleep(3)

                nxt_h = d.hour + 1
                nxt_m = random.randint(0, 59)
                print(nxt_h, nxt_m)