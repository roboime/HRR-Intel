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
    def take_photo(self):
        pass

    @abstractmethod
    def stop(self):
        pass

class RaspCamera(Camera):
    def __init__(self):
        """
        aaaa
        """
        self.counter = 0

    def take_photo(self, name: str | None):
        """
        Tira uma foto e salva no diretório "images"
        """
        directory = "images"
        if name is None:
            name = "image" + str(self.counter) + ".jpg"
            self.counter += 1
        
        path = os.path.join(directory, name)


    def stop(self, estado: Estado):
        """
        Para de fotografar e salva as fotos em uma pasta
        """