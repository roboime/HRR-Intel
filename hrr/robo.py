"""Modulo base do robo de corrida"""
from time import sleep
from desvio import Desvio
from estado import *
from serial_com import *
from sensor_distancia import *
from camera import *
from alinhamento import *
from gyro import *
from exceptions import *
from time import sleep, time
import constantes_old as c

class Robo:
    """Classe base do robo de corrida"""
    def __init__(self, estado: Estado,
                  discovery: Serial,
                  camera: Camera,
                  sensor_distancia: SensorDistancia,
                  gyro: Gyro):
        """Inicializa com instancias das classes Estado, Visao, Imu e Alinhamento"""
         
        self.estado: Estado = estado
        self.discovery: SerialMyrio = discovery
        self.camera: Camera = camera
        self.sensor_distancia: SensorDistancia = sensor_distancia
        self.gyro: Gyro = gyro
        self.desvio: Desvio = Desvio(self)

    def add_alinhamento(self, alinhamento: Alinhamento):
        self.alinhamento = alinhamento
        
    def corrida(self):
        """Metodo base da corrida do robo"""

class FactoryRobo:
    def __init__(self) -> None:
        try:
            SerialMyrio()
            self.serial = SerialMyrio
        except MyrioNotFoundException:
            self.serial = None
        try:
            IMU()
            self.gyro = IMU
        except IMUNotFoundException:
            self.gyro = None
        try:
            RaspCamera()
            self.camera = RaspCamera
        except CameraNotFoundException:
            self.camera = None
        try:
            SensorDistancia()
            self.sensor_distancia = SensorDistancia
        except SensorDistanciaNotFoundException:
            self.sensor_distancia = None
        
        if self.gyro and self.camera:
            self.alinhamento = AlinhamentoCameraIMU
        elif self.gyro:
            self.alinhamento = AlinhamentoIMU
        else:
            self.alinhamento = AlinhamentoCamera
        
        self.estado = Estado

    def __str__(self) -> str:
        return f'''Specs do robo:
        Serial: {self.serial}
        Camera: {self.camera}
        Sensor de distancia: {self.sensor_distancia}
        IMU: {self.gyro}
        Alinhamento: {self.alinhamento}
        Estado: {self.estado}
        '''
    
    def make_robo(self) -> Robo:    
        robo = Robo(self.estado, self.serial, self.camera, self.sensor_distancia, self.gyro)
        alinhamento = self.alinhamento(robo)
        robo.add_alinhamento(alinhamento)
        return robo