import sys
import cv2
from PIL import Image, ImageDraw
import numpy as np
import glob

import cv2pil
import facenet
import keyinput

#カメラの設定　デバイスIDは0
cap = cv2.VideoCapture(0)

def save_faceFeature(dbpath, name):
    #初期化
    mode = 0
    skip = True
    keywait = True
    count = 0

    #名前の重複チェック
    check_name(dbpath, name, count)
    print('count:', count)

    print('データ登録開始　Yes:y')
    #ビデオ入力開始
    while(True):
        ret, face = img_crop(cap, keywait)
        key = cv2.waitKey(1)
        #キー入力が取れないので代用
        key = keyinput.keythrough(1)
        print('key:', key)
        #ord：文字を10進数で表記されるアスキーコードへ変換する
        if keywait == True and key == 'y':
            print('顔データ登録開始')
            keywait = False

        #顔データ登録開始
        if keywait == False:
            #顔が見つかなれば継続
            if (face == None):
                continue

            #マスクなしモード設定
            if mode == 0:
                mode = 1
                registnum = 0

            #データ登録
            if mode == 1 or mode == 2:
                regist_faceFeature(face, dbpath, name, skip, mode, count, registnum)

            #データチェック
            if mode == 3:
                check_faceFeature(face, dbpath, name)

            if skip == True or mode == 3:
                print('登録終了しますか？　Yes:y No:n')
                if keyinput.keyin() == 'y':
                    print('登録終了')
                    break
                else:
                    print('再登録')
                    mode = 0
                    skip = True
                    keywait = True

def regist_faceFeature(face, dbpath, name, skip, mode, count, registnum):
    if mode == 1:
        print('マスクなしモードを設定するか Yes:y Skip:s', registnum + 1)
    elif mode == 2:
        print('マスクありモードを設定するか Yes:y Skip:s', registnum + 1)
    else:
        return

    regist_skip(skip, mode)
    print(skip, mode)
    if skip == False:
        #データ登録
        print('データ登録')
        regist_dbx3(face, dbpath, name, skip, mode, count, registnum)

def check_faceFeature(face, dbpath, name):
    #テスト
    print('顔認証テストをするか Yes:y Skip:s')
    regist_skip(skip, mode)
    if skip == False:
        detect = facenet.compare_similarity(face, dbpath)
        if detect == '':
            print('顔認証テスト　NG')
        else:
            print('you are ', detect)

def check_name(dbpath, name, count):
    maxnum = 0
    #dbpathにある同じ名前のファイルを検索
    for file in glob.glob(dbpath + '/' + name + '*.npy'):
        print(file)
        num = int(file.split('_')[1])
        print('num:', num)
        #番号の二桁目以上を取得
        num = num / 10
        #番号の最大値を取得
        if num > maxnum:
            maxnum = num
    print('maxnum:', maxnum)
    if maxnum != 0:
        #カウントアップしてcountを返す
        count = (maxnum + 1) * 10

def img_crop(cap, keywait):
    #初期化
    ret = True
    face = None
    #カメラからの画像取得
    ret, frame = cap.read()
    #画像表示
    cv2.imshow('camera', frame)

    if keywait == False:
        #OpenCV→Pill変換
        pill = cv2pil.cv2pil(frame)
        #顔検出
        face = facenet.detect_face(pill, 'out.jpg')
        print(face)
        #顔が見つかれば認証
        if (face != None):
            print('顔検出OK')
            # 画像ファイルの読み込み(カラー画像(3チャンネル)として読み込まれる)
            img = cv2.imread('out.jpg')
            # 画像の表示
            cv2.imshow('face', img)
            ret = True
        else:
            print('顔検出NG')
            ret = False

    return ret, face

def regist_dbx3(img_cropped, dbpath, name, skip, mode, count, registnum):
    #データ登録
    regist_db(img_cropped, dbpath, name + '_' + str(count))
    print('データ登録')
    count = count + 1
    registnum = registnum + 1
    #3枚登録
    if registnum > 3:
        skip = True
        mode = mode + 1
        registnum = 0

def regist_db(img_cropped, dbpath, name):
    #切り出し画像でデータ作成
    fv = facenet.feature_vector(img_cropped)
    #DB登録
    vector = dbpath + '/' + name
    np.save(vector, fv.astype('float32'))

def regist_skip(skip, mode):
    if skip == True:
        if mode == 1:
            print('マスクなし画像登録')
        elif mode == 2:
            print('マスクあり画像登録')
        else:
            print('顔認証テスト')

        ret = keyinput.keyin()
        if ret == 's':
            #スキップする
            skip = True
            mode = mode + 1
        else:
            #スキップしない
            skip = False

if __name__ == '__main__':
    #args[1] = dbpath
    #args[2] = name
    args = sys.argv
    if 2 <= len(args):
        print(args[1], args[2])
        save_faceFeature(args[1], args[2])
    else:
        print('Arguments are too short')

