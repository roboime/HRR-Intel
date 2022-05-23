"""Modulo responsavel pela visao computacional no robo"""
#from source.robo.visao.camera.camera import Camera
import math
import numpy as np
import cv2
from . import constantes as c
from . import helpers as h


class Visao():
    """Classe responsavel pela analise de imagens usando o opencv"""
    def __init__(self, img, camera):
        """Inicia com uma instancia de Camera() e uma imagem. A imagem eh invertida e instanciada.
        Tambem sao salvos alguns atributos relacionados a imagem"""
        self.camera = camera

        #img = np.array(img)
        img = cv2.rotate(img, cv2.ROTATE_180)
        #cv2.imwrite("/home/pi/Pictures/img.jpg", img)
        img.astype(np.uint8)
        self.img = img

        (self.altura, self.largura) = img.shape[:2]
        self.centro = ( (self.largura)//2, (self.altura)//2 )
        #M = cv2.getRotationMatriself.x_2D(self.centro, 180, 1)
        #img = cv2.warpAffine(img, M, (self.largura, self.altura))

        self.topo_da_pista = int(0.4*self.altura) #coordenada y do topo da pista
        self.meio_da_pista = 0 # coordenada x do meio da pista
        self.largura_pista = 0 # largura do final da pista na imagem
        self.mult_largura_pista = 0.7 # ate quanto da metade da largura da pista
                                      # ainda eh atravessavel pelo robo
        self.lines = []
        self.left_lines = []
        self.right_lines = []
        self.left = []
        self.right = []
        self.corner1 = 0
        self.corner2 = 0

    @classmethod
    def from_camera(cls, camera):
        """Inicializa o objeto instanciando a camera com uma foto tirada por ela"""
        return cls(camera.capture_opencv(), camera)

    @classmethod
    def from_path(cls, path):
        """Inicializa o objeto sem a camera e com uma imagem salva em algum path"""
        return cls(cv2.imread(path), None)

    def mask(self, ranges_file_path):
        """Recebe o arquivo de filtros de certa cor e cria uma mascara para a imagem"""
        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV) # converte a cor para hsv
        with open(ranges_file_path, "r") as file:
            lines = file.readlines()
            ranges = lines[0].split(",")
            #range de cores em hsv para reconhecer as bordas
            lower = np.array([int(ranges[0]),int(ranges[1]),int(ranges[2])])
            upper = np.array([int(ranges[3]),int(ranges[4]),int(ranges[5])])
        mask = cv2.inRange(hsv, lower, upper)
        kernel = np.ones((5,5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations = c.INTERATIONS)
        return mask

    def desenhar_alinhamento(self):
        """Desenha todos os pontos e retas usados na funcao decisao_alinhamento()"""
        self.img = cv2.line(self.img,
            (self.largura//2, 0),
            (self.largura//2, self.altura),
            (255, 0, 0), 2)
        self.img = cv2.line(self.img,
            (int(self.largura_pista//2*self.mult_largura_pista)+
                (self.corner1+self.corner2)//2, 0),
            (int(self.largura_pista//2*self.mult_largura_pista)+
                (self.corner1+self.corner2)//2, self.altura),
            (127, 127, 0), 2)
        self.img = cv2.line(self.img,
            (-int(self.largura_pista//2*self.mult_largura_pista)+
                (self.corner1+self.corner2)//2, 0),
            (-int(self.largura_pista//2*self.mult_largura_pista)+
                (self.corner1+self.corner2)//2, self.altura),
            (127, 127, 0), 2)
        self.img = cv2.circle(self.img,
            (self.corner1, self.topo_da_pista),
            radius=10,
            color=(0, 255, 255),
            thickness=-1)
        self.img = cv2.circle(self.img,
            (self.corner2,
            self.topo_da_pista),
            radius=10,
            color=(0, 255, 255),
            thickness=-1)
        self.img = cv2.circle(self.img,
            ((self.corner1+self.corner2)//2,
            self.topo_da_pista),
            radius=10,
            color=(0, 0, 255),
            thickness=-1)

    def desenhar_bordas(self):
        """Desenha todas as retas usadas na funcao bordas_laterais_da_pista()"""
        if len(self.lines) > 0:
            for line in self.lines:
                x_1, y_1, x_2, y_2 = line.reshape(4)
                cv2.line(self.img, (x_1,y_1), (x_2,y_2), (0,127,255), 2)
        if len(self.right_lines) > 0:
            for line in self.right_lines:
                x_1, y_1, x_2, y_2 = line
                cv2.line(self.img, (x_1,y_1), (x_2,y_2), (0,255,0), 2)
        if len(self.left_lines) > 0:
            for line in self.left_lines:
                x_1, y_1, x_2, y_2 = line
                cv2.line(self.img, (x_1,y_1), (x_2,y_2), (0,127,0), 2)
        [x_1, y_1, x_2, y_2] = self.right
        cv2.line(self.img, (x_1,y_1), (x_2,y_2), (0,0,255), 2)
        [x_1, y_1, x_2, y_2] = self.left
        cv2.line(self.img, (x_1,y_1), (x_2,y_2), (0,0,255), 2)

    def bordas_laterais_da_pista(self):
        """Acha todas as retas correspondentes as bordas laterais da pista.
        Caso não ache alguma delas ela retorna uma reta vertical no lado esquerdo ou direito."""
        if self.camera is not None:
            self.img = self.camera.capture_opencv()
        mask = self.mask("./data/filtros_de_cor/ranges_preto.txt")
        edges = cv2.Canny(mask,
            threshold1= c.THRESHOLD1,
            threshold2= c.THRESHOLD2,
            apertureSize= c.APERTURE_SIZE)
        lines = cv2.HoughLinesP(edges,
            rho= c.RHO,
            theta= c.THETA,
            threshold= c.THRESHOLD,
            minLineLength = c.MINLINELENGTH,
            maxLineGap = c.MAXLINEGAP)
        if lines is None:
            self.lines = []
        else:
            self.lines = lines

        self.left_lines = []
        self.right_lines =[]
        if len(self.lines) > 0:
            for line in self.lines:
                line = line.reshape(4)
                x_1, y_1, x_2, y_2 = line
                desvio_maximo = np.pi/180*c.RANGE_INCLINACAO
                if y_1 > self.topo_da_pista or y_2 > self.topo_da_pista:
                    if (math.atan(1)-desvio_maximo/2 <
                    math.atan(h.coef_angular(line)) <
                    math.atan(1)+desvio_maximo/2):
                        self.right_lines.append([x_1, y_1, x_2, y_2])
                    if (math.atan(-1)-desvio_maximo/2 <
                    math.atan(h.coef_angular(line)) <
                    math.atan(-1)+desvio_maximo/2):
                        self.left_lines.append([x_1, y_1, x_2, y_2])

        self.left = vertical_esquerda = [0, 0, 0, self.altura]
        self.right = vertical_direita = [self.largura, 0, self.largura, self.altura]

        if len(self.right_lines) != 0:
            y_max = 0
            self.right = self.right_lines[0]
            for line in self.right_lines:
                _, y_coordinate = h.intersection(line, vertical_direita)
                if y_coordinate > y_max:
                    y_max = y_coordinate
                    self.right = line

        if len(self.left_lines) != 0:
            y_max = 0
            self.left = self.left_lines[0]
            for line in self.left_lines:
                _, y_coordinate = h.intersection(line, vertical_esquerda)
                if y_coordinate > y_max:
                    y_max = y_coordinate
                    self.left = line

    def borda_inferior_obstaculo(self):
        """Identifica a borda laranja mais baixa e traca o ponto medio dela, retornando-o.
        Usada na decisao desvio
        (Implementar)"""

    def decisao_desvio_obstaculo(self):
        """Decide para onde virar quando encontra um obstaculo.
        Recebe somente a camera. Usado apenas no loop de obstaculo.
        (Implementar)"""

    def decisao_alinhamento(self):
        """verifica o alinhamento com a pista por meio da imagem.
        Retorna a decisao "ANDAR", "GIRAR_ESQUERDA" ou "GIRAR_DIREITA".
        """
        self.bordas_laterais_da_pista()
        horizontal = [0, self.topo_da_pista, self.largura, self.topo_da_pista]

        self.corner1, _ = h.intersection(horizontal, self.left)
        self.corner2, _ = h.intersection(horizontal, self.right)

        largura_pista = abs(self.corner2 - self.corner1)
        mult_largura_pista = 0.3
        delta_x = (self.corner1 + self.corner2)//2-self.largura//2

        if largura_pista//2*mult_largura_pista > abs(delta_x):
            return "ANDAR"
        elif delta_x > 0:
            return "GIRAR_DIREITA"
        else:
            return "GIRAR_ESQUERDA"
