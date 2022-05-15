import cv2
import time
import numpy as np
from os import listdir
from os.path import  join
from root.source.robo.visao.visao import Visao

path = "./data/images/input_imgs/"

VISAO = [Visao.from_path(join(path, f)) for f in listdir(join(path))]

font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,30)
fontScale              = 1
fontColor              = (255,255,255)
lineType               = 2

def main():
    cnt=1
    for obj in VISAO:
        ret = obj.decisao_alinhamento()
        cv2.putText(obj.img, ret, bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
        cv2.imwrite("./data/images/teste_alinhamento/"+str(cnt)+".png", obj.img)
        cnt+=1
  