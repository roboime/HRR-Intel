from time import sleep
import source.robo.constantes as c
from source.robo.estado.estado import Estado
from source.robo.visao.visao import Visao
from source.robo.imu.imu import Imu

class Robo(Estado,Visao,Imu):
    def __init__(self, imu):
        Estado.__init__(self)
        Visao.__init__(self)
        Imu.__init__(self)
    def corrida(self):
        while(True):
            self.trocar_estado("ANDAR")
            self.alinhamento(self)
    def girar(self, sentido):
        self.trocar_estado(sentido)
        while abs(self.obter_angulo_yaw()) > c.TOLERANCIA_ALINHAMENTO:
            sleep(c.INTERVALO_GIRO_ALINHAMENTO)
        self.trocar_estado(c.PARAR)

    def corrigir_alinhamento(self):
        self.trocar_estado(self.decisao_alinhamento())
        while self.obter_estado_atual() == "GIRAR_ESQUERDA" or self.obter_estado_atual() == "GIRAR_DIREITA":
            sleep(c.INTERVALO_GIRO_ALINHAMENTO)
            self.trocar_estado(c.PARAR)
            self.trocar_estado(self.decisao_alinhamento())

    def alinhamento(self):
        if abs(self.delta_angulo_yaw()) < c.ANGULO_YAW_LIMITE:
            return
        elif self.delta_angulo_yaw() < - c.ANGULO_YAW_LIMITE:
            self.girar(self, "GIRAR_DIREITA")

        elif self.delta_angulo_yaw() > c.ANGULO_YAW_LIMITE:
            self.girar(self, "GIRAR_ESQUERDA")
        self.corrigir_alinhamento(self)
        self.mudar_referencia()
            