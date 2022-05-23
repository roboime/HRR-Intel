"""Modulo base do robo de corrida"""
from .alinhamento import Alinhamento

class Robo:
    """Classe base do robo de corrida"""
    def __init__(self = None, estado = None, imu = None, visao = None):
        """Inicializa com instancias das classes Estado, Visao, Imu e Alinhamento"""
        self.estado = estado
        self.imu = imu
        self.visao = visao
        self.alinhamento = Alinhamento(self)
    def corrida(self):
        """Metodo base da corrida do robo"""
        while True:
            self.estado.trocar_estado("ANDAR")
            self.alinhamento.verificar_alinhamento()
    