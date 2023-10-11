"""Modulo base do robo de corrida"""
from time import sleep
from desvio import DesvioObstaculo
from estado import Estado
from serial_com import SerialMyrio
from visao import Classe_imagem, checar_alinhamento_pista_v2
from sensor_distancia import SensorDistancia
from camera import RaspCamera
from time import sleep, time
import constantes as c

class Robo:
    """Classe base do robo de corrida"""
    def __init__(self, estado: Estado = Estado(),
                  sensor_distancia: SensorDistancia= SensorDistancia(),
                  camera: RaspCamera = RaspCamera(),
                  discovery: SerialMyrio = SerialMyrio()):
        """Inicializa com instancias das classes Estado, Visao, Imu e Alinhamento"""
         
        self.estado: Estado = estado
        self.desvio: DesvioObstaculo = DesvioObstaculo(self)
        self.sensor_distancia: SensorDistancia = sensor_distancia
        self.camera: RaspCamera = camera
        self.discovery: SerialMyrio = discovery
    def corrida(self):
        """Metodo base da corrida do robo"""

