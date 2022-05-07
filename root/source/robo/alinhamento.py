from time import sleep
import source.robo.constantes as c

def girar(robo, sentido):
    robo.estado.trocar_estado(sentido)
    while abs(robo.imu.obter_angulo_yaw()) > c.TOLERANCIA_ALINHAMENTO:
        sleep(c.INTERVALO_GIRO_ALINHAMENTO)
    robo.estado.trocar_estado(c.PARAR)

def corrigir_alinhamento(robo):
    robo.estado.trocar_estado(robo.visao.decisao_alinhamento())
    while robo.estado.obter_estado_atual() == "GIRAR_ESQUERDA" or robo.estado.obter_estado_atual() == "GIRAR_DIREITA":
        sleep(c.INTERVALO_GIRO_ALINHAMENTO)
        robo.estado.trocar_estado(c.PARAR)
        robo.estado.trocar_estado(robo.visao.decisao_alinhamento())

def alinhamento(robo):
    if abs(robo.imu.delta_angulo_yaw()) < c.ANGULO_YAW_LIMITE:
        return
    elif robo.imu.delta_angulo_yaw() < - c.ANGULO_YAW_LIMITE:
        girar(robo, "GIRAR_DIREITA")

    elif robo.imu.delta_angulo_yaw() > c.ANGULO_YAW_LIMITE:
        girar(robo, "GIRAR_ESQUERDA")
    corrigir_alinhamento(robo)
    robo.imu.mudar_referencia()

        