import cv2
import os
from lxml import etree
import endpoint as end
import xml.dom.minidom


class GEN_Annotations(object):

    def __init__(self, flodername, filename, path):
        self.root = etree.Element("annotation")

        child1 = etree.SubElement(self.root, "folder")
        child1.text = flodername

        child2 = etree.SubElement(self.root, "filename")
        child2.text = filename

        child3 = etree.SubElement(self.root, "path")
        child3.text = path

        child4 = etree.SubElement(self.root, "source")
        child5 = etree.SubElement(child4, "database")
        child5.text = "Unknown"

    def set_size(self, witdh, height, channel):
        '''设置图片尺寸'''
        size = etree.SubElement(self.root, "size")
        widthn = etree.SubElement(size, "width")
        widthn.text = str(witdh)
        heightn = etree.SubElement(size, "height")
        heightn.text = str(height)
        channeln = etree.SubElement(size, "depth")
        channeln.text = str(channel)

    def savefile(self, filename):
        '''保存xml文件'''
        tree = etree.ElementTree(self.root)
        tree.write(filename, pretty_print=True, xml_declaration=False, encoding='utf-8')

    def add_pic_attr(self, label, xmin, ymin, xmax, ymax):
        '''添加图片信息'''
        object = etree.SubElement(self.root, "object")
        namen = etree.SubElement(object, "name")
        namen.text = label
        bndbox = etree.SubElement(object, "bndbox")
        xminn = etree.SubElement(bndbox, "xmin")
        xminn.text = str(xmin)
        yminn = etree.SubElement(bndbox, "ymin")
        yminn.text = str(ymin)
        xmaxn = etree.SubElement(bndbox, "xmax")
        xmaxn.text = str(xmax)
        ymaxn = etree.SubElement(bndbox, "ymax")
        ymaxn.text = str(ymax)


def gene_xml(img, img_name, coorList):
    height, width, depth = img.shape
    filename = img_name
    # 获取图片所在的文件夹名
    path = os.path.abspath(img_name)
    floder_name = os.path.split(path)[0].split('\\')[-1]
    anno = GEN_Annotations(floder_name, filename, path)
    anno.set_size(width, height, depth)

    # 根据端点设置xml文件
    for coor in coorList:
        x, y = coor[1], coor[0]
        swidth, sheight = 15, 15
        left, right = x - swidth, x + swidth
        top, bottom = y - sheight, y + sheight

        if x - 10 < 0:
            pass
        elif x + 10 > width:
            pass
        elif y - 10 < 0:
            pass
        elif y + 10 > height:
            pass
        else:
            xmin, ymin, xmax, ymax = left, top, right, bottom
            anno.add_pic_attr("mouse", xmin, ymin, xmax, ymax)
    anno.savefile('./labelPic/' + img_name.split('.')[0] + '.xml')


# if __name__ == "__main__":
#     img_path = "./pic/1.png"
#     img = cv2.imread('/Users/wangmian/Downloads/x.PNG')
#     dis = end.thinImage(img)
#     endpoint = end.endPoint(dis)
#     gene_xml(img_path, endpoint)
