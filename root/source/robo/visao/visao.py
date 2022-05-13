from source.robo.visao.camera.camera import Camera
import cv2
import source.robo.visao.constantes as c
import numpy as np
import math
import source.robo.visao.helpers as h
class Visao():
    ''' 
    Classe relacionada a imagem obtida pela camera. Ao ser chamada, inverte a imagem e salva constantes relacionadas a imagem, como altura, largura e centro.
    Possui o metodo mask, que retorna a mascara da imagem, passando o arquivo onde esta salvo os ranges da cor.
    '''
    def __init__(self, img, camera):
        self.camera = camera
        
        #img = np.array(img)
        img = cv2.rotate(img, cv2.ROTATE_180)
        #cv2.imwrite("/home/pi/Pictures/img.jpg", img)
        img.astype(np.uint8)
        self.img = img

        (self.altura, self.largura) = img.shape[:2] 
        self.centro = ( (self.largura)//2, (self.altura)//2 )
        #M = cv2.getRotationMatriself.x2D(self.centro, 180, 1)
        #img = cv2.warpAffine(img, M, (self.largura, self.altura))

        self.topo_da_pista = int(0.4*self.altura) #coordenada y do topo da pista
        self.meio_da_pista = 0 # coordenada x do meio da pista
        self.largura_pista = 0 # largura do final da pista na imagem
        self.mult_largura_pista = 0.7 #ate quanto da metade da largura da pista ainda eh atravessavel pelo robo
    @classmethod
    def from_camera(cls):
        camera = Camera()
        return cls(camera.capture_opencv(), camera)

    @classmethod
    def from_path(cls, path):
        return cls(cv2.imread(path), None)

    def mask(self, ranges_file_path):
        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV) # converte a cor para hsv
        with open(ranges_file_path, "r") as f:
            lines = f.readlines()
            range = lines[0].split(",")
            lower = np.array([int(range[0]),int(range[1]),int(range[2])])  #range de cores em hsv para reconhecer as bordas
            upper = np.array([int(range[3]),int(range[4]),int(range[5])])
        mask = cv2.inRange(hsv, lower, upper)
        kernel = np.ones((5,5), np.uint8) 
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations = c.INTERATIONS)
        return mask
    
    def desenhar_alinhamento(self):
        self.img = cv2.line(self.img, (self.largura//2, 0), (self.largura//2, self.altura), (255, 0, 0), 2)
        self.img = cv2.line(self.img, (int(self.largura_pista//2*self.mult_largura_pista)+(self.x1+self.x2)//2, 0), (int(self.largura_pista//2*self.mult_largura_pista)+(self.x1+self.x2)//2, self.altura), (127, 127, 0), 2)
        self.img = cv2.line(self.img, (-int(self.largura_pista//2*self.mult_largura_pista)+(self.x1+self.x2)//2, 0), (-int(self.largura_pista//2*self.mult_largura_pista)+(self.x1+self.x2)//2, self.altura), (127, 127, 0), 2)
        self.img = cv2.circle(self.img, (self.x1, self.topo_da_pista), radius=10, color=(0, 255, 255), thickness=-1)
        self.img = cv2.circle(self.img, (self.x2, self.topo_da_pista), radius=10, color=(0, 255, 255), thickness=-1)
        self.img = cv2.circle(self.img, ((self.x1+self.x2)//2, self.topo_da_pista), radius=10, color=(0, 0, 255), thickness=-1)
    
    def desenhar_bordas(self,lines, right, left, right_lines, left_lines):
        for line in lines:
            x1,y1,x2,y2 = line.reshape(4)
            cv2.line(self.img, (x1,y1), (x2,y2), (0,127,255), 2)
        for line in right_lines:
            x1,y1,x2,y2 = line
            cv2.line(self.img, (x1,y1), (x2,y2), (0,255,0), 2)
        for line in left_lines:
            x1,y1,x2,y2 = line
            cv2.line(self.img, (x1,y1), (x2,y2), (0,127,0), 2)
        [x1, y1, x2, y2] = right
        cv2.line(self.img, (x1,y1), (x2,y2), (0,0,255), 2)
        [x1, y1, x2, y2] = left
        cv2.line(self.img, (x1,y1), (x2,y2), (0,0,255), 2)
        
    def bordas_laterais(self):
        if self.camera is not None: self.img = self.camera.capture_opencv()
        mask = self.mask("./data/filtros_de_cor/ranges_preto.txt")
        edges = cv2.Canny(mask, 50, 150, apertureSize=3)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold = c.THRESHOLD, minLineLength = c.MINLINELENGTH, maxLineGap = c.MAXLINEGAP)
        left_lines = []
        right_lines =[]
        if lines is not None:
            for line in lines:
                line = line.reshape(4)
                x1,y1,x2,y2 = line                
                desvio_maximo = np.pi/180*c.RANGE_INCLINACAO
                if y1>self.topo_da_pista or y2>self.topo_da_pista:
                    if math.atan(1)-desvio_maximo/2 < math.atan(h.coef_angular(line)) < math.atan(1)+desvio_maximo/2:
                        right_lines.append([x1,y1,x2,y2])
                    if math.atan(-1)-desvio_maximo/2 < math.atan(h.coef_angular(line)) < math.atan(-1)+desvio_maximo/2:
                        left_lines.append([x1,y1,x2,y2])
                        
        left = vertical_esquerda = [0,0,0,self.altura]
        right = vertical_direita = [self.largura,0,self.largura,self.altura]

        if(len(right_lines) != 0):
            y_max = 0
            right = right_lines[0]
            for line in right_lines:
                _,y = h.intersection(line, vertical_direita)
                if y > y_max:
                    y_max = y
                    right = line
            
        if(len(left_lines) != 0):
            y_max = 0
            left = left_lines[0]
            for line in left_lines:
                _,y = h.intersection(line, vertical_esquerda)
                if y > y_max:
                    y_max = y
                    left = line
        self.desenhar_bordas(lines, right, left, right_lines, left_lines)
        return left, right
    
    def decisao_alinhamento(self):
        left, right = self.bordas_laterais()
        horizontal = [0, self.topo_da_pista, self.largura, self.topo_da_pista]
        
        self.x1, _ = h.intersection(horizontal, left)
        self.x2, _ = h.intersection(horizontal, right)

        largura_pista = abs(self.x2 - self.x1)
        mult_largura_pista = 0.3
        delta_x = (self.x1+self.x2)//2-self.largura//2
        self.desenhar_alinhamento()
        if largura_pista//2*mult_largura_pista > abs(delta_x):
            return "ANDAR"
        elif delta_x > 0:
            return "GIRAR_DIREITA"
        else:
            return "GIRAR_ESQUERDA"
        