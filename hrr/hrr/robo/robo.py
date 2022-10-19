"""Modulo base do robo de corrida"""
from time import sleep

class Robo:
    """Classe base do robo de corrida"""
    loop_rate = 24
    def __init__(self, estado = None, imu = None, visao = None, alinhamento = None,
        desvio= None, sensor_distancia= None):
        """Inicializa com instancias das classes Estado, Visao, Imu e Alinhamento"""
        self.estado = estado
        self.imu = imu
        self.visao = visao
        self.alinhamento = alinhamento
        self.desvio = desvio
        self.sensor_distancia = sensor_distancia
    def corrida(self):
        """Metodo base da corrida do robo"""
        while True:
            sleep(1/self.loop_rate)
            self.estado.trocar_estado("ANDAR")
            self.alinhamento.verificar_alinhamento()
            if self.desvio is not None:
                self.desvio.verificar_desvio()
            

def main():
    Robo.__init__
    Robo.corrida