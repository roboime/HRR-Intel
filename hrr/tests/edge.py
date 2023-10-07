import cv2
import numpy as np
import math
import os

IMG = None
IMG_WIDTH = 0
RIGHT = 1
LEFT = -1

class line():

    def __init__(self, segment):

        segment = segment.reshape(4)
        self.x1, self.y1, self.x2, self.y2 = segment

        side = (self.x1 + self.x2)/2 - IMG_WIDTH/2
        self.side = side / abs(side) # 1 para lado direito e -1 para lado esquerdo

        if self.x1 != self.x2:
            self.angCoef = (self.y2-self.y1)/(self.x2-self.x1)
            self.inc = math.atan(self.angCoef)
            self.linCoef = self.y1 - self.angCoef * self.x1
        else:
            self.linCoef = None
            self.angCoef = None
            self.inc = math.pi/2
    def get_y(self, x):
        return self.linCoef + self.angCoef * x


def white_mask():
    global IMG_WIDTH
    global IMG
    IMG = cv2.imread(os.path.join("input_imgs", "k.jpg"))
    IMG_WIDTH = IMG.shape[1]

    hsv = cv2.cvtColor(IMG, cv2.COLOR_BGR2HSV) # converte a cor para hsv
    lower = np.array([0,0,140])   #range de cores em hsv para reconhecer as bordas
    upper = np.array([255,255,255])
    mask = cv2.inRange(hsv, lower, upper)

    kernel = np.ones((5,5), np.uint8) 
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    cv2.imwrite('edge.png', mask)
    return mask

def edge():
    edges = cv2.Canny(white_mask(), 75, 150) # destaca as linhas da imagem convertida em preto e branco
    segments = cv2.HoughLinesP(edges, 1, np.pi/180, 20, maxLineGap=20, minLineLength=50) # obtem os pontos que formam os segmentos de reta das linhas
    if segments is None: return [], [], 0 #não achou nenhum segmento de reta
    lines = []
    for segment in segments:
        print(segment)
        l = line(segment) 
        lines.append(l)
    left_major = right_major = np.NINF
    left_edge = right_edge = None

    for l in lines:
        if l.angCoef is not None: # se não for inclinada de 90°
            if l.side*l.angCoef < 3.5 and l.side*l.angCoef > 2/7: #está dentro do range da inclinação
                r_intersect = l.get_y(IMG_WIDTH) # intersecção com a borda direita da imagem
                l_intersect = l.linCoef # intersecção com a borda esquerda da imagem

                if l.side == RIGHT and r_intersect > right_major:           #
                    right_major = r_intersect                               #
                    right_edge = l                                          #     a reta cuja intersecção com a borda lateral é
                if l.side == LEFT and l_intersect > left_major:             #     mais próxima da borda inferior será a borda lateral
                    left_major = l_intersect                                #     da pista
                    left_edge = l                                           #
    if left_edge is None and right_edge is None: return [], [], 0   # nenhuma das retas é borda da pista
    if left_edge is None:
        cv2.line(IMG, (right_edge.x1, right_edge.y1), (right_edge.x2, right_edge.y2), (255,0,255), 2)
    if right_edge is None:
        cv2.line(IMG, (left_edge.x1, left_edge.y1), (left_edge.x2, left_edge.y2), (255,0,255), 2)
    else:
        cv2.line(IMG, (left_edge.x1, left_edge.y1), (left_edge.x2, left_edge.y2), (255,0,255), 2)
        cv2.line(IMG, (right_edge.x1, right_edge.y1), (right_edge.x2, right_edge.y2), (255,0,255), 2)

    mp1 = ((left_edge.x1 + right_edge.x1)//2, (left_edge.y1 + right_edge.y1)//2)
    mp2 = ((left_edge.x2 + right_edge.x2)//2, (left_edge.y2 + right_edge.y2)//2)
    cv2.line(IMG, mp1, mp2, (255,0,255), 2)

edge()
cv2.imwrite("final.png", IMG)