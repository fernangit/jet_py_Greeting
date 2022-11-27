# -*- coding: utf-8 -*-
import os, sys, errno
import signal
from datetime import datetime
import time
import random

import cv2 as cv
from PIL import Image
import numpy as np

import jtalk
import utterance
import posedetect
import cv2pil
import facenet

def greeting():
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
        if not hasFrame:
            cv.waitKey()
            break

        #OpenPose呼び出し
        points = posedetect.getpoints('gpu', hasFrame, frame)

        #Pointを検出したら挨拶
        print('points=', points)
        #有効Point取り出し
        v_points= [p for p in points if p != None]
        print('v_points=', v_points)
        print('len=', len(v_points))
        #有効ポイント10以上かつ前回から5秒以上経過していたら挨拶
        if ((len(v_points) > 10) and ((time.time() - t_st) > 5)):
            #OpenCV→Pill変換
            pill = cv2pil.cv2pil(frame)
            print("detect face")
            #顔検出
            face = facenet.detect_face(pill, 'out.jpg')
            print(face)
            #顔が見つかれば認証
            detectname = ''
            if (face != None):
                #similarity
        #        detectname = facenet.compare_similarity(Image.open('out.jpg'), 'facedb2') 
                detectname = facenet.compare_similarity(pill, 'facedb') 
                print('you are ', detectname)
            #認証した？
            if(detectname != ''):
                #認証挨拶モーション再生
                print('play motion')
            else:
                #通常挨拶モーション再生
                print('play motion')

            #現在時刻読み取り
            d = datetime.now()
            t_st = time.time()
            rnd = random.randint(0, 40)
            print(rnd)
            if (d.hour > 5) and (d.hour < 12):
                #午前
                if rnd > (len(utterance.mng_lst) - 1):
                    jtalk.jtalk(utterance.morning + '　' + detectname)
                else:
                    jtalk.jtalk(utterance.mng_lst[rnd] + '　' + detectname)
            else:
                #午後
                if rnd > (len(utterance.evg_lst) - 1):
                    jtalk.jtalk(utterance.evening + '　' + detectname)
                else:
                    jtalk.jtalk(utterance.evg_lst[rnd] + '　' + detectname)

                time.sleep(3)
                #アイドル動画再起動

                #独り言
                if d.hour == nxt_h and d.minute == nxt_m:
                    #モーション再生
                    print('play motion')
                    #独り言再生
                    jtalk.jtalk(utterance.mono_lst[random.randint(0, len(utterance.mono_lst) - 1)])
                    time.sleep(3)

                    nxt_h = d.hour + 1
                    nxt_m = random.randint(0, 59)
                    print(nxt_h, nxt_m)

if __name__ == '__main__':
    greeting()