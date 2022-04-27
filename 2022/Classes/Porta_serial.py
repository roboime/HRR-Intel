import RPi.GPIO as GPIO
from constantes import *

class Classe_porta_serial():
    def __init__(self):
        ################################################ Configuracoes da Rasp ################################################
        
        channel = 18                                                                                            #porta utilizada
        GPIO.setmode(GPIO.BCM)          
        GPIO.setup(channel, GPIO.OUT)

        ################################################ Configuracoes da MyRio ################################################
        porta = "/dev/ttyAMA1"                                                                             #nao e a porta AMA0**
        baudrate_myrio = 230400                                                                         #deve igualar a da myrio
        self.serial_output = serial.Serial(porta,baudrate_myrio)                   # porta serial que faz comunicacao coma MyRio
        
        #self.Save_config(self)

    def Escrever_estado(self, state):
        self.serial_output.write(state)