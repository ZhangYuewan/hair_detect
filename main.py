import cv2
import imgPre as imp
import endpoint as end
import gene_xml as gene
import prediction_2 as pdt
import haircut as hc
import count as num
import time

if __name__ == '__main__':
    # 读入图片
    img_path = "./pic/10.png"
    src = cv2.imread(img_path)
    tic = time.clock()
    # 图像尺寸大小处理
    src = src[5:800, 165:1625]
    height, width = src.shape[:2]
    size = (int(width * 0.5), int(height * 0.5))
    src = cv2.resize(src, size, interpolation=cv2.INTER_AREA)
    cv2.imshow("src", src)
    # 图片预处理，得到二值图
    binary = imp.img_pre(src)
    print(binary.shape)
    # 细化求线段端点
    thinBinary = end.thinImage(binary)
    # cv2.imshow("thinBinary", thinBinary*255)
    endpoint = end.endPoint(thinBinary)
    print("find endpoints, done!")
    # 根据端点坐标生成xml文件
    pathlist = img_path.split("/")
    img_name = pathlist[-1]
    gene.gene_xml(src, img_name, endpoint)
    print("generate xml file, done!")
    xmlPath = './labelPic/' + img_name.split('.')[0] + '.xml'
    # 判断端点是否为毛囊
    # coordinate = pdt.prediction(xmlPath, cv2.cvtColor(thinBinary*255, cv2.COLOR_GRAY2RGB), './model/99model_2.pkl')
    coordinate = pdt.prediction(xmlPath, src, './model/99model_2.pkl')
    print("predict the endpoints, done!")
    # 进行剃发，最后一个参数指的是正方形的边长
    print("coordinate", coordinate)
    img_res = hc.haircut(binary, src, coordinate, 40)
    cv2.imshow("img_res", img_res)
    sumcount = num.countHair(coordinate, binary)
    print("sumcount", sumcount)
    toc = time.clock()
    print("执行时间：", toc)
    cv2.waitKey(0)