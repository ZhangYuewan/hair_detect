from torchvision import transforms
import torch
import xml
import cv2


def prediction(xmls, imgs, models):
      DOMTree = xml.dom.minidom.parse(xmls)
      collection = DOMTree.documentElement
      objects = collection.getElementsByTagName("object")
      net = torch.load(models)
      coordinate=[]
      maonang_num = 0

      for object in objects:
            bndbox = object.getElementsByTagName('bndbox')[0]
            xmin = bndbox.getElementsByTagName('xmin')[0]
            xmin_data = xmin.childNodes[0].data
            ymin = bndbox.getElementsByTagName('ymin')[0]
            ymin_data = ymin.childNodes[0].data
            xmax = bndbox.getElementsByTagName('xmax')[0]
            xmax_data = xmax.childNodes[0].data
            ymax = bndbox.getElementsByTagName('ymax')[0]
            ymax_data = ymax.childNodes[0].data
            xmin = int(xmin_data)
            xmax = int(xmax_data)
            ymin = int(ymin_data)
            ymax = int(ymax_data)
            img_cut = imgs[ymin:ymax, xmin:xmax, :]

            crop_obj=transforms.Compose([
              transforms.ToPILImage(),
              transforms.CenterCrop((64, 64)),
              transforms.ToTensor(),
              transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
            ])
            img_cut = crop_obj(img_cut)
            img_cut = torch.unsqueeze(img_cut, dim=0).float()
            outputs = net(img_cut)
            _, predicted = torch.max(outputs, 1)
            if predicted == 1:
                  coordinate.append((xmin, ymin, xmax, ymax))
                  maonang_num += 1
      print("maonang number: ", maonang_num)
      return coordinate

# imge=cv2.imread("./pic/10.png")
# coordinate=prediction("./labelPic/10.xml",imge,'./99model.pkl')
# print(coordinate)