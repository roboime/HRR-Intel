"""Modulo base do robo de corrida"""
from time import sleep
from desvio import DesvioObstaculo
from estado import Estado
from serial_com import SerialMyrio
from sensor_distancia import SensorDistancia
from camera import RaspCamera
from alinhamento import *
from imu import IMU
from time import sleep, time
import constantes_old as c

class Robo:
    """Classe base do robo de corrida"""
    def __init__(self, estado: Estado,
                  discovery: SerialMyrio):
        """Inicializa com instancias das classes Estado, Visao, Imu e Alinhamento"""
         
        self.estado: Estado = estado
        self.desvio: DesvioObstaculo = DesvioObstaculo(self)
        self.discovery: SerialMyrio = discovery
        try:
            self.camera: RaspCamera = RaspCamera()
        except Exception as e:
            self.camera = None
            print(e)
            print('picamera not imported due to ImportError')
        try:
            self.sensor_distancia: SensorDistancia = SensorDistancia()
        except Exception as e:
            self.sensor_distancia = None
            print(e)
            print('picamera not imported due to ImportError')
        try:
            self.gyro: IMU = IMU()
        except Exception as e:
            self.gyro = None
            print(e)
            print('picamera not imported due to ImportError')

        if self.camera and self.sensor_distancia and self.gyro:
            self.alinhamento = AlinhamentoCameraIMU()
        elif self.camera and self.sensor_distancia:
            self.alinhamento = AlinhamentoCamera()
        elif self.gyro:
            self.alinhamento = AlinhamentoIMU()
        else:
            print("aaaa")

    def corrida(self):
        """Metodo base da corrida do robo"""

