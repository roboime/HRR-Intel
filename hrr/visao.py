"""Modulo responsavel pela visao computacional no robo"""
#from source.robo.visao.camera.camera import Camera
import math
import numpy as np
import cv2
import constantes as c
import helpers as h
from imagem import Imagem
import picamera

class Visao():
    """Classe responsavel pela analise de imagens usando o opencv"""
    def __init__(self):
        """Inicia com uma instancia de Camera() e uma imagem. A imagem eh invertida e instanciada.
        Tambem sao salvos alguns atributos relacionados a imagem"""
        self.camera = picamera.PiCamera()
        self.camera.resolution = (1024,768)
        self.camera.start_preview()
        self.imagem = Imagem(self.camera.capture())
        self.camera.stop_preview()

        (self.altura, self.largura) = self.imagem.shape()
        self.centro = ( (self.largura)//2, (self.altura)//2)

        self.topo_pista = int(0.4*self.altura) #coordenada y do topo da pista
        self.meio_pista = 0 # coordenada x do meio da pista
        self.largura_pista = 0 # largura do final da pista na imagem
        self.mult_largura_pista = 0.3 # ate quanto da metade da largura da pista
                                      # ainda eh atravessavel pelo robo
        self.lines = []
        self.left_lines = []
        self.right_lines = []
        self.left = []
        self.right = []
        self.corner1 = 0
        self.corner2 = 0
    
    def atualizar_imagem(self):
        self.imagem.salvar()
        self.imagem.atualizar(self.camera.capture())

    def desenhar_alinhamento(self):
        """Desenha todos os pontos e retas usados na funcao decisao_alinhamento()"""
        
        self.imagem.desenhar_reta([self.largura//2, 0, self.largura//2, self.altura], (255, 0, 0))
        self.imagem.desenhar_reta([self.amplitude_pista+self.meio_pista, 0, self.amplitude_pista+self.meio_pista, self.altura], (127, 127, 0))
        self.imagem.desenhar_reta([-self.amplitude_pista+self.meio_pista, 0, -self.amplitude_pista+self.meio_pista, self.altura], (127, 127, 0))
        self.imagem.desenhar_circulo((self.corner1, self.topo_pista), (0, 255, 255))
        self.imagem.desenhar_circulo((self.corner2, self.topo_pista), (0, 255, 255))
        self.imagem.desenhar_circulo((self.meio_pista, self.topo_pista), (0, 0, 255))

    def desenhar_bordas(self):
        """Desenha todas as retas usadas na funcao bordas_laterais_pista()"""
        if len(self.lines) > 0:
            for line in self.lines:
                self.imagem.desenhar_reta(line.reshape(4), (0,127,255))
        if len(self.right_lines) > 0:
            for line in self.right_lines:
                self.imagem.desenhar_reta(line, (0,255,0))
        if len(self.left_lines) > 0:
            for line in self.left_lines:
                self.imagem.desenhar_reta(line, (0,127,0))
        self.imagem.desenhar_reta(self.left, (0,0,255))
        self.imagem.desenhar_reta(self.right, (0,0,255))

    def bordas_laterais_pista(self):
        """Acha todas as retas correspondentes as bordas laterais da pista.
        Caso nao ache alguma delas ela retorna uma reta vertical no lado esquerdo ou direito."""
        self.atualizar_imagem()
        mask = self.imagem.mask()
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
                if y_1 > self.topo_pista or y_2 > self.topo_pista:
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
        self.bordas_laterais_pista()
        horizontal = [0, self.topo_pista, self.largura, self.topo_pista]

        self.corner1, _ = h.intersection(horizontal, self.left)
        self.corner2, _ = h.intersection(horizontal, self.right)

        self.largura_pista = abs(self.corner2 - self.corner1)
        self.meio_pista = (self.corner1 + self.corner2)//2
        self.amplitude_pista = int(self.largura_pista//2*self.mult_largura_pista)
        delta_x = self.meio_pista - self.largura//2

        #self.desenhar_alinhamento()
        if self.amplitude_pista > abs(delta_x):
            return "ANDAR"
        elif delta_x > 0:
            return "GIRAR_DIREITA"
        else:
            return "GIRAR_ESQUERDA"
