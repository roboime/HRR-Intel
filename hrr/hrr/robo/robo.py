"""Modulo base do robo de corrida"""

class Robo:
    """Classe base do robo de corrida"""
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
            self.estado.trocar_estado("ANDAR")
            self.alinhamento.verificar_alinhamento()
    def corrida_desvio(self):
        """Especializacao do metodo de corrida do Robo para desviar de obstaculos"""
        while True:
            self.estado.trocar_estado("ANDAR")
            self.alinhamento.verificar_alinhamento()
            self.desvio.verificar_desvio()
            