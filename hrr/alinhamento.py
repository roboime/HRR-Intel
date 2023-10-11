"""Modulo responsavel pelo alinhamento do robo"""
from time import sleep
import constantes as c
from visao import decisao_desvio
from robo import Robo

class Alinhamento():
    """Classe dedicada a verificar e corrigir o alinhamento do robo com a direcao da pista"""
    def __init__(self, robo):
        """Inicializa com uma instancia da classe Robo"""
        self.robo: Robo = robo
        self.tradutor = {
            c.ANDAR: '0',
            c.GIRAR_ESQUERDA: '1', 
            c.GIRAR_DIREITA: '2',
            c.PARAR: '3',
            c.SUBIR: '6',
            c.DESCER: '7'
        }

    def girar(self, sentido):
        """Gira o robo ate alinhar com a frente"""
        self.robo.estado.trocar_estado(sentido)
        while abs(self.robo.imu.delta_angulo_yaw()) > c.TOLERANCIA_ALINHAMENTO:
            sleep(c.INTERVALO_GIRO_ALINHAMENTO)
        self.robo.estado.trocar_estado(c.PARAR)

    def corrigir(self):
        """Gira o robo ate alinhar com o centro da pista com o auxilio da Classe_imagem"""
        self.robo.estado.trocar_estado(self.robo.camera.decisao_alinhamento())
        while self.robo.estado.obter_estado_atual() != "ANDAR":
            self.robo.estado.trocar_estado(c.PARAR)
            self.robo.estado.trocar_estado(self.robo.camera.decisao_alinhamento())
    def verificar_alinhamento(self):
        """Verificar o alinhamento do robo com a pista e o corrige caso esteja desalinhado"""
        self.corrigir()

class Alinhamento_imu(Alinhamento):
    def __init__(self, robo):
        Alinhamento.__init__(self, robo)
        self.angulo = 0.0
    def verificar_alinhamento(self):
        print("Entrou na Verificacao de Alinhamento")
        self.angulo = self.angulo + (self.robo.imu.calcular_w_yaw() * 1/2610 + c.B)
        print ("AnGz=%.2f" %self.angulo)
        delta = self.angulo - self.robo.imu.get_referencia()
        self.robo.discovery.escrever_estado(decisao_desvio(self.robo.camera))
