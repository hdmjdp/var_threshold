import cv2
import numpy as np


def _convolve(img, fil, StdDevScale, AbsThreshold, mode='fill'):
    if mode == 'fill':
        h = fil.shape[0] // 2
        w = fil.shape[1] // 2
        img = np.pad(img, ((h, h), (w, w)), 'edge')
    fil_heigh = fil.shape[0]  # 获取卷积核(滤波)的高度
    fil_width = fil.shape[1]  # 获取卷积核(滤波)的宽度

    conv_heigh = img.shape[0] - fil.shape[0] + 1  # 确定卷积结果的大小
    conv_width = img.shape[1] - fil.shape[1] + 1

    m = np.zeros((conv_heigh, conv_width), dtype='uint8')
    v = np.zeros((conv_heigh, conv_width), dtype='uint8')
    binary = np.zeros((conv_heigh, conv_width), dtype='uint8')
    for i in range(conv_heigh):
        for j in range(conv_width):  # 逐点相乘并求和得到每一个点
            m[i][j], d = wise_element_sum(img[i:i + fil_heigh, j:j + fil_width], fil)
            if StdDevScale >= 0:
                v[i][j] = max(StdDevScale * d, AbsThreshold)
            else:
                v[i][j] = min(StdDevScale * d, AbsThreshold)

            if img[i][i] <= m[i][j] - v[i][j]:
                binary[i][j] = 0
            else:
                binary[i][j] = 255
    return m, v, binary


def wise_element_sum(img, fil):
    # res = (img * fil).sum()
    # print(res)
    mean1, stddev1 = cv2.meanStdDev(img)
    # print(mean1[0][0], stddev1[0][0])
    # if (res < 0):
    #     res = 0
    # elif res > 255:
    #     res = 255
    return mean1[0][0],  stddev1[0][0]


img = cv2.imread('/Volumes/Transcend/高内涵/image/明场/20/20180402152454.bmp', 0)
img = cv2.imread('MDA-MB-231-20171208-4x-3B-2xxx.jpg', 0)
# img = cv2.imread('1.png', 0)
# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)#灰度图像
# gray = img
img = cv2.resize(img, (400, 300), interpolation=cv2.INTER_AREA)
# median = cv2.medianBlur(gray, ksize=9)
# thresh = 10
# s = gray.copy()

StdDevScale = 5.2
AbsThreshold = 30
block_size = 7

fil = np.ones((block_size, block_size), np.uint8)

mean_array, v_array, binary = _convolve(img, fil, StdDevScale, AbsThreshold)

cv2.imshow("1", binary)
cv2.waitKey()