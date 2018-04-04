import cv2
import numpy as np


def pix_sub(s1, s2):
    """
    像素值的减法
    :param s1:
    :param s2:
    :return: 差值
    """
    if s1 >= s2:
        return s1 - s2
    else:
        return s2 - s1


def pic_sub(dest,s1,s2):
    for x in range(dest.shape[0]):
        for y in range(dest.shape[1]):
            if(s2[x,y] > s1[x,y]):
                dest[x,y] = s2[x,y] - s1[x,y]
            else:
                dest[x,y] = s1[x,y] - s2[x,y]


def convolve(img, fil, StdDevScale, AbsThreshold, mode='fill'):
    if mode == 'fill':
        h = fil.shape[0] // 2
        w = fil.shape[1] // 2
        img = np.pad(img, ((h, h), (w, w)), 'edge')
    fil_heigh = fil.shape[0]  # 获取卷积核(滤波)的高度
    fil_width = fil.shape[1]  # 获取卷积核(滤波)的宽度

    conv_heigh = img.shape[0] - fil.shape[0] + 1  # 确定卷积结果的大小
    conv_width = img.shape[1] - fil.shape[1] + 1

    m = np.zeros((conv_heigh, conv_width), dtype='float')
    v = np.zeros((conv_heigh, conv_width), dtype='float')
    binary = np.zeros((conv_heigh, conv_width), dtype='uint8')
    for i in range(conv_heigh):
        for j in range(conv_width):
            m[i][j], d = wise_pixel_op(img[i:i + fil_heigh, j:j + fil_width], fil)
            if StdDevScale >= 0:
                v[i][j] = max(StdDevScale * d, AbsThreshold)
            else:
                v[i][j] = min(StdDevScale * d, AbsThreshold)

            if img[i][i] <= abs(m[i][j] - v[i][j]):
                binary[i][j] = 0
            else:
                binary[i][j] = 255
    return m, v, binary


def wise_pixel_op(img):
    mean1, stddev1 = cv2.meanStdDev(img)
    return mean1[0][0], stddev1[0][0]


img = cv2.imread('/Volumes/Transcend/高内涵/image/明场/20/20180402152454.bmp', 0)
# img = cv2.imread('MDA-MB-231-20171208-4x-3B-2xxx.jpg', 0)
img = cv2.imread('MDA-MB-231-20171212-4x-7C-A3.jpg', 0)
# img = cv2.imread('1.png', 0)
# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)#灰度图像
# gray = img
# img = cv2.resize(img, (400, 300), interpolation=cv2.INTER_AREA)
# src = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
#                           cv2.THRESH_BINARY, 11, 10)


StdDevScale = 0
AbsThreshold = 10
block_size = 17

fil = np.ones((block_size, block_size), np.uint8)

mean_array, v_array, binary = convolve(img, fil, StdDevScale, AbsThreshold)

cv2.imshow("1", src)#np.array(mean_array, dtype='uint8'))
cv2.waitKey()
