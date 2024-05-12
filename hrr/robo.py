"""Modulo base do robo de corrida"""
from time import sleep, time
from typing import Self
from hrr.desvio import Desvio
from hrr.estado import Estado
from hrr.comm import *
from hrr.sensor_distancia import *
from hrr.camera import *
from hrr.alinhamento import *
from hrr.gyro import *
from hrr.exceptions import *
from hrr.controller import Controller
import hrr.constantes as c


class Robo:
    """Classe base do robo de corrida"""
    
    __slots__ = ['state', 'comm', 'camera', 'distance_sensor', 'gyro', 'controller', '_compiled']

    @staticmethod
    def build_instance() -> Self:
        return Robo(SerialMyrio(), RaspCamera(), SensorDistancia(), IMU())

    def __init__(self,
                  discovery: Serial,
                  camera: Camera,
                  sensor_distancia: SensorDistancia,
                  gyro: Gyro):
        """Inicializa com instancias das classes Estado, Visao, Imu e Alinhamento"""
         
        self.estado: Estado = Estado.PARADO
        self.discovery: Serial = discovery
        self.camera: Camera = camera
        self.sensor_distancia: SensorDistancia = sensor_distancia
        self.gyro: Gyro = gyro
        self._compiled = False

    def compile(self, use_ml: bool=False) -> Self:
        '''
            Método responsável por observar se o objeto robô possui o estado de hardware apropriado para o funcionamento. 
            Os possíveis estados são:


            Além disso, o método também é responsável por compilar o alinhamento do robô.
            Para mais detalhes, ler code report.
        '''
        
        self._compiled = True
        hardware = {
            'camera': self.camera,
            'sensor_distancia': self.sensor_distancia,
            'gyro': self.gyro,
            'comm': self.discovery
        }
        self.controller = Controller('ml' if use_ml else 'standard', hardware)
        return self

    def corrida(self) -> None:
        '''Método base da corrida do robo'''
        if not self._compiled:
            raise RobotCompileException('Robô não compilado')
        while True:
            self.estado = self.controller.proximo_estado()
            self.discovery.escrever_estado(self.estado)
            sleep(0.1)