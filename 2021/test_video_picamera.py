from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
from funcoes import checar_alinhamento_pista_v2


width = 640
height = 480

class Classe_imagem():
    def __init__(self, img):
        self.cont = 0
        #print("Entrando no _init_ do Classe_imagem()")
        #img = cv2.imread(path)
        #img = np.array(img)

        #img = cv2.rotate(img, cv2.ROTATE_180)

        img.astype(np.uint8)

        (self.altura, self.largura) = img.shape[:2] 
        self.centro = ( (self.largura)/2, (self.altura)/2 )

        #M = cv2.getRotationMatrix2D(self.centro, 180, 1)

        #print("Altura: {}  Largura: {}".format(self.altura,self.largura))

        #img = cv2.warpAffine(img, M, (self.largura, self.altura))

        #print("SAIMO DO WARPAFFINE")
        self.img = img
        #self.topo_da_pista = int(0.0*self.altura) #coordenada y do topo da pista
        self.topo_da_pista = (self.altura)//2 
        self.meio_da_pista = 0 # coordenada x do meio da pista
        self.largura_pista = 0 # largura do final da pista na imagem
        self.mult_largura_pista = 0.7 #ate quanto da metade da largura da pista ainda eh atravessavel pelo robo
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
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        return mask


if __name__ == "__main__":

    img_array = []

    camera = PiCamera()
    camera.resolution = (width, height)
    camera.framerate = 24
    size=(640, 480)
    rawCapture = PiRGBArray(camera, size)

    # allow the camera to warmup
    time.sleep(0.1)
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        frame = frame.array

        #print(sla)
        image = np.zeros(frame.shape, np.uint8)
        smaller_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        obj = Classe_imagem(cv2.resize(frame, (0, 0), fx=0.5, fy=0.5))
        mask_img = obj.mask('./ranges_preto.txt')
        mask_img2 = obj.mask('./ranges_laranja.txt')
        _ = checar_alinhamento_pista_v2(obj)
        for i in range(mask_img.shape[0]):
            for j in range(mask_img.shape[1]):
                image[i][j][:3] = mask_img[i][j]
        for i in range(mask_img2.shape[0]):
            for j in range(mask_img2.shape[1]):
                image[i][j+mask_img2.shape[1]][:3] = mask_img2[i][j]
        image[height//2:, :width//2] = smaller_frame
        image[height//2:, width//2:] = obj.img
        
        img_array.append(image)
        cv2.imshow('frame', image)
        rawCapture.truncate(0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    out = cv2.VideoWriter('project.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

    cv2.destroyAllWindows()

