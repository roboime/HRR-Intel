from time import sleep, time
import os
import cv2 as cv
from estado import Estado
try:
    import picamera
except:
    print('picamera not imported due to ImportError')
import hrr.constantes as c

from abc import ABC, abstractmethod
from hrr.constantes import WIDTH, HEIGHT, FRAMERATE, WARMUP_TIME, CONTRAST


class Camera(ABC):
    CONTRAST = CONTRAST
    WIDTH, HEIGHT = WIDTH, HEIGHT
    FRAMERATE = FRAMERATE
    WARMUP_TIME = WARMUP_TIME

    @abstractmethod
    def tirar_foto(self, name: str | None):
        pass

    @abstractmethod
    def parar(self):
        pass


class RaspCamera(Camera):
    def __init__(self, dir: str="images"):
        self.counter = 0
        self.path = os.path.join(os.getcwd(), dir)
        cam = picamera.PiCamera(resolution=(
            c.WIDTH, c.HEIGHT), framerate=c.FRAMERATE, contrast=c.CONTRAST)
        self.cam = cam
        sleep(c.WARMUP_TIME)

    def tirar_foto(self, name: str | None=None):
        """
        Tira uma foto e salva no diretório "images"
        """
        if name is None:
            name = "image" + str(self.counter) + ".jpg"
            self.counter += 1
        
        path = os.path.join(self.path, name)
        try:
            self.cam.capture(path)
            return path
        except KeyboardInterrupt: self.cam.stop_preview()


    def parar(self, estado: Estado):
        """
        Para de fotografar e salva as fotos em uma pasta
        """
        atual = estado.atual
        estado.trocar_estado("PARAR")
        img = self.tirar_foto()
        estado.trocar_estado(atual)
        return img



# import numpy as np

# import sys

# #sys.path.append('./hrr/data/images/fotos/')

# class RaspCamera(__Camera):
#     def __init__(self):
#         # print("Entra no _init_ da Classe_camera")
#         cam = picamera.PiCamera(resolution=(
#             c.WIDTH, c.HEIGHT), framerate=c.FRAMERATE, contrast=c.CONTRAST)
#         self.cam = cam
#         sleep(c.WARMUP_TIME)

#     def capture(self):
#         return self.capture_opencv()

#     def capture_opencv(self):
#         image = np.empty((c.HEIGHT * c.WIDTH * 3,), dtype=np.uint8)
#         self.cam.capture(image, 'bgr')
#         image = image.reshape((c.HEIGHT, c.WIDTH, 3))
#         return image

#     def capture_sequence(self, frames):
# #        cam.start_preview()
#         # Give the camera some warm-up time
#  #       time.sleep(2)
#         start = time()
#         self.cam.capture_sequence([
#             '../data/images/sequence/image%02d.jpg' % i
#             for i in range(frames)
#             ], use_video_port=True)
#         finish = time()
#         print('Captured %d frames at %.2ffps' % (
#         frames,
#         frames / (finish - start)))