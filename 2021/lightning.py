from skimage import exposure
import matplotlib.pyplot as plt
from os import listdir
from os.path import  join
import argparse
import cv2
import numpy as np
# construct the argument parser and parse the arguments
"""ap = argparse.ArgumentParser()
ap.add_argument("-s", "--source", required=True,
	help="path to the input source image")
ap.add_argument("-r", "--reference", required=True,
	help="path to the input reference image")
args = vars(ap.parse_args())"""
path = "./tests/imagens/input_imgs/"

class Classe_imagem():
    def __init__(self, img):
        self.cont = 0
        #print("Entrando no _init_ do Classe_imagem()")
        #img = cv2.imread(path)
        img = np.array(img)

        img = cv2.rotate(img, cv2.ROTATE_180)

        img.astype(np.uint8)

        (self.altura, self.largura) = img.shape[:2] 
        self.centro = ( (self.largura)/2, (self.altura)/2 )

        #M = cv2.getRotationMatrix2D(self.centro, 180, 1)

        #print("Altura: {}  Largura: {}".format(self.altura,self.largura))

        #img = cv2.warpAffine(img, M, (self.largura, self.altura))

        #print("SAIMO DO WARPAFFINE")
        self.img = img
        #self.topo_da_pista = int(0.0*self.altura) #coordenada y do topo da pista
        self.topo_da_pista = int((self.altura)*0 )
        self.meio_da_pista = 0 # coordenada x do meio da pista
        self.largura_pista = 0 # largura do final da pista na imagem
        self.mult_largura_pista = 0.8 #ate quanto da metade da largura da pista ainda eh atravessavel pelo robo
        #print("Saindo do _init_ do Classe_imagem()")

    def mask(self, ranges_file_path):
        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV) # converte a cor para hsv
        with open(ranges_file_path, "r") as f:
            lines = f.readlines()
            range = lines[0].split(",")
            lower = np.array([int(range[0]),int(range[1]),int(range[2])])  #range de cores em hsv para reconhecer as bordas
            upper = np.array([int(range[3]),int(range[4]),int(range[5])])
        mask = cv2.inRange(hsv, lower, upper)
        kernel = np.ones((5,5), np.uint8) 
        #mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)
        #mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        return mask

IMAGES = [Classe_imagem(cv2.imread(join(path, f))) for f in listdir(join(path))]
# load the source and reference images
cnt=1
ref = cv2.imread("./tests/imagens/input_imgs/i.jpg")
for OBJ in IMAGES:
    src = OBJ.img
    multi = True if src.shape[-1] > 1 else False
    matched = exposure.match_histograms(src, ref, multichannel=multi)
    # show the output images
    cv2.imwrite("./tests/imagens/hm_imgs/"+str(cnt)+".png", matched)
    cnt+=1