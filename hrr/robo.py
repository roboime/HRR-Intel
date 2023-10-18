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
import hrr.constantes as c

class Robo:
    """Classe base do robo de corrida"""
    def __init__(self, estado: Estado,
                  discovery: Serial,
                  camera: Camera,
                  sensor_distancia: SensorDistancia,
                  gyro: Gyro):
        """Inicializa com instancias das classes Estado, Visao, Imu e Alinhamento"""
         
        self.estado: Estado = estado
        self.discovery: Serial = discovery
        self.camera: Camera = camera
        self.sensor_distancia: SensorDistancia = sensor_distancia
        self.gyro: Gyro = gyro
        self.desvio: Desvio = Desvio(self)

    def add_alinhamento(self, alinhamento: Alinhamento):
        self.alinhamento = alinhamento
        
    def corrida(self):
        """Metodo base da corrida do robo"""
        # while True:
        #     self.estado = self.estado.atualizar_estado(self)
        #     self.estado.enviar_estado(self.discovery)
        #     self.estado = self.estado.trocar_estado(self)
        #     self.estado.enviar_estado(self.discovery)
        #     sleep(0.1)

class FactoryRobo:
    def __init__(self, *, alinhar_com_gyro: bool=True, alinhar_com_camera: bool=True) -> None:
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
        
        if self.gyro and self.camera and alinhar_com_camera and alinhar_com_gyro:
            self.alinhamento = AlinhamentoCameraIMU
        elif self.gyro and alinhar_com_gyro and not alinhar_com_camera:
            self.alinhamento = AlinhamentoIMU
        elif self.camera and alinhar_com_camera and not alinhar_com_gyro:
            self.alinhamento = AlinhamentoCamera
        else:
            raise RobotConfigException('Configuração inválida')
        self.estado = Estado

    def __str__(self) -> str:
        return f'''Default specs do robo:
        Serial: {self.serial}
        Camera: {self.camera}
        Sensor de distancia: {self.sensor_distancia}
        IMU: {self.gyro}
        Alinhamento: {self.alinhamento}
        Estado: {self.estado}
        '''
    
    def make_robo(self, **kwargs) -> Robo:
        robo: Robo | None = None
        if kwargs is None:
            robo = Robo(self.estado(), self.serial(), self.camera(), self.sensor_distancia(), self.gyro())
        else:
            robo = Robo(kwargs['estado'](), kwargs['serial'](), kwargs['camera'](), kwargs['sensor_distancia'](), kwargs['gyro']())
        alinhamento = self.alinhamento(robo)
        robo.add_alinhamento(alinhamento)
        return robo