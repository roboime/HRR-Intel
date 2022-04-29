from time import sleep

def girar(robo, sentido):
    robo.estado.trocar_estado(sentido)
    while abs(robo.imu.obter_angulo_yaw) > TOLERANCIA_ALINHAMENTO:
        sleep(INTERVALO_GIRO_ALINHAMENTO)
    robo.estado.trocar_estado(PARAR)

def corrigir_alinhamento(robo):
    robo.estado.trocar_estado(robo.visao.checar_alinhamento_pista())
    while robo.estado.obter_estado_atual() == GIRAR_ESQUERDA or robo.estado.obter_estado_atual() == GIRAR_DIREITA:
        sleep(INTERVALO_GIRO_ALINHAMENTO)
        robo.estado.trocar_estado(PARAR)
        robo.estado.trocar_estado(robo.visao.checar_alinhamento_pista())

def alinhamento(robo):
    if abs(robo.imu.delta_angulo_yaw()) < ANGULO_YAW_LIMITE:
        return
    elif robo.imu.delta_angulo_yaw() < - ANGULO_YAW_LIMITE:
        girar(robo, GIRAR_DIREITA)

    elif robo.imu.delta_angulo_yaw() > ANGULO_YAW_LIMITE:
        girar(robo, GIRAR_ESQUERDA)
    corrigir_alinhamento(robo)
    robo.imu.mudar_referencia()

        