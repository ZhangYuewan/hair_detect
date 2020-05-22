# -*- coding: UTF-8 -*-

# 对canny阈值做了一个自适应的过程

import numpy as np
import cv2
import copy
import math


def gradient(blurred):
    # 对平滑后的图像使用Sobel算子计算水平方向和竖直方向的一阶导数（图像梯度）（Gx和Gy）
    # 根据得到的这两幅梯度图找到边界的梯度和方向
    # ksize=3是因为cv2.Canny方法默认的Ksize=3
    # cv2.CV_64F是使用64位存储，为了运算不越界
    sobelx = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)

    # 建立两个np.arr类型的数据
    sobel = np.zeros((len(sobelx), len(sobelx[0])))
    theat = np.zeros((len(sobelx), len(sobelx[0])))

    # 根据公式计算合成梯度值
    for i in range(len(sobelx)):
        for j in range(len(sobelx[0])):
            sobel[i][j] = math.sqrt(sobelx[i][j] * sobelx[i][j] + sobely[i][j] * sobely[i][j])
            # 将弧度转化为度数
            if sobelx[i][j] != 0:
                theat[i][j] = math.atan(sobely[i][j] / sobelx[i][j]) * 180 / math.pi
            else:
                if sobely[i][j] < 0:
                    theat[i][j] = -90
                elif sobely[i][j] > 0:
                    theat[i][j] = 90
                elif sobely[i][j] == 0:
                    theat[i][j] = 45
            # 做边界的划分，划分为四个梯度值
            temp = theat[i][j]
            if -112.5 < temp <= -67.5:
                theat[i][j] = 90
            elif -67.5 < temp <= -22.5:
                theat[i][j] = 135
            elif -22.5 < temp <= 22.5:
                theat[i][j] = 0
            elif 22.5 < temp <= 67.5:
                theat[i][j] = 45
            elif 67.5 < temp <= 112.5:
                theat[i][j] = 90
    # 以下是 非极大值抑制 的算法
    # 模型结束后移到另一个文件并做精简
    # 还要考虑和nms算法的异同

    # 做非边界部分的判断
    # i从1到倒数第二，j同样
    for i in range(1, len(sobel) - 1):
        for j in range(1, len(sobel[0]) - 1):
            if theat[i][j] == 0:
                if sobel[i][j] < max(sobel[i + 1][j], sobel[i - 1][j]):
                    blurred[i][j] = 0
            elif theat[i][j] == 45:
                if sobel[i][j] < max(sobel[i + 1][j - 1], sobel[i - 1][j - 1]):
                    blurred[i][j] = 0
            elif theat[i][j] == 90:
                if sobel[i][j] < max(sobel[i][j + 1], sobel[i][j - 1]):
                    blurred[i][j] = 0
            elif theat[i][j] == 135:
                if sobel[i][j] < max(sobel[i + 1][j - 1], sobel[i - 1][j + 1]):
                    blurred[i][j] = 0

    # 上边界非端点处理，i=0，i不能减1
    for j in range(1, len(sobelx[0]) - 1):
        i = 0
        if theat[0][j] == 0:
            if sobel[i][j] < sobel[i + 1][j]:
                blurred[i][j] = 0
        elif theat[0][j] == 45:
            if sobel[i][j] < sobel[i + 1][j - 1]:
                blurred[i][j] = 0
        elif theat[0][j] == 90:
            if sobel[i][j] < max(sobel[i][j + 1], sobel[i][j - 1]):
                blurred[i][j] = 0
        elif theat[0][j] == 135:
            if sobel[i][j] < sobel[i + 1][j - 1]:
                blurred[i][j] = 0
    # 下边界非端点，i = 255，i不能加1
    for j in range(1, len(sobel[0]) - 1):
        i = len(theat) - 1
        if theat[i][j] == 0:
            if sobel[i][j] < sobel[i - 1][j]:
                blurred[i][j] = 0
        elif theat[i][j] == 45:
            if sobel[i][j] < sobel[i - 1][j - 1]:
                blurred[i][j] = 0
        elif theat[i][j] == 90:
            if sobel[i][j] < max(sobel[i][j + 1], sobel[i][j - 1]):
                blurred[i][j] = 0
        elif theat[i][j] == 135:
            if sobel[i][j] < sobel[i - 1][j + 1]:
                blurred[i][j] = 0
    # 左边界非端点，j=0，j不能减1
    for i in range(1, len(sobel) - 1):
        j = 0
        if theat[i][j] == 0:
            if sobel[i][j] < max(sobel[i + 1][j], sobel[i - 1][j]):
                blurred[i][j] = 0
        elif theat[i][j] == 90:
            if sobel[i][j] < sobel[i][j + 1]:
                blurred[i][j] = 0
        elif theat[i][j] == 135:
            if sobel[i][j] < sobel[i - 1][j + 1]:
                blurred[i][j] = 0
    # 右边界非端点，j=255，不能加1
    for i in range(1, len(sobel) - 1):
        j = len(sobel[0]) - 1
        if theat[i][j] == 0:
            if sobel[i][j] < max(sobel[i + 1][j], sobel[i - 1][j]):
                blurred[i][j] = 0
        elif theat[i][j] == 45:
            if sobel[i][j] < max(sobel[i + 1][j - 1], sobel[i - 1][j - 1]):
                blurred[i][j] = 0
        elif theat[i][j] == 90:
            if sobel[i][j] < sobel[i][j - 1]:
                blurred[i][j] = 0
        elif theat[i][j] == 135:
            if sobel[i][j] < sobel[i + 1][j - 1]:
                blurred[i][j] = 0
    # 左上角。i，j不能减1
    if theat[0][0] == 0:
        if sobel[0][0] < sobel[0 + 1][0]:
            blurred[0][0] = 0
    elif theat[0][0] == 90:
        if sobel[0][0] < sobel[0][0 + 1]:
            blurred[0][0] = 0
    # 左下角，i不能加，j不能减
    if theat[len(sobel) - 1][0] == 0:
        if sobel[len(sobel) - 1][0] < sobel[len(sobel) - 1 - 1][0]:
            blurred[len(sobel - 1)][0] = 0
    elif theat[len(sobel) - 1][0] == 90:
        if sobel[len(sobel) - 1][0] < sobel[len(sobel) - 1][0 + 1]:
            blurred[len(sobel) - 1][0] = 0
    elif theat[len(sobel) - 1][0] == 135:
        if sobel[len(sobel) - 1][0] < sobel[len(sobel) - 1 - 1][0 + 1]:
            blurred[len(sobel) - 1][0] = 0
    # 右下角 右上角暂时没写，可仿照上文实现

    return blurred


def loop(gradient):
    Max = np.max(gradient)
    Min = np.min(gradient)

    # T是初始平均值，Tnew是迭代平均值
    t = (Max + Min) / 2

    while True:
        imagemax = copy.deepcopy(gradient)
        imagemin = copy.deepcopy(gradient)
        imagemax[imagemax < t] = 0
        imagemin[imagemin >= t] = 0

        tnew = ((sum(imagemax[imagemax > 0]) / len(imagemax[imagemax > 0])) + sum(imagemin[imagemin > 0]) / len(
            imagemin[imagemin > 0])) / 2
        if abs(tnew - t) < 1:
            break
        else:
            t = tnew
    return tnew


def canny(peppers):
    # 读取一张图片,做灰度化处理,转为二维矩阵。虽然原图是灰度图,但仍需此步骤,不然会是三维矩阵
    # 使用高斯滤波消除噪声
    # (5,5)是高斯核的大小,0是sigmaX,0的意思是让方程自己给你算对应的sigma
    peppers_b = cv2.GaussianBlur(peppers, (5, 5), 0)
    peppers_t = copy.deepcopy(peppers_b)
    # 返回的是经过非极大值抑制后的矩阵
    peppers_g = gradient(peppers_t)
    # 返回的是迭代后的最优阈值
    peppers_T = loop(peppers_g)
    # 这一条就只会使用大津法算出的阈值,但大津有缺点,直方图没有明显双峰时效果可能不好
    peppers_ret, image = cv2.threshold(peppers_b, peppers_T, 255, cv2.THRESH_OTSU)
    # 因为想要有更多的边被画出来,所以取更小的（我自己一厢情愿的,可能没有理论依据）
    peppers_T = min(peppers_ret, peppers_T)
    ret, binary = cv2.threshold(peppers_b, peppers_T, 255, cv2.THRESH_BINARY)
    # cv2.imshow('binary', binary)
    peppers = cv2.Canny(peppers_b, peppers_T / 4, peppers_T)
    # 这是自适应阈值的边缘切割,用高斯核做窗口去给每一个像素一个自适应阈值
    # 最后一个参数会影响切割质量,具体原理请参考文档
    # 倒数第二个会影响切割出来的边的宽度,原理见文档
    # peppers_two = cv2.adaptiveThreshold(peppers_b, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 3, 2)

    # cv2.imshow('peppers', peppers)
    # cv2.imshow('peppers_two', peppers_two)
    return peppers


def edge_pro(dis, edge):
    h, w = dis.shape[:2]
    for i in range(h):
        for j in range(w):
            dis[i, j] = dis[i, j] if dis[i, j] > edge[i, j] else 0
    return dis
