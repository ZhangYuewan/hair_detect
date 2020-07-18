import cv2

def getDim(points,img_skeleton,img_thresh,diam_of_follicle):
    rows = img_skeleton.shape[0]
    cols = img_skeleton.shape[1]
    for i in range(rows):
        for j in range(cols):
            if (img_thresh[i][j] < 180):
                img_thresh[i][j] = 0
            else:
                img_thresh[i][j] = 255

    for i in range(rows):
        for j in range(cols):
            if (img_skeleton[i][j] < 180):
                img_skeleton[i][j] = 0
            else:
                img_skeleton[i][j] = 255

    point_tuple1 = points[0]
    x1 = point_tuple1[0]
    y1 = point_tuple1[1]

    point_tuple2 = points[1]
    x2 = point_tuple2[0]
    y2 = point_tuple2[1]

    diam = 0
    for j in range(cols):
        y = ((y2 - y1) / (x1 - x2)) * (j - x1) + y1
        y = int(y)
        if (img_thresh[y][j] == 255):
            diam = diam + 1

    is_follicle = False

    if(diam<diam_of_follicle):
        is_follicle = True

    result = []
    result.append(diam)
    result.append(is_follicle)
    return result
