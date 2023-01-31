# -*- coding: utf-8 -*-
import os, sys, errno
import signal
from datetime import datetime
import time
import random
import copy

import cv2 as cv
from PIL import Image
import numpy as np
import pyautogui

import jtalk
import utterance
import pose_detect
import cv2pil
import facenet
import transfer
import motion
import talk
import regist_detected

def scale_to_resolation(img, resolation):
    h, w = img.shape[:2]
    scale = (resolation / (w * h)) **0.5
    return cv.resize(img, dsize = None, fx = scale, fy = scale)

def greeting(mode = 0):
    #サーバ起動済み＆WebGL起動済みであること

    #カメラの設定　デバイスIDは0
    cap = cv.VideoCapture(0)

    #起動セリフ
    talk.opening()

    #起動モーション
    motion.set_first_motion()

    #OpenPose用デバイス設定
    pose_detect.set_openpose_device('gpu')

    #現在時刻読み取り
    d = datetime.now()
    nxt_h = d.hour
    nxt_m = random.randint(0, 59)
    t_st = time.time()

#    while cv.waitKey(1) < 0:
    while True:
        cv.waitKey(1)
        greeting = False
        cropped_face = False
        #現在時刻読み取り
#        print('現在時刻読み取り')
        d = datetime.now()
        #30分でスリープ
        if (time.time() - t_st) > (60 * 30):
            #Sleepモーション
#            print('sleep motion')
            motion.set_sleep_motion()

        #所定時刻の所定モーション呼び出し
#        print('所定時刻の所定モーション呼び出し')
        motion.set_default_motion(d)

        #独り言
#        print('独り言')
        nxt_h, nxt_m = talk.monologue(d, nxt_h, nxt_m)

        #画面キャプチャ
#        print('画面キャプチャ')
        hasFrame, frame = cap.read()
        if not hasFrame:
            continue

        #サイズ変更
        scale_to_resolation(frame, 320 * 480)

        if (mode != 0):
            #debug
#            cv.namedWindow("Output-Skeleton", cv.WINDOW_NORMAL)
            resized_frame = cv.resize(frame, ((int)(frame.shape[1]), (int)(frame.shape[0])))
            cv.imshow('Input', resized_frame)
            cv.moveWindow('window name', 100, 100)

        #元画像を保存
        org_frame = copy.copy(frame)

        if (mode == 1):
            #ポーズ省略の場合
            cropped_frame = org_frame
            cropped_face = True

        if (mode == 0):
            #OpenPose呼び出し
#            print('OpenPose呼び出し')
            points = pose_detect.getpoints(hasFrame, frame)
#            print('points=', points)
            #有効Point取り出し
            v_points= [p for p in points if p != None]
#            print('v_points=', v_points)
#            print('len=', len(v_points))
            #0：頭、1：首
            #0：頭、1：首を取得しておく
            f_point = []
            f_point.append(points[0])
            f_point.append(points[1])

        #前回から7秒以上経過？
        if (time.time() - t_st) > 7:
            max_sim = 0
            detect_name = ''
            #有効ポイント10以上
            if ((mode == 0) and (len(v_points) > 10)):
#                print('有効ポイント10以上かつ前回から7秒以上経過')
                #挨拶する
                greeting = True
                #0：頭、1：首を取得できているか
                if points[0] != None and points[1] != None:
                    print("detect face")
                    cropped_face = True
                    #顔周辺の画像を切り出す             
                    cropped_frame = pose_detect.crop_frame(f_point, org_frame)

            #有効ポイント10以下
            elif ((mode == 0) and (len(v_points) <= 10)):
                    continue

            if cropped_face == True:
                #OpenCV→Pill変換
                pill = cv2pil.cv2pil(cropped_frame)
                #顔検出
#                print("顔検出")
#                face = facenet.detect_face(pill, path='out.jpg')
                face = facenet.detect_face(pill)
#                print(face)
                #顔が見つかれば認証
                if (face != None):
#                    print("顔が見つかれば認証")
                    #挨拶する
                    greeting = True
                    #similarity
#                    max_sim, detect_name, fv = facenet.compare_similarity(face, 'facedb') 
                    max_sim, detect_name, fv = facenet.compare_similarity(face, 'facedb2') 

                #認証した？
                if(detect_name != ''):
#                    print("認証した")
                    # 登録
                    regist_detected.regist_detected(detect_name)
                    #類似度80%以上で今回データで差し替え
                    if max_sim > 0.8:
#                        vector = 'facedb' + '/' + detect_name
                        vector = 'facedb2' + '/' + detect_name
                        np.save(vector, fv.astype('float32'))
                    #名前の抽出
                    detect_name = detect_name.split('_')[0]
                    #さん付け
                    detect_name = detect_name + 'さん'
                    print('you are ', detect_name)

            #挨拶する
            if greeting == True:
                #認識度レベル変換
                level = transfer.transfer_percentage(max_sim, 0.7, motion.get_motion_num())
                if level > len(utterance.op_lst) - 1:
                    level = len(utterance.op_lst) - 1

                #挨拶音声再生
#                print('挨拶音声再生')
                talk.greeting(d, detect_name, utterance.op_lst[level])

                #モーションズレ補正
                time.sleep(0.5)

                #挨拶モーション再生
#                print('挨拶モーション再生')
                motion.set_level_motion(level)

                t_st = time.time()
#                print('t_st:', t_st)

if __name__ == '__main__':
    #args[1] = mode 0:通常/1:ポーズ省略
    args = sys.argv
    if 1 <= len(args):
        print(args[1])
        greeting(int(args[1]))
    else:
        print('Arguments are too short')

