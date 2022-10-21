import cv2
import numpy as np
import math

class Imagem():
    PATH_FILTROS = "./hrr/data/filtros_de_cor/ranges_preto.txt"
    PATH_SAVE = "./hrr/data/images/teste_visao/img.jpg"
    INTERATIONS = 2
    def __init__(self, img):
        self.atualizar(img)
        #M = cv2.getRotationMatriself.x_2D(self.centro, 180, 1)
        #img = cv2.warpAffine(img, M, (self.largura, self.altura))

    def atualizar(self, img):
        img = np.array(img)
        img.astype(np.uint8)
        img = cv2.rotate(img, cv2.ROTATE_180)
        cv2.imwrite('/home/pi/HRR-Intel/hrr/image.jpg', img)
    
    def shape(self):
        return self.img.shape[:2]

    def mask(self):
        """Recebe o arquivo de filtros de certa cor e cria uma mascara para a imagem"""
        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV) # converte a cor para hsv
        with open(self.PATH_FILTROS, "r") as file:
            lines = file.readlines()
            ranges = lines[0].split(",")
            #range de cores em hsv para reconhecer as bordas
            lower = np.array([int(ranges[0]),int(ranges[1]),int(ranges[2])])
            upper = np.array([int(ranges[3]),int(ranges[4]),int(ranges[5])])
        mask = cv2.inRange(hsv, lower, upper)
        kernel = np.ones((5,5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations = self.INTERATIONS)
        return mask

    def desenhar_reta(self, reta, cor):
        [x1, y1, x2, y2] = reta
        self.img = cv2.line(self.img,
            (x1, y1),
            (x2, y2),
            cor, 2)
    def desenhar_circulo(self, ponto, cor):
        self.img = cv2.circle(self.img,
            ponto,
            radius=10,
            color=cor,
            thickness=-1)
    def escrever_texto(self, text, ponto):
        self.img = cv2.putText(self.img, text, ponto, cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
    def salvar(self):
        cv2.imwrite(self.PATH_SAVE, self.img)
    def exibir(self):
        cv2.imshow('img', self.img)