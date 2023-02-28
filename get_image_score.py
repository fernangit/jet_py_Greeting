#https://hiroki.jp/detect_blur
import cv2
import sys

#ピンぼけ度合をスコア化
def score(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian =  variance_of_laplacian(gray)
    print('image_score = ', laplacian)
    return laplacian

#エッジ検出
def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()

if __name__ == '__main__':
    #args[1] = image_path
    args = sys.argv
    if 2 <= len(args):
        print(args[1])
        score(args[1])
    else:
        print('Arguments are too short')
