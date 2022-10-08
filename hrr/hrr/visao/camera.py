from time import sleep, time
import os
import numpy as np
import cv2
import sys
try:
    import picamera
except:
    print('picamera not imported due to ImportError')
from . import constantes as c

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
        # print("Entra no _init_ da Classe_camera")
        cam = picamera.PiCamera(resolution=(
            c.WIDTH, c.HEIGHT), framerate=c.FRAMERATE, contrast=c.CONTRAST)
        self.cam = cam
        sleep(c.WARMUP_TIME)

    def capture(self):
        return self.capture_opencv()

    def capture_opencv(self):
        image = np.empty((c.HEIGHT * c.WIDTH * 3,), dtype=np.uint8)
        self.cam.capture(image, 'bgr')
        image = image.reshape((c.HEIGHT, c.WIDTH, 3))
        return image

    def capture_sequence(self, frames):
#        cam.start_preview()
        # Give the camera some warm-up time
 #       time.sleep(2)
        start = time()
        self.cam.capture_sequence([
            '../data/images/sequence/image%02d.jpg' % i
            for i in range(frames)
            ], use_video_port=True)
        finish = time()
        print('Captured %d frames at %.2ffps' % (
        frames,
        frames / (finish - start)))

    def take_photo(self):
        try:
            self.path_atual = "./tests/fotos_main/imagem_main" + \
                str(self.indice_atual) + ".jpg"
            # print(" foto tirada em " + self.path_atual)
            self.cam.capture(self.path_atual)
            self.indice_atual = (self.indice_atual + 1) % 10
            # print("Saindo do Take_photo()")
            return self.path_atual
        except KeyboardInterrupt: self.cam.stop_preview()

    def parar_fotografar(self, estado):
        atual = estado.Obter_estado_atual()
        estado.Trocar_estado("PARAR")
        img = self.Take_photo()
        estado.Trocar_estado(atual)
        return img
