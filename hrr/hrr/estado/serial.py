"""Modulo base para implementacao de classes para a comunicacao serial"""
try:
    import RPi.GPIO as GPIO
except ImportError:
    print('GPIO not imported due to ImportError')
import serial

PATH = './hrr/data/serial_teste/serial_teste.txt'

class Serialport():
    """Classe base para implementacao de classes para a comunicacao serial"""
    states = {
        "ANDAR" : "0",
        "GIRAR_ESQUERDA" : "1",
        "GIRAR_DIREITA" : "2",
        "PARAR" : "3",
        "SUBIR"  :  "6",
        "DESCER" : "7"
    }
    def escrever_estado(self, state):
        """Metodo que envia o estado atual por meio de comunicacao serial"""

class SerialTeste(Serialport):
    """Classe herdada da classe SeriaBase e define uma porta serial ficticia
    por meio do arquivo de saida no path indicado"""
    def __init__(self):
        """Herda o __init__ da Serialport e define o local do arquivo destino"""
        Serialport.__init__(self)
        self.output_path = PATH
    def escrever_estado(self, state):
        """Metodo que envia o estado atual para o arquivo destino,
        simulando uma comunicacao serial"""
        with open(self.output_path, 'a') as output:
            output.write(f'{state}\n')


class SerialMyrio(Serialport):
    """Classe herdada da classe SeriaBase e define a porta serial que faz coneccao com a MyRIO"""
    def __init__(self):
        Serialport.__init__(self)
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
