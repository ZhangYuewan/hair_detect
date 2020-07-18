import cv2
import endpoint as end


def countHairSingle(di):
    count = 0
    H, W = di.shape
    for i in range(H):
        for j in range(W):
            p1 = di[i, j]
            if p1 != 1:
                continue
            p2 = 0 if i == 0 else di[i - 1, j]
            p3 = 0 if i == 0 or j == W - 1 else di[i - 1, j + 1]
            p4 = 0 if j == W - 1 else di[i, j + 1]
            p5 = 0 if i == H - 1 or j == W - 1 else di[i + 1, j + 1]
            p6 = 0 if i == H - 1 else di[i + 1, j]
            p7 = 0 if i == H - 1 or j == 0 else di[i + 1, j - 1]
            p8 = 0 if j == 0 else di[i, j - 1]
            p9 = 0 if i == 0 or j == 0 else di[i - 1, j - 1]

            if p2 + p3 + p4 + p5 + p6 + p7 + p8 + p9 == 1:
                count += 1
    return count / 2


def countHair(coordinate, binary):
    sumcount = 0
    coordidate_length = len(coordinate)
    for i in range(coordidate_length):
        coorTuple = coordinate[i]
        xmin, ymin, xmax, ymax = coorTuple[0], coorTuple[1], coorTuple[2], coorTuple[3]
        di = binary[ymin:ymax, xmin:xmax]
        di = end.thinImage(di)
        # cv2.imwrite('./pic/temp/objects/%d.jpg' % i, di)
        count = countHairSingle(di)
        if count >= 4:
            count = 3
        sumcount += count
    return int(sumcount)
