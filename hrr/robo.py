"""Modulo base do robo de corrida"""
from time import sleep
from desvio import Desvio
from estado import *
from serial_com import *
from sensor_distancia import *
from camera import *
from alinhamento import *
from gyro import *
from time import sleep, time
import constantes_old as c

class Robo:
    """Classe base do robo de corrida"""
    def __init__(self, estado: Estado,
                  discovery: Serial,
                  camera: Camera,
                  sensor_distancia: SensorDistancia,
                  gyro: Gyro,
                  alinhamento: Alinhamento):
        """Inicializa com instancias das classes Estado, Visao, Imu e Alinhamento"""
         
        self.estado: Estado = estado
        self.discovery: SerialMyrio = discovery
        self.camera: Camera = camera
        self.sensor_distancia: SensorDistancia = sensor_distancia
        self.gyro: Gyro = gyro
        self.alinhamento: Alinhamento = alinhamento
        self.desvio: Desvio = Desvio(self)

    def corrida(self):
        """Metodo base da corrida do robo"""

class FactoryRobo:
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return " "
    
    def make_robo(self) -> Robo:    
        pass