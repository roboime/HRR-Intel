from visao import bordas_laterais_v2, Classe_imagem
#from classes import Classe_camera
from funcoes import checar_alinhamento_pista_v2
import cv2
import numpy as np

def sla():    #camera = Classe_camera()
    for i in range(141):
        path = "./tests/imagens/filme6/" + str(i) + ".jpg"
        obj = Classe_imagem(path)
        checar_alinhamento_pista_v2(obj)
        cv2.imwrite("./tests/imagens/filme7/" + str(i) + ".jpg", obj.img)
if __name__ == "__main__":
    img_array = []
    for i in range(3, 144):
        img = cv2.imread("./tests/imagens/filme8/" + str(i) + ".jpg")
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)

    
    out = cv2.VideoWriter('./project2.avi',cv2.VideoWriter_fourcc(*'DIVX'), 4, size)
    
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

