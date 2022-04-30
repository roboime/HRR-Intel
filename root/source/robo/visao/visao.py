import cv2
from imagem import Imagem
from camera import Camera

class Visao():
    ''' 
Classe relacionada a imagem obtida pela camera. Ao ser chamada, inverte a imagem e salva constantes relacionadas a imagem, como altura, largura e centro.
Possui o metodo mask, que retorna a mascara da imagem, passando o arquivo onde esta salvo os ranges da cor.
'''
    def __init__(self):
        self.imagem = Imagem()
    def checar_alinhamento_pista(self):
        left, right, case = self.imagem.bordas_laterais()
        horizontal = [0, self.imagem.topo_da_pista, self.imagem.largura, self.imagem.topo_da_pista]
        x1 = 0
        x2 = self.imagem.largura
        
        if case ==NAO_HA_RETA:
            return ANDAR
        elif case == HA_DUAS_RETAS:
            x1, _ = self.imagem.interscetion(horizontal, left)
            x2, _ = self.imagem.interscetion(horizontal, right)
        elif case == SO_ESQUERDA:
            x1, _ = self.imagem.interscetion(horizontal, left)
        elif case == SO_DIREITA:
            x2, _ = self.imagem.interscetion(horizontal, right)  

        largura_pista = abs(x2 - x1)
        mult_largura_pista = 0.3
        delta_x = (x1+x2)//2-self.imagem.largura//2
        #self.imagem.img = cv2.line(self.imagem.img, (self.imagem.largura//2, 0), (self.imagem.largura//2, self.imagem.altura), (255, 0, 0), 2)
        #self.imagem.img = cv2.line(self.imagem.img, (int(self.imagem.largura_pista//2*self.imagem.mult_largura_pista)+(x1+x2)//2, 0), (int(self.imagem.largura_pista//2*self.imagem.mult_largura_pista)+(x1+x2)//2, self.imagem.altura), (127, 127, 0), 2)
        #self.imagem.img = cv2.line(self.imagem.img, (-int(self.imagem.largura_pista//2*self.imagem.mult_largura_pista)+(x1+x2)//2, 0), (-int(self.imagem.largura_pista//2*self.imagem.mult_largura_pista)+(x1+x2)//2, self.imagem.altura), (127, 127, 0), 2)
        #self.imagem.img = cv2.circle(self.imagem.img, (x1, self.imagem.topo_da_pista), radius=10, color=(0, 255, 255), thickness=-1)
        #self.imagem.img = cv2.circle(self.imagem.img, (x2, self.imagem.topo_da_pista), radius=10, color=(0, 255, 255), thickness=-1)
        #self.imagem.img = cv2.circle(self.imagem.img, ((x1+x2)//2, self.imagem.topo_da_pista), radius=10, color=(0, 0, 255), thickness=-1)
        if largura_pista//2*mult_largura_pista > abs(delta_x):
            return ANDAR
        elif delta_x > 0:
            return GIRAR_DIREITA
        else:
            return GIRAR_ESQUERDA 