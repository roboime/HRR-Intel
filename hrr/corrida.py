from robo import Robo
from alinhamento import Alinhamento_imu
from desvio import DesvioObstaculo
from estado import Estado
from serial_com import SerialMyrio
from imu6050 import Imu6050 
from visao import Visao
from sensor_distancia import SensorDistancia

class CriarRobo:
    def __init__(self, robo: Robo = Robo()):
        """Inicializa com instancias das classes Estado, Visao, Imu e Alinhamento"""
        self.robo = robo

    def main(self):
        try:
            self.robo.corrida()
        except KeyboardInterrupt:
            print(" CTRL+C detectado. O loop foi interrompido.")
            y = SerialMyrio()
            while(1):
                y.parar()
        

x = CriarRobo()
x.main()
        

