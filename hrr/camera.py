from time import sleep, time
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
    def capture():
        pass

class RaspCamera(Camera):
    def __init__(self):
        '''
        aaaa
        '''

    def take_photo(self):
        '''
        Tira uma foto e salva em uma pasta
        '''

    def parar_fotografar(self, estado: Estado):
        '''
        Para de fotografar e salva as fotos em uma pasta
        '''