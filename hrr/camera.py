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

class RaspCamera(__Camera):
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