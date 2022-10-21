"""Modulo responsavel pelo alinhamento do robo"""
from time import sleep
import constantes as c
from imu6050 import Imu6050

class Alinhamento():
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
            self.robo.estado.trocar_estado(c.PARAR)
            self.robo.estado.trocar_estado(self.robo.visao.decisao_alinhamento())
    def verificar_alinhamento(self):
        """Verificar o alinhamento do robo com a pista e o corrige caso esteja desalinhado"""
        self.__corrigir()

class Alinhamento_imu(Alinhamento):
    def __init__(self, robo):
        Alinhamento.__init__(self, robo)
        self.angulo = 0.0
    def verificar_alinhamento(self):
        print("Entrou na Verificacao de Alinhamento")
        g = Imu6050()
        self.angulo = self.angulo + (g.__calcular_w_yaw() * 1/2610 + c.B)*3.0
        print ("AnGz=%.2f" %self.angulo)
        delta = self.angulo - g.get_referencia()
        if abs(delta) < c.ANGULO_YAW_LIMITE:
            return

        elif delta < - c.ANGULO_YAW_LIMITE:
            print("Girar Direita ")
            self.__girar("GIRAR_DIREITA")

        elif delta > c.ANGULO_YAW_LIMITE:
            print("Girar Esquerda ")
            self.__girar("GIRAR_ESQUERDA")

        self.__corrigir()
        print("Corrigiu ")
        g.mudar_referencia(self.angulo)
        print("Referencia do Giro Resetada ")

class Alinhamento_visao(Alinhamento):
    def __init__(self):
        Alinhamento.__init__()
    def verificar_alinhamento(self):
        print("Verificar Alinhamento ")
        self.__corrigir()
