import cv2
import time
import numpy as np
from os import listdir
from os.path import  join
from funcoes import *

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

font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,30)
fontScale              = 1
fontColor              = (255,255,255)
lineType               = 2

def bordas_laterais_v2(objeto_imagem):
    mask = objeto_imagem.mask("ranges_branco.txt")
   # reconhecer_pista(mask, objeto_imagem)
    img = objeto_imagem.img
    edges = cv2.Canny(mask, 50, 150, apertureSize=3)
    cv2.imwrite("./tests/mask.png", mask)

    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=40, minLineLength=10, maxLineGap=50)
  #  lines = cv2.HoughLinesP(mask, 1, np.pi/180, threshold=100, minLineLength=10, maxLineGap=20)
    left_lines = []
    right_lines =[]
   # todas_as_linhas = IMG
    if lines is not None:
        for line in lines:
            line = line.reshape(4)
            x1,y1,x2,y2 = line
            img = cv2.line(img, (x1,y1), (x2,y2), (0,127,255), 2)
        	
            desvio_maximo = np.pi/180*RANGE_INCLINACAO
            #print("topo da imagem", objeto_imagem.topo_da_pista)
            #print("range inclinacao", RANGE_INCLINACAO)
            #print("pontos: ", line)
            #print("coef_angular: ", coef_angular(line))
            #print("angulo: ", 180/np.pi*math.atan(coef_angular(line)))
            if y1>objeto_imagem.topo_da_pista or y2>objeto_imagem.topo_da_pista:
                if math.atan(1)-desvio_maximo/2 < math.atan(coef_angular(line)) < math.atan(1)+desvio_maximo/2 and (x1 >= objeto_imagem.largura//2 or x2 >= objeto_imagem.largura//2):
                    right_lines.append([x1,y1,x2,y2])
                #    print("angulo : ", 180/np.pi*math.atan(coef_angular(line)))
                  #  print([x1, y1, x2, y2])
                    cv2.line(objeto_imagem.img, (x1,y1), (x2,y2), (0,255,0), 2)
                if math.atan(-1)-desvio_maximo/2 < math.atan(coef_angular(line)) < math.atan(-1)+desvio_maximo/2 and (x1 < objeto_imagem.largura//2 or x2 < objeto_imagem.largura//2):
                    left_lines.append([x1,y1,x2,y2])
                    cv2.line(objeto_imagem.img, (x1,y1), (x2,y2), (0,127,0), 2)
    else: return [],[],NAO_HA_RETA
   # cv2.imwrite("todas_as_linhas.png", todas_as_linhas)

    ha_reta_na_direita = False
    if(len(right_lines) != 0):
        ha_reta_na_direita = True
        vertical_direita = [objeto_imagem.largura,0,objeto_imagem.largura,objeto_imagem.altura]
        y_max = 0
        right = right_lines[0]
        for line in right_lines:
            _,y = interscetion(line, vertical_direita)
            if y > y_max:
                y_max = y
                right = line
        [x1, y1, x2, y2] = right
        cv2.line(objeto_imagem.img, (x1,y1), (x2,y2), (0,0,255), 2)
        
    ha_reta_na_esquerda = False
    if(len(left_lines) != 0):
        ha_reta_na_esquerda = True
        vertical_esquerda = [0,0,0,objeto_imagem.altura]
        y_max = 0
        left = left_lines[0]
        for line in left_lines:
            _,y = interscetion(line, vertical_esquerda)
            if y > y_max:
                y_max = y
                left = line
        [x1, y1, x2, y2] = left
        cv2.line(objeto_imagem.img, (x1,y1), (x2,y2), (0,0,255), 2)

    cv2.imwrite("./tests/bordas_laterais.jpg", objeto_imagem.img)
    if ha_reta_na_direita == False and ha_reta_na_esquerda == False:
        return [],[],NAO_HA_RETA
    if ha_reta_na_direita == True and ha_reta_na_esquerda == True:
        return left, right, HA_DUAS_RETAS
    if ha_reta_na_direita == False and ha_reta_na_esquerda == True:
        return left, [], SO_ESQUERDA
    if ha_reta_na_direita == True and ha_reta_na_esquerda == False:
        return [], right, SO_DIREITA



def checar_alinhamento_pista_v2(objeto_imagem):
    left, right, caso = bordas_laterais_v2(objeto_imagem)
    k = objeto_imagem.largura//2
    if caso == SO_DIREITA:
        horizontal = [0, objeto_imagem.topo_da_pista, objeto_imagem.largura, objeto_imagem.topo_da_pista]
        x, _ = interscetion(horizontal, right)
        delta_x = x-objeto_imagem.largura//2
        min_largura = int(k - (objeto_imagem.altura - objeto_imagem.topo_da_pista) / coef_angular(right))
        objeto_imagem.img = cv2.circle(objeto_imagem.img, (x, objeto_imagem.topo_da_pista), radius=10, color=(0, 0, 255), thickness=-1)
        objeto_imagem.img = cv2.line(objeto_imagem.img, (objeto_imagem.largura//2 + min_largura, 0), (objeto_imagem.largura//2 + min_largura, objeto_imagem.altura), (127, 127, 0), 2)
        objeto_imagem.img = cv2.line(objeto_imagem.img, (objeto_imagem.largura//2, 0), (objeto_imagem.largura//2, objeto_imagem.altura), (255, 0, 0), 2)
        if delta_x > min_largura and delta_x > 0:
            cv2.putText(objeto_imagem.img,'SO DIREITA: ALINHADO', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
            return ANDAR
        else:
            cv2.putText(objeto_imagem.img,'SO DIREITA: GIRAR ESQUERDA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
            return GIRAR_ESQUERDA
    elif caso == SO_ESQUERDA:
        horizontal = [0, objeto_imagem.topo_da_pista, objeto_imagem.largura, objeto_imagem.topo_da_pista]
        x, _ = interscetion(horizontal, left)
        delta_x = -x + objeto_imagem.largura//2
        min_largura = int(k + (objeto_imagem.altura - objeto_imagem.topo_da_pista) / coef_angular(left))
        objeto_imagem.img = cv2.circle(objeto_imagem.img, (x, objeto_imagem.topo_da_pista), radius=10, color=(0, 0, 255), thickness=-1)
        objeto_imagem.img = cv2.line(objeto_imagem.img, (objeto_imagem.largura//2 - min_largura, 0), (objeto_imagem.largura//2 - min_largura, objeto_imagem.altura), (127, 127, 0), 2)
        objeto_imagem.img = cv2.line(objeto_imagem.img, (objeto_imagem.largura//2, 0), (objeto_imagem.largura//2, objeto_imagem.altura), (255, 0, 0), 2)
        if delta_x > min_largura and delta_x > 0:
            cv2.putText(objeto_imagem.img,'SO ESQUERDA: ALINHADO', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
            return ANDAR
        else:
            cv2.putText(objeto_imagem.img,'SO ESQUERDA: GIRAR DIREITA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
            return GIRAR_DIREITA
    elif caso == NAO_HA_RETA:
        cv2.putText(objeto_imagem.img,'NAO HA RETA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
        return ANDAR
    else:
        horizontal = [0, objeto_imagem.topo_da_pista, objeto_imagem.largura, objeto_imagem.topo_da_pista]
        x1, _ = interscetion(horizontal, left)
        x2, _ = interscetion(horizontal, right)
        objeto_imagem.largura_pista = abs(x2 - x1)
        
        delta_x = (x1+x2)//2-objeto_imagem.largura//2
        objeto_imagem.img = cv2.line(objeto_imagem.img, (objeto_imagem.largura//2, 0), (objeto_imagem.largura//2, objeto_imagem.altura), (255, 0, 0), 2)
        objeto_imagem.img = cv2.line(objeto_imagem.img, (int(objeto_imagem.largura_pista//2*objeto_imagem.mult_largura_pista)+(x1+x2)//2, 0), (int(objeto_imagem.largura_pista//2*objeto_imagem.mult_largura_pista)+(x1+x2)//2, objeto_imagem.altura), (127, 127, 0), 2)
        objeto_imagem.img = cv2.line(objeto_imagem.img, (-int(objeto_imagem.largura_pista//2*objeto_imagem.mult_largura_pista)+(x1+x2)//2, 0), (-int(objeto_imagem.largura_pista//2*objeto_imagem.mult_largura_pista)+(x1+x2)//2, objeto_imagem.altura), (127, 127, 0), 2)
        objeto_imagem.img = cv2.circle(objeto_imagem.img, (x1, objeto_imagem.topo_da_pista), radius=10, color=(0, 255, 255), thickness=-1)
        objeto_imagem.img = cv2.circle(objeto_imagem.img, (x2, objeto_imagem.topo_da_pista), radius=10, color=(0, 255, 255), thickness=-1)
        objeto_imagem.img = cv2.circle(objeto_imagem.img, ((x1+x2)//2, objeto_imagem.topo_da_pista), radius=10, color=(0, 0, 255), thickness=-1)
        if objeto_imagem.largura_pista//2*objeto_imagem.mult_largura_pista > abs(delta_x):
            cv2.putText(objeto_imagem.img,'2 RETAS: ALINHADO', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
            return ANDAR
        elif delta_x > 0:
            cv2.putText(objeto_imagem.img,'2 RETAS: GIRAR DIREITA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
            return GIRAR_DIREITA
        else:
            cv2.putText(objeto_imagem.img,'2 RETAS: GIRAR ESQUERDA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
            return GIRAR_ESQUERDA

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
  