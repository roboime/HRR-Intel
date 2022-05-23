"""Modulo que define a porta serial que faz coneccao com a MyRIO"""

import RPi.GPIO as GPIO
import serial
from .serial_base import SerialBase

class SerialMyrio(SerialBase):
    """Classe herdada da classe SeriaBase e define a porta serial que faz coneccao com a MyRIO"""
    def __init__(self):
        SerialBase.__init__(self)
        # Configuracoes da Rasp
        channel = 18 #porta utilizada
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(channel, GPIO.OUT)

        # Configuracoes da MyRio
        porta = "/dev/ttyAMA1" # nao e a porta AMA0**
        baudrate_myrio = 230400 # deve igualar a da myrio
        # porta serial que faz comunicacao com a MyRio
        self.serial_output = serial.Serial(porta,baudrate_myrio)

    def escrever_estado(self, state):
        """Metodo que envia o estado atual para a myrio por meio de comunicacao serial"""
        self.serial_output.write(self.states[state])
