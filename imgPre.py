import cv2
import time
import math
import numpy as np
import edge as e


def gamma_trans(gray):  # 自适应gamma增强
    mean = np.mean(gray)
    gamma_val = math.log10(0.5) / math.log10(mean / 255)  # 公式计算gamma
    gamma_table = [np.power(x / 255.0, gamma_val) * 255.0 for x in range(256)]  # 建立映射表
    gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)  # 颜色值为整数
    return cv2.LUT(gray, gamma_table)  # 图片颜色查表,另外可以根据光强（颜色）均匀化原则设计自适应算法。


# 以下分离毛发与头皮,输入参数：原图、增强后的灰度图
def diff(src, img):
    # Kernel for the morphological filtering
    kernel = cv2.getStructuringElement(1, (60, 60))
    # Perform the blackHat filtering on the grayscale image to find the
    # hair countours
    blackhat = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)
    # cv2.imwrite('blackhat_sample1.jpg', blackhat, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    # intensify the hair countours in preparation for the inpainting
    # algorithm
    ret, thresh2 = cv2.threshold(blackhat, 10, 255, cv2.THRESH_BINARY)
    print(thresh2.shape)
    # cv2.imwrite('thresholded_sample1.jpg', thresh2, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    # inpaint the original image depending on the mask
    dst = cv2.inpaint(src, thresh2, 1, cv2.INPAINT_TELEA)
    # cv2.imwrite('test_pictures/org111.jpg', dst, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    # dst 去除毛发之后的图片
    dis = cv2.subtract(dst, src)
    cv2.imshow("dis", dis)
    return dis


def small_remove(thresh):
    h, w = thresh.shape
    # 去除较小孤立噪点
    binary, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # 需要搞一个list给cv2.drawContours()才行！！！！！
    c_max = []
    for i in range(len(contours)):
        cnt = contours[i]
        area = cv2.contourArea(cnt)
        # 处理掉小的轮廓区域，这个区域的大小自己定义。
        if area < (h / 150 * w / 150):
            c_min = [cnt]
            # thickness不为-1时，表示画轮廓线，thickness的值表示线的宽度。
            cv2.drawContours(thresh, c_min, -1, (0, 0, 0), thickness=-1)
            continue
    return thresh


# type = 1 时代表对孔洞大小有限制，大于某值时不再填充
def FillHole(im_in, type):
    im_in = cv2.copyMakeBorder(im_in, 2, 2, 2, 2, cv2.BORDER_CONSTANT, value=0)
    # 复制 im_in 图像
    im_floodfill = im_in.copy()
    # Mask 用于 floodFill，官方要求长宽+2
    h1, w1 = im_in.shape[:2]
    mask = np.zeros((h1 + 2, w1 + 2), np.uint8)

    # floodFill函数中的seedPoint对应像素必须是背景
    isbreak = False
    for i in range(im_floodfill.shape[0]):
        for j in range(im_floodfill.shape[1]):
            if im_floodfill[i][j] == 0:
                seedPoint = (i, j)
                isbreak = True
                break
        if isbreak:
            break

    # 得到im_floodfill 255填充非孔洞值
    cv2.floodFill(im_floodfill, mask, seedPoint, 255)

    # 得到im_floodfill的逆im_floodfill_inv
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)

    if type == 1:
        # 之所以复制一份im_floodfill_inv是因为函数findContours会改变im_floodfill_inv_copy
        im_floodfill_inv_copy = im_floodfill_inv.copy()
        # 函数findContours获取轮廓
        binary, cnts, hierarchy = cv2.findContours(im_floodfill_inv_copy, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        size = int(h1 * w1 / 3600)
        for num in range(len(cnts)):
            if cv2.contourArea(cnts[num]) >= size:
                cv2.fillConvexPoly(im_floodfill_inv, cnts[num], 0)

    # 把im_in、im_floodfill_inv这两幅图像结合起来得到前景
    im_out = im_in | im_floodfill_inv
    im_out = im_out[2:h1-2, 2:w1-2]
    # 返回结果
    return im_out


def color_pro(src, gray_img):
    h, w = gray_img.shape
    res = np.zeros((h, w), np.uint8)
    for i in range(h):
        for j in range(w):
            r, g, b = src[i, j]
            # YUV空间里的Y值，大于192判断为浅色
            if r * 0.299 + g * 0.578 + b * 0.114 >= 192:
                res[i, j] = 255
    cv2.imshow("color_res", res)
    return res


def getWhitePixel(th):
    area = 0
    height, width = th.shape
    for i in range(height):
        for j in range(width):
            if th[i, j] == 255:
                area += 1
    ratio = area / (height * width)
    return ratio


def img_pre(src):
    # cv2.imshow("src", src)

    # 转化为灰度图
    gray = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)
    # gamma自适应增强
    img_gamma = gamma_trans(gray)
    # res = color_pro(img_gamma)
    # peppers = e.canny(img_gamma)
    # peppers = FillHole(peppers, 0)
    # cv2.imshow("peppers_fill", peppers)
    # cv2.imshow("img_gamma", img_gamma)
    # ret, th1 = cv2.threshold(img_gamma, 0, 255, cv2.THRESH_OTSU)
    # cv2.imshow("th1", th1)

    # 差值处理
    dis = diff(src, img_gamma)
    # cv2.imshow("dis", dis)
    dis = cv2.cvtColor(dis, cv2.COLOR_BGR2GRAY)
    ret, dis_th1 = cv2.threshold(dis, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # dis_th2 = cv2.add(dis_th1, peppers)
    # cv2.imshow("dis_th", dis_th1)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    dis_th1 = cv2.morphologyEx(dis_th1, cv2.MORPH_CLOSE, kernel)
    # 目前对于短发到这里处理结果比较好
    # dis_th1 = small_remove(dis_th1)
    # dis_th1 = FillHole(dis_th1, 1)
    # cv2.imshow("dis_th11", dis_th1)
    ratio = getWhitePixel(dis_th1)
    print(ratio)
    # 0.120是默认大小，用来区分长发与短发，凸显毫毛的时候可以把参数调大一点，如0.360
    if ratio < 0.120:
        # 创建CLAHE对象
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        # 限制对比度的自适应阈值均衡化
        dst = clahe.apply(dis)
        # 使用全局直方图均衡化
        equa = cv2.equalizeHist(dis)
        dis_de1 = cv2.fastNlMeansDenoising(equa, None, 10, 7, 21)
        ret, dis_th1 = cv2.threshold(dis_de1, 0, 255, cv2.THRESH_OTSU)
    # cv2.imshow("dst", dst)
    # cv2.imshow("equa", equa)
    # cv2.imshow("dis_de1", dis_de1)
    dis_th1 = FillHole(dis_th1, 1)
    dis_th1 = small_remove(dis_th1)
    cv2.imshow("dis_th1", dis_th1)
    return dis_th1


# if __name__ == '__main__':
#     img_path = "./pic/10.png"
#     src = cv2.imread(img_path)
#     # 图像尺寸大小处理
#     src = src[5:800, 165:1625]
#     height, width = src.shape[:2]
#     size = (int(width * 0.5), int(height * 0.5))
#     src = cv2.resize(src, size, interpolation=cv2.INTER_AREA)
#     cv2.imshow("src", src)
#     # 图片预处理，得到二值图
#     binary = img_pre(src)
