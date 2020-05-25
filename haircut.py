import cv2


def haircut(img_thresh, img, coordidate, sideLength):
    coordidate_length = len(coordidate)
    x=[]
    y=[]
    for i in range(coordidate_length):
        coordidate_tuple = coordidate[i]
        x_mid = int(coordidate_tuple[0]+coordidate_tuple[2])//2
        y_mid = int(coordidate_tuple[1]+coordidate_tuple[3])//2
        x.append(x_mid)
        y.append(y_mid)

    cv2.imshow('src',img)
    cv2.waitKey(0)
    rows = img_thresh.shape[0]
    cols = img_thresh.shape[1]
    # print(rows)
    # print(cols)
    for i in range(rows):
        for j in range(cols):
            if (img_thresh[i][j] < 180):
                img_thresh[i][j] = 0
            else:
                img_thresh[i][j] = 255
    length = len(x)
    # 对边界的点进行移动
    for i in range(length):
        if (x[i] - sideLength//2 < 0):
            abs = sideLength//2 - x[i]
            x[i] = x[i] + abs
        if (x[i] + sideLength//2 > rows):
            abs = x[i] + sideLength/2 - rows
            x[i] = x[i] - abs
        if (y[i] - sideLength//2 < 0):
            abs = sideLength//2 - y[i]
            y[i] = y[i] + abs
        if (y[i] + sideLength//2 > cols):
            abs = y[i] + sideLength//2 - cols
            y[i] = y[i] - abs

    x1 = []
    y1 = []
    x2 = []
    y2 = []
    for i in range(length):
        a1 =int(x[i] - sideLength//2)
        b1 =int(y[i] - sideLength//2)
        a2 =int(x[i] + sideLength//2)
        b2 =int(y[i] + sideLength//2)
        x1.append(a1)
        y1.append(b1)
        x2.append(a2)
        y2.append(b2)

    # print(x1)
    # print(y1)
    # print(x2)
    # print(y2)
    #进行剃发的相关代码
    # Convert the original image to grayscale
    grayScale = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # cv2.imwrite('grayScale_sample1.jpg', grayScale, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

    # Kernel for the morphological filtering
    kernel = cv2.getStructuringElement(1, (60, 60))

    # Perform the blackHat filtering on the grayscale image to find the
    # hair countours
    blackhat = cv2.morphologyEx(grayScale, cv2.MORPH_BLACKHAT, kernel)
    # cv2.imwrite('blackhat_sample1.jpg', blackhat, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

    # intensify the hair countours in preparation for the inpainting
    # algorithm
    ret, thresh2 = cv2.threshold(blackhat, 10, 255, cv2.THRESH_BINARY)
    print(thresh2.shape)
    # cv2.imwrite('thresholded_sample1.jpg', thresh2, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

    # inpaint the original image depending on the mask
    dst = cv2.inpaint(img, thresh2, 1, cv2.INPAINT_TELEA)
    cv2.imwrite('./pic/temp/background.jpg', dst, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    background = cv2.imread("./pic/temp/background.jpg")

    #对光头图片进行毛发渲染
    result = img.copy()
    for i in range(length):
        for m in range(x1[i], x2[i]):
            for n in range(y1[i], y2[i]):
                result[m][n] = [6, 6, 6]

    print('完成')

    for i in range(rows):
        for j in range(cols):
            if (all(result[i][j] != [6, 6, 6])):
                result[i][j] = background[i][j]

    for i in range(length):
        for m in range(x1[i], x2[i]):
            for n in range(y1[i], y2[i]):
                result[m][n] = img[m][n]
    return result

