import cv2
import numpy as np

def thinImage(img):
    H, W, C = img.shape
    dis = (np.array(img)/255).astype('uint8')[:,:,0:1]
    dis = dis.squeeze()
    flag = []

    while True:
        for i in range(H):
            for j in range(W):
                p1 = dis[i, j]
                if p1 != 1:
                    continue
                p2 = 0 if i == 0 else dis[i-1, j]
                p3 = 0 if i == 0 or j == W-1 else dis[i-1, j+1]
                p4 = 0 if j == W-1 else dis[i, j+1]
                p5 = 0 if i == H-1 or j == W-1 else dis[i+1, j+1]
                p6 = 0 if i == H-1 else dis[i+1, j]
                p7 = 0 if i == H-1 or j == 0 else dis[i+1, j-1]
                p8 = 0 if j == 0 else dis[i, j-1]
                p9 = 0 if i == 0 or j == 0 else dis[i-1, j-1]
                if p2+p3+p4+p5+p6+p7+p8+p9 >= 2 and p2+p3+p4+p5+p6+p7+p8+p9 <= 6:
                    ap = 0
                    if p2 == 0 and p3 == 1:
                        ap = ap+1
                    if p3 == 0 and p4 == 1:
                        ap = ap+1
                    if p4 == 0 and p5 == 1:
                        ap = ap+1
                    if p5 == 0 and p6 == 1:
                        ap = ap+1
                    if p6 == 0 and p7 == 1:
                        ap = ap+1
                    if p7 == 0 and p8 == 1:
                        ap = ap+1
                    if p8 == 0 and p9 == 1:
                        ap = ap+1
                    if p9 == 0 and p2 == 1:
                        ap = ap+1
                    if ap == 1 and p2 * p4 * p6 == 0 and p4 * p6 * p8 == 0:
                        flag.append((i, j))

        for i in range(len(flag)):
            dis[flag[i]] = 0

        if len(flag) == 0:
            break
        else:
            flag.clear()
        for i in range(H):
            for j in range(W):
                p1 = dis[i, j]
                if p1 != 1:
                    continue
                p2 = 0 if i == 0 else dis[i-1, j]
                p3 = 0 if i == 0 or j == W-1 else dis[i-1, j+1]
                p4 = 0 if j == W-1 else dis[i, j+1]
                p5 = 0 if i == H-1 or j == W-1 else dis[i+1, j+1]
                p6 = 0 if i == H-1 else dis[i+1, j]
                p7 = 0 if i == H-1 or j == 0 else dis[i+1, j-1]
                p8 = 0 if j == 0 else dis[i, j-1]
                p9 = 0 if i ==0 or j == 0 else dis[i-1, j-1]
                if p2+p3+p4+p5+p6+p7+p8+p9 >= 2 and p2+p3+p4+p5+p6+p7+p8+p9 <= 6:
                    ap = 0
                    if p2 == 0 and p3 == 1:
                        ap = ap+1
                    if p3 == 0 and p4 == 1:
                        ap = ap+1
                    if p4 == 0 and p5 == 1:
                        ap = ap+1
                    if p5 == 0 and p6 == 1:
                        ap = ap+1
                    if p6 == 0 and p7 == 1:
                        ap = ap+1
                    if p7 == 0 and p8 == 1:
                        ap = ap+1
                    if p8 == 0 and p9 == 1:
                        ap = ap+1
                    if p9 == 0 and p2 == 1:
                        ap = ap+1
                    if ap == 1 and p2 * p4 * p8 == 0 and p2 * p6 * p8 == 0:
                        flag.append((i, j))

        for i in range(len(flag)):
            dis[flag[i]] = 0

        if len(flag) == 0:
            break
        else:
            flag.clear()
    return dis


def endPoint(dis):
    H, W = dis.shape
    endpoint = []
    for i in range(H):
        for j in range(W):
            p1 = dis[i, j]
            if p1 != 1:
                continue
            p2 = 0 if i == 0 else dis[i - 1, j]
            p3 = 0 if i == 0 or j == W - 1 else dis[i - 1, j + 1]
            p4 = 0 if j == W - 1 else dis[i, j + 1]
            p5 = 0 if i == H - 1 or j == W - 1 else dis[i + 1, j + 1]
            p6 = 0 if i == H - 1 else dis[i + 1, j]
            p7 = 0 if i == H - 1 or j == 0 else dis[i + 1, j - 1]
            p8 = 0 if j == 0 else dis[i, j - 1]
            p9 = 0 if i == 0 or j == 0 else dis[i - 1, j - 1]
            if p2+p3+p4+p5+p6+p7+p8+p9 == 1:
                endpoint.append((i, j))

    return endpoint


img = cv2.imread('/Users/wangmian/Downloads/x.PNG')
dis = thinImage(img)
endpoint = endPoint(dis)
print(endpoint)





