import sys
import cv2
from PIL import Image, ImageDraw
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
    count = 0

    #名前の重複チェック
    check_name(dbpath, name, count)
    print('count:', count)

    #ビデオ入力開始
    while(True):
        ret, face = img_crop(cap)
        #顔が見つかなれば継続
        if (face == None):
            continue

        #マスクなしモード設定
        if mode == 0:
            mode = 1
        #マスクなしモードを設定するか
        print('マスクなしモードを設定するか Yes:0 Skip:1')
        regist_skip(skip, mode, count)
        print(skip, mode, count)
        #マスクなしモード登録
        if mode == 1:
            print('マスクなしモード登録')
            regist_dbx3(face, dbpath, name, skip, mode, count)

        #マスクありモードを設定するか
        print('マスクありモードを設定するか Yes:0 Skip:1')
        regist_skip(skip, mode, count)
        print(skip, mode, count)
        #マスクありモード登録
        if mode == 2:
            print('マスクありモード登録')
            regist_dbx3(face, dbpath, name, skip, mode, count)

        #テスト
        print('テストするか Yes:0 Skip:1')
        regist_skip(skip, mode, count)
        if mode == 3 and skip == False:
            detect = facenet.compare_similarity(face, dbpath)
            if detect == '':
                print('顔認証テスト　NG')
            else:
                print('you are ', detect)

        if skip == True or mode == 3:
            print('登録終了しますか？　Yes:0　No:1')
            if keyinput.keyin() == '1':
                print('登録終了')
                break
            else:
                print('再登録')
                mode = 0
                skip = True
                count = 0

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

def img_crop(cap):
    #カメラからの画像取得
    ret, frame = cap.read()
    #OpenCV→Pill変換
    pill = cv2pil.cv2pil(frame)
    #顔検出
    face = facenet.detect_face(pill, 'out.jpg')
    print(face)
    #画像表示
    cv2.imshow('camera', frame)
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

    cv2.waitKey(10)

    return ret, face

def regist_dbx3(img_cropped, dbpath, name, skip, mode, count):
    #データ登録
    regist_db(img_cropped, dbpath, name + '_' + str(count))
    print('データ登録')
    count = count + 1
    #3枚登録
    if count > 3:
        skip = True
        mode = mode + 1

def regist_db(img_cropped, dbpath, name):
    #切り出し画像でデータ作成
    feature_vector = facenet.feature_vector(img_cropped)
    #DB登録
    return 

def regist_skip(skip, mode, count):
    if skip == True:
        if mode == 1:
            print('マスクなし画像を登録します')
        elif mode == 2:
            print('マスクあり画像を登録します')
        else:
            print('顔検証します')

        if keyinput.keyin() == '1':
            skip = True
            mode = mode + 1
            count = 0
        else:
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

