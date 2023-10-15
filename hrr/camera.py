from time import sleep, time
import os
import cv2 as cv
from estado import Estado
try:
    import picamera
except:
    print('picamera not imported due to ImportError')
import constantes_old as c

from abc import ABC, abstractmethod



class Camera(ABC):
    CONTRAST = 70
    WIDTH, HEIGHT = 1280, 720
    FRAMERATE = 30
    WARMUP_TIME = 2

    @abstractmethod
    def tirar_foto(self, name: str | None):
        pass

    @abstractmethod
    def parar(self):
        pass


class RaspCamera(Camera):
    def __init__(self):
        """
        aaaa
        """
        self.counter = 0

    def tirar_foto(self, name: str | None):
        """
        Tira uma foto e salva no diretório "images"
        """
        directory = "images"
        if name is None:
            name = "image" + str(self.counter) + ".jpg"
            self.counter += 1
        
        path = os.path.join(directory, name)


    def parar(self, estado: Estado):
        """
        Para de fotografar e salva as fotos em uma pasta
        """