from robo import Robo
from alinhamento import Alinhamento_imu
from desvio import DesvioObstaculo
from estado import Estado
from serial_com import SerialMyrio
from imu6050 import Imu6050 
from visao import Visao
from sensor_distancia import SensorDistancia

class CriarRobo:
    def __init__(self, robo = Robo(estado = Estado, imu = Imu6050, visao = Visao, alinhamento = Alinhamento_imu,
        desvio= DesvioObstaculo, sensor_distancia= SensorDistancia)):
        """Inicializa com instancias das classes Estado, Visao, Imu e Alinhamento"""
        self.robo = robo
        self.robo.estado = robo.estado
        self.robo.imu = robo.imu
        self.robo.visao = robo.visao
        self.robo.alinhamento = robo.alinhamento
        self.robo.desvio = robo.desvio
        self.robo.sensor_distancia = robo.sensor_distancia

    def main(self):
        try:
            self.robo.corrida()
        except KeyboardInterrupt:
            print(" CTRL+C detectado. O loop foi interrompido.")
            y = SerialMyrio()
            y.parar()
        

x = CriarRobo()
x.main()
        

