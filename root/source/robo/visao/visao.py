import cv2

class Visao():
    ''' 
Classe relacionada a imagem obtida pela camera. Ao ser chamada, inverte a imagem e salva constantes relacionadas a imagem, como altura, largura e centro.
Possui o metodo mask, que retorna a mascara da imagem, passando o arquivo onde esta salvo os ranges da cor.
'''
    def __init__(self):
        self.imagem = Imagem()
    def checar_alinhamento_pista(self):
        left, right, case = imagem.bordas_laterais()
        horizontal = [0, imagem.topo_da_pista, imagem.largura, imagem.topo_da_pista]
        x1 = 0
        x2 = imagem.largura
        
        if case ==NAO_HA_RETA:
            return ANDAR
        elif case == HA_DUAS_RETAS:
            x1, _ = imagem.interscetion(horizontal, left)
            x2, _ = imagem.interscetion(horizontal, right)
        elif case == SO_ESQUERDA:
            x1, _ = imagem.interscetion(horizontal, left)
        elif case == SO_DIREITA:
            x2, _ = imagem.interscetion(horizontal, right)  

        largura_pista = abs(x2 - x1)
        mult_largura_pista = 0.3
        delta_x = (x1+x2)//2-imagem.largura//2
        #imagem.img = cv2.line(imagem.img, (imagem.largura//2, 0), (imagem.largura//2, imagem.altura), (255, 0, 0), 2)
        #imagem.img = cv2.line(imagem.img, (int(imagem.largura_pista//2*imagem.mult_largura_pista)+(x1+x2)//2, 0), (int(imagem.largura_pista//2*imagem.mult_largura_pista)+(x1+x2)//2, imagem.altura), (127, 127, 0), 2)
        #imagem.img = cv2.line(imagem.img, (-int(imagem.largura_pista//2*imagem.mult_largura_pista)+(x1+x2)//2, 0), (-int(imagem.largura_pista//2*imagem.mult_largura_pista)+(x1+x2)//2, imagem.altura), (127, 127, 0), 2)
        #imagem.img = cv2.circle(imagem.img, (x1, imagem.topo_da_pista), radius=10, color=(0, 255, 255), thickness=-1)
        #imagem.img = cv2.circle(imagem.img, (x2, imagem.topo_da_pista), radius=10, color=(0, 255, 255), thickness=-1)
        #imagem.img = cv2.circle(imagem.img, ((x1+x2)//2, imagem.topo_da_pista), radius=10, color=(0, 0, 255), thickness=-1)
        if largura_pista//2*mult_largura_pista > abs(delta_x):
            return ANDAR
        elif delta_x > 0:
            return GIRAR_DIREITA
        else:
            return GIRAR_ESQUERDA 