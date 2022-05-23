"""Modulo do robo para o desafio de desvio de obstaculos."""
from .robo import Robo
from .desvio_obstaculo import DesvioObstaculo

class RoboObstaculo(Robo):
    """Classe que herda as funcionalidades do Robo para desafio de desvio de obstaculos"""
    def __init__(self, estado = None, imu = None, sensor_distancia = None, visao = None):
        """Inicializa herdando o Robo e instanciando as classes SensorDistancia e DesvioObstaculo"""
        Robo.__init__(self, estado, imu, visao)
        self.sensor_distancia = sensor_distancia
        self.desvio_obstaculo = DesvioObstaculo(self)
    def corrida(self):
        """Especializacao do metodo de corrida do Robo para desviar de obstaculos"""
        while True:
            self.estado.trocar_estado("ANDAR")
            self.alinhamento.verificar_alinhamento()
            self.desvio_obstaculo.verificar_obstaculo()
            