"""Modulo responsavel pelo alinhament do robo"""
from time import sleep
from . import constantes as c

class __Alinhamento():
    """Classe dedicada a verificar e corrigir o alinhamento do robo com a direcao da pista"""
    def __init__(self, robo):
        """Inicializa com uma instancia da classe Robo"""
        self.robo = robo
    def __girar(self, sentido):
        """Gira o robo ate alinhar com a frente"""
        self.robo.estado.trocar_estado(sentido)
        while abs(self.robo.imu.obter_angulo_yaw()) > c.TOLERANCIA_ALINHAMENTO:
            sleep(c.INTERVALO_GIRO_ALINHAMENTO)
        self.robo.estado.trocar_estado(c.PARAR)

    def __corrigir(self):
        """Gira o robo ate alinhar com o centro da pista com o auxilio da visao"""
        self.robo.estado.trocar_estado(self.robo.visao.decisao_alinhamento())
        while self.robo.estado.obter_estado_atual() != "ANDAR":
            sleep(c.INTERVALO_GIRO_ALINHAMENTO)
            self.robo.estado.trocar_estado(c.PARAR)
            self.robo.estado.trocar_estado(self.robo.visao.decisao_alinhamento())
    def verificar_alinhamento(self):
        """Verificar o alinhamento do robo com a pista e o corrige caso esteja desalinhado"""

class Alinhamento_imu(__Alinhamento):
    def __init__(self):
        __Alinhamento.__init__()
    def verificar_alinhamento(self):
        """Verificar o alinhamento do robo com a pista com o auxílio do IMU e o
        corrige caso esteja desalinhado"""
        delta = self.robo.imu.delta_angulo_yaw()
        if abs(delta) < c.ANGULO_YAW_LIMITE:
            return

        elif delta < - c.ANGULO_YAW_LIMITE:
            self.__girar("GIRAR_DIREITA")

        elif delta > c.ANGULO_YAW_LIMITE:
            self.__girar("GIRAR_ESQUERDA")

        self.__corrigir()
        self.robo.imu.mudar_referencia()

class Alinhamento_visao(__Alinhamento):
    def __init__(self):
        __Alinhamento.__init__()
    def verificar_alinhamento(self):
        """Verificar o alinhamento do robo com a pista com o auxílio da visao
        e o corrige caso esteja desalinhado"""
        self.__corrigir()
    