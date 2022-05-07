import cv2
import time
import numpy as np
from os import listdir
from os.path import  join
from source import robo

path = "../data/images/input_imgs/"

IMAGES = [robo.Visao.from_path(join(path, f)) for f in listdir(join(path))]

font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,30)
fontScale              = 1
fontColor              = (255,255,255)
lineType               = 2

if __name__ == "__main__":
    cnt=1
    for OBJ in IMAGES:

        frame = OBJ.img
        width = OBJ.largura
        height = OBJ.altura
        #print(sla)
        image = np.zeros(frame.shape, np.uint8)
        smaller_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        frame = cv2.rotate(frame, cv2.ROTATE_180)
        obj = Classe_imagem(cv2.resize(frame, (0, 0), fx=0.5, fy=0.5))
        mask_img = obj.mask('./ranges_branco.txt')
        mask_img2 = cv2.Canny(mask_img, 50, 150, apertureSize=3)
        _ = checar_alinhamento_pista_v2(obj)
        for i in range(mask_img.shape[0]):
            for j in range(mask_img.shape[1]):
                image[i][j][:3] = mask_img[i][j]

        for i in range(mask_img2.shape[0]):
            for j in range(mask_img2.shape[1]):
                image[i][j+mask_img2.shape[1]][:3] = mask_img2[i][j]
                
        image[height//2:, :width//2] = smaller_frame
        image[height//2:, width//2:] = obj.img
        
        cv2.imwrite("./tests/imagens/output_imgs/"+str(cnt)+".png", image)
        cnt+=1
  