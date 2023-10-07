"""Modulo responsavel pelo alinhamento do robo"""
from time import sleep
import constantes as c
from imu6050 import Imu6050
from serial_com import SerialMyrio
from visao import Visao
from estado import Estado

class Alinhamento():
    """Classe dedicada a verificar e corrigir o alinhamento do robo com a direcao da pista"""
    def __init__(self):
        """Inicializa com uma instancia da classe Robo"""
        self.e = Estado()
    def girar(self, sentido):
        """Gira o robo ate alinhar com a frente"""
        self.e.trocar_estado(sentido)
        while abs(self.robo.imu.obter_angulo_yaw()) > c.TOLERANCIA_ALINHAMENTO:
            sleep(c.INTERVALO_GIRO_ALINHAMENTO)
        self.e.trocar_estado(c.PARAR)

    def corrigir(self):
        """Gira o robo ate alinhar com o centro da pista com o auxilio da visao"""
        self.v = Visao()
        self.e.trocar_estado(self.v.decisao_alinhamento())
        while self.e.obter_estado_atual() != "ANDAR":
            self.e.trocar_estado(c.PARAR)
            self.e.trocar_estado(self.v.decisao_alinhamento())
    def verificar_alinhamento(self):
        """Verificar o alinhamento do robo com a pista e o corrige caso esteja desalinhado"""
        self.corrigir()

class Alinhamento_imu(Alinhamento):
    def __init__(self):
        Alinhamento.__init__(self)
        self.angulo = 0.0
        self.g = Imu6050()
        self.x = SerialMyrio()
    def verificar_alinhamento(self):
        print("Entrou na Verificacao de Alinhamento")
        self.angulo = self.angulo + (self.g.calcular_w_yaw() * 1/2610 + c.B)
        print ("AnGz=%.2f" %self.angulo)
        delta = self.angulo - self.g.get_referencia()
        if abs(delta) < c.ANGULO_YAW_LIMITE:
           self.x.escrever_estado("ANDAR") 
           print("Andar Frente ")

        elif delta < - c.ANGULO_YAW_LIMITE:
            print("Girar Direita ")
            self.x.escrever_estado("GIRAR_DIREITA")

        elif delta > c.ANGULO_YAW_LIMITE:
            print("Girar Esquerda ")
            self.x.escrever_estado("GIRAR_ESQUERDA")

       # self.corrigir()
       # print("Corrigiu ")
       # self.g.mudar_referencia(self.angulo)
       # print("Referencia do Giro Resetada ")

class Alinhamento_visao(Alinhamento):
    def __init__(self):
        Alinhamento.__init__()
    def verificar_alinhamento(self):
        print("Verificar Alinhamento ")
        self.corrigir()
