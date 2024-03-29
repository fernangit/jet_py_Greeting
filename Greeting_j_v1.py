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
import threading

import pose_detect
import cv2pil
import facenet
import facecv
import torch
from torchvision.transforms import functional as F
import motion
import talk
import regist_detected
import send_receive_server
import image_filter
import gc

#時刻初期化
def initialize_time():
    #現在時刻読み取り
    d = datetime.now()
    nxt_h = d.hour
    nxt_m = random.randint(0, 59)
    t_st = time.time()
    
    return nxt_h, nxt_m, t_st

#デバイス初期設定
def initialize_devices(device_id, mode):
    #カメラの設定　デバイスIDは0
    cap = cv.VideoCapture(device_id)
    if mode == 0:
        #OpenPose用デバイス設定
        pose_detect.set_openpose_device('gpu', net)

    return cap

#画像サイズ変換
def scale_to_resolation(img, resolation):
    h, w = img.shape[:2]
    scale = (resolation / (w * h)) **0.5
    
    return cv.resize(img, dsize = None, fx = scale, fy = scale)

#フレーム補正
def correct_frame(frame):
    #画像サイズ変換
    frame = scale_to_resolation(frame, 320 * 240)

    #画像シャープ化
#    frame = image_filter.apply_sharp_filter(frame)
    
    return frame

#フレーム除外
def exclude_frame(frame):
    #score 100未満をピンボケ画像として除外
    score = image_filter.get_image_score(frame)
    if score < 100:
        return False

    '''
    #顔が検出できなければ除外
    faces = image_filter.detect_faces_dlib(frame)
    if len(faces) < 1:
        return False

    #顔が検出できなければ除外
    faces = image_filter.detect_faces(frame)
    if len(faces) < 1:
        return False

    #目が2つ検出できなければ除外
    eyes = image_filter.detect_eyes(frame)
    if len(eyes) < 2:
        return False

    #画像サイズが所定のサイズより小なら除外（カメラからの距離を推定）
    height, width = frame.shape[:2]
#    print("height:", height)
#    print("width:", width)
    '''
    return True

#起動セリフ＆モーション
def opening():
    #起動セリフ
    talk.opening()

    #起動モーション
    motion.set_first_motion()

#定期的セリフ＆モーション
def regulary(d, nxt_h, nxt_m, t_st):
    #30分でスリープ
    if (time.time() - t_st) > (60 * 30):
        #Sleepモーション
        motion.set_sleep_motion()
        t_st = time.time()

    #所定時刻の所定モーション呼び出し
    motion.set_default_motion(d)

    #独り言
    nxt_h, nxt_m = talk.monologue(d, nxt_h, nxt_m)

    return nxt_h, nxt_m, t_st

#骨格検出
def detect_point(hasFrame, frame, org_frame, greeting):
    cropped_face = False
    cropped_frame = org_frame
    
    #OpenPose呼び出し
    points = pose_detect.getpoints(hasFrame, frame)

    #有効Point取り出し
    v_points= [p for p in points if p != None]
#    print('v_points=', v_points)
#    print('len=', len(v_points))

    #有効ポイント10以上
    if (len(v_points) > 10):
        #挨拶する
        greeting = True
        #0：頭、1：首を取得できているか
        if points[0] != None and points[1] != None:
            print("detect face")
            cropped_face = True
            #0：頭、1：首を設定
            f_point = []
            f_point.append(points[0])
            f_point.append(points[1])
            #顔周辺の画像を切り出す             
            cropped_frame = pose_detect.crop_frame(f_point, org_frame)

    return greeting, cropped_face, cropped_frame

#顔検出
def detect_face(frame):
    #for debug
    cv.imshow('Input', frame)
    cv.moveWindow('window name', 100, 100)

    #ポーズ省略の場合
    cropped_frame = frame
    cropped_face = True
    
    return cropped_frame, cropped_face
    
#顔認証
def authenticate_face(cropped_frame, greeting):
    max_sim = 0
    detect_name = ''

    #フレーム除外
    if exclude_frame(cropped_frame) == False:
        return greeting, max_sim, detect_name
    
    #OpenCV→Pill変換
    pill = cv2pil.cv2pil(cropped_frame)

    #顔検出
#    face = facenet.detect_face(pill, path='out.jpg')
    face = facenet.detect_face(pill)
#    faces, face_frame = facecv.detect_face(cropped_frame) #for facecv

    #顔が見つかれば認証
    if (face != None):
#    if (len(faces) != 0): #for facecv
#        face = cv2pil.cv2pil(face_frame) #for facecv
        #正面顔チェック
        front_face = facenet.frontal_face(pill)
#        front_face = facecv.frontal_face(face_frame) #for facecv
        
        if (front_face != False):
            #挨拶する
            greeting = True
            #similarity
#            max_sim, detect_name, fv = facenet.compare_similarity(face, 'facedb') 
            max_sim, detect_name, fv = facenet.compare_similarity(face, 'facedb2') 
#            face = F.to_tensor(np.float32(face)) #for facecv
#            max_sim, detect_name, fv = facenet.compare_similarity(face, 'facedb2') #for facecv

    if(detect_name != ''):
        # 登録
        regist_detected.regist_detected(detect_name)
        #類似度80%以上で今回データで差し替え
        if max_sim > 0.8:
#            vector = 'facedb' + '/' + detect_name
            vector = 'facedb2' + '/' + detect_name
            np.save(vector, fv.astype('float32'))

        #名前の抽出
        detect_name = detect_name.split('_')[0]
        #さん付け
        detect_name = detect_name + 'さん！'
        print('you are ', detect_name)

    return greeting, max_sim, detect_name

#挨拶
def greet(d, url, max_sim, detect_name):
    #認識度レベル変換
    level = talk.percentage_to_level(max_sim, 0.7, motion.get_motion_num())
    if level > talk.len_utterance_op_lst() - 1:
        level = talk.len_utterance_op_lst() - 1

    #挨拶音声再生
    utter = talk.greeting(d, detect_name, talk.level_to_utterance(level))

    #モーションズレ補正
    time.sleep(0.5)

    #挨拶モーション再生
    motion.set_level_motion(level)
    
    #発話内容をサーバーに送信
    send_receive_server.send_utterance(url, utter, str(max_sim), '', '')

    #発話内容をリセット
    threading.Thread(target=reset_utterance).start()

def greeting_main(url, mode = 0):
    #サーバ起動済み＆WebGL起動済みであること

    #時刻初期化
    nxt_h, nxt_m, t_st = initialize_time()

    #デバイス初期設定
    cap = initialize_devices(0, mode)
    
    #起動セリフ＆モーション
    opening()
    
    while True:
#        #苦し紛れのメモリ解放
#        torch.cuda.empty_cache()
#        gc.collect()

        cv.waitKey(1)
        greeting = False

        #現在時刻読み取り
        d = datetime.now()

        #定期的セリフ＆モーション
        nxt_h, nxt_m, t_st = regulary(d, nxt_h, nxt_m, t_st)

        #読み上げ
#        talk.read_sentence()

        #画面キャプチャ
        hasFrame, frame = cap.read()
        if not hasFrame:
            continue

        #入力フレーム補正
        frame = correct_frame(frame)

        #前回から7秒以上経過？
        if (time.time() - t_st) > 7:
            #元画像を保存
            org_frame = copy.copy(frame)

            if (mode == 0):
                #骨格検出
                greeting, cropped_face, cropped_frame = detect_point(hasFrame, frame, org_frame, greeting)

            elif (mode == 1):
                #顔検出
                cropped_frame, cropped_face = detect_face(org_frame)

            if cropped_face == True:
                #顔認証
                greeting, max_sim, detect_name = authenticate_face(cropped_frame, greeting)

            #挨拶する
            if greeting == True:
                greet(d, url, max_sim, detect_name)

                t_st = time.time()

#発話内容をリセット
def reset_utterance():
    time.sleep(7)
    send_receive_server.send_utterance(url, '', '0', '', '')

if __name__ == '__main__':
    #args[1] = server url ex.localhost:8000
    #args[2] = mode 0:通常/1:ポーズ省略
    args = sys.argv
    if 2 <= len(args):
        print(args[1])
        print(args[2])
        url = 'http://' + args[1] + '/StreamingAssets/Utterance'
        print(url)
        greeting_main(url, int(args[2]))
    else:
        print('Arguments are too short')

