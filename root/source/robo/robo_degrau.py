from robo import Robo
from desvio_degrau import DesvioDegrau

class RoboDegrau(Robo):
    """Classe que herda as funcionalidades do Robo e eh dedicada ao desafio de desvio de degrau"""
    def __init__(self, estado = None, imu = None, sensor_distancia = None, visao = None):
        """Inicializa herdando o Robo e instanciando as classes SensorDistancia e DesvioDegrau"""
        Robo.__init__(self, estado, imu, visao)
        self.sensor_distancia = sensor_distancia
        self.desvio_degrau = DesvioDegrau()
        
    def corrida(self):
        """Especializacao do metodo de corrida do Robo para desviar de degraus"""
        while(True):
            self.estado.trocar_estado("ANDAR")
            self.alinhamento.verificar_alinhamento()
            self.desvio_degrau.verificar_degrau()
