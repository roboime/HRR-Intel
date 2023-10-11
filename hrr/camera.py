from time import sleep, time
import os
import numpy as np
import cv2
from estado import Estado
import sys
try:
    import picamera
except:
    print('picamera not imported due to ImportError')
import constantes as c

#sys.path.append('./hrr/data/images/fotos/')

class __Camera():
    CONTRAST = 70
    WIDTH, HEIGHT = 1280, 720
    FRAMERATE = 30
    WARMUP_TIME = 2
    def capture():
        pass

class Teste(__Camera):
    def __init__(self):
        pass
    def capture(self):
        print('captured')
        return cv2.imread('./hrr/data/images/fotos/imagem_teste_checar_alinhamento_3.jpg')

class RaspCamera(__Camera):
    def __init__(self):
        self.camera = picamera.PiCamera()
        self.intervalo_foto = 0.25
        self.indice_atual = 0
        self.path_pasta = os.path.dirname(os.path.abspath(__file__))
        self.path_atual = self.path_pasta + "1.jpg"

    def Take_photo(self):
        self.camera.start_preview()
        self.camera.contrast = self.CONTRAST
        time.sleep(self.intervalo_foto)
        try:
            self.path_atual = "./tests/fotos_main/imagem_main" + str(self.indice_atual) + ".jpg"
            print(" foto tirada em " + self.path_atual)
            self.camera.capture(self.path_atual)
            self.camera.stop_preview()
            self.indice_atual = (self.indice_atual + 1) % 10
            print("Saindo do Take_photo()")
            return self.path_atual
        except KeyboardInterrupt: self.camera.stop_preview()


    def parar_fotografar(self, estado: Estado):
        atual = estado.obter_estado_atual()
        estado.trocar_estado("PARAR")
        img = self.Take_photo()
        estado.trocar_estado(atual)
        return img
