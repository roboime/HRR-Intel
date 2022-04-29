import cv2

class Imagem():
    ''' 
Classe relacionada a imagem obtida pela camera. Ao ser chamada, inverte a imagem e salva constantes relacionadas a imagem, como altura, largura e centro.
Possui o metodo mask, que retorna a mascara da imagem, passando o arquivo onde esta salvo os ranges da cor.
'''
    def __init__(self):
        camera = Camera()
        img = cv2.imread(camera.path_atual)
        #img = np.array(img)

        img = cv2.rotate(img, cv2.ROTATE_180)
        cv2.imwrite("/home/pi/Pictures/imagem_girada.jpg", img)

        img.astype(np.uint8)

        (self.altura, self.largura) = img.shape[:2] 
        self.centro = ( (self.largura)//2, (self.altura)//2 )
        #M = cv2.getRotationMatrix2D(self.centro, 180, 1)
        #img = cv2.warpAffine(img, M, (self.largura, self.altura))

        self.img = img
        self.topo_da_pista = int(0.4*self.altura) #coordenada y do topo da pista
        self.meio_da_pista = 0 # coordenada x do meio da pista
        self.largura_pista = 0 # largura do final da pista na imagem
        self.mult_largura_pista = 0.7 #ate quanto da metade da largura da pista ainda eh atravessavel pelo robo

    def mask(self, ranges_file_path):
        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV) # converte a cor para hsv
        with open(ranges_file_path, "r") as f:
            lines = f.readlines()
            range = lines[0].split(",")
            lower = np.array([int(range[0]),int(range[1]),int(range[2])])  #range de cores em hsv para reconhecer as bordas
            upper = np.array([int(range[3]),int(range[4]),int(range[5])])
        mask = cv2.inRange(hsv, lower, upper)
        kernel = np.ones((5,5), np.uint8) 
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
        return mask
    