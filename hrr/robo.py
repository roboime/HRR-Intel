"""Modulo base do robo de corrida"""
from time import sleep
from alinhamento import Alinhamento_imu
from desvio import DesvioObstaculo
from estado import Estado
from serial_com import SerialMyrio
from imu6050 import Imu6050 
from visao import Visao
from sensor_distancia import SensorDistancia


class Robo:
    """Classe base do robo de corrida"""
    def __init__(self, estado = Estado, imu = Imu6050, visao = Visao, alinhamento = Alinhamento_imu,
        desvio= DesvioObstaculo, sensor_distancia= SensorDistancia):
        """Inicializa com instancias das classes Estado, Visao, Imu e Alinhamento"""
        self.estado = estado
        self.imu = imu
        self.visao = visao
        self.alinhamento = alinhamento
        self.desvio = desvio
        self.sensor_distancia = sensor_distancia
    def corrida(self):
        """Metodo base da corrida do robo"""
        x = SerialMyrio()
        a = Alinhamento_imu()
        
        while True:
            x.escrever_estado("ANDAR")
            print("Mandou Andar \n")
            a.verificar_alinhamento()
          #  if self.desvio is not None:
           #     d = DesvioObstaculo()
            #    d.verificar_desvio()


