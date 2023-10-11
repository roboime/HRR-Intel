"""Modulo base do robo de corrida"""
from time import sleep
from alinhamento import Alinhamento_imu
from desvio import DesvioObstaculo
from estado import Estado
from serial_com import SerialMyrio
from imu6050 import Imu6050 
from visao import Classe_imagem
from sensor_distancia import SensorDistancia
from camera import RaspCamera

class Robo:
    """Classe base do robo de corrida"""
    def __init__(self, estado: Estado = Estado(),
                  imu: Imu6050 = Imu6050(), 
                  visao: Classe_imagem = Classe_imagem(), 
                  desvio: DesvioObstaculo = DesvioObstaculo(), 
                  sensor_distancia: SensorDistancia= SensorDistancia(),
                  camera: RaspCamera = RaspCamera(),
                  discovery: SerialMyrio = SerialMyrio()):
        """Inicializa com instancias das classes Estado, Visao, Imu e Alinhamento"""
        self.alinhamento: Alinhamento_imu = Alinhamento_imu(self)
        self.estado: Estado = estado
        self.imu: Imu6050 = imu
        self.visao: Classe_imagem = visao
        self.desvio: DesvioObstaculo = desvio
        self.sensor_distancia: SensorDistancia = sensor_distancia
        self.camera: RaspCamera = camera
        self.discovery: SerialMyrio = discovery
    def corrida(self):
        """Metodo base da corrida do robo"""
        self.discovery.escrever_estado("ANDAR")
        print("Mandou Andar \n")
        while True:
            sleep(20)
            self.alinhamento.verificar_alinhamento()
          


