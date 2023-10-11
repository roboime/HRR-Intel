import numpy as np

"""Modulo de constantes usadas em estado.py"""
TEMPO_ANDAR = 1.06
TEMPO_GIRAR_ESQUERDA = 1.76
TEMPO_GIRAR_DIREITA = 1.72
TEMPO_PARAR = 0.75
TEMPO_SUBIR = 0
TEMPO_DESCER = 0

"""Constantes utilizadas em visao.py"""

#Canny constants
THRESHOLD1= 50
THRESHOLD2= 150
APERTURE_SIZE= 3
#HoughLinesP constants
RHO = 1
THETA = np.pi/180
THRESHOLD= 40  #100
MINLINELENGTH = 10 #10
MAXLINEGAP = 50 #20
RANGE_INCLINACAO = 75 #Em graus
INTERATIONS = 2

"""Constantes utilizadas em robo.py e seus modulos derivados"""

TOLERANCIA_ALINHAMENTO = 5
INTERVALO_GIRO_ALINHAMENTO = 0.0022
ANGULO_YAW_LIMITE = 30

######################## CONSTANTES BASICAS ##############################

ANDAR="0"                 
GIRAR_ESQUERDA="1"        
GIRAR_DIREITA="2"         
PARAR="3"
SUBIR = "6"
DESCER = "7"

######################## CONSTANTES INVARIAVEIS ##########################

velocidade = 5             
angulo_limite = 10.0

largura_do_robo = 25.0

distancialimite = 55.0
distanciaMedia = 35.0
distanciaMinima = 20.0

######################## CONSTANSTES A SE AJUSTAR ########################


# CONSTANTES DE PASSO

## CONSTANTES DE TEMPO
tempo_do_passo = {
    ANDAR : 3.6,
    GIRAR_ESQUERDA : 2.4,
    GIRAR_DIREITA : 2.4,
    PARAR : 0.75
}

intervalo_alinhamento = 20
intervalo_caminhada = 2     # Tentar maximizar intervalo_caminhada quando for botar o robo para andar
intervalo_enquanto_gira = 3
tempo_para_parar = 1

## CONSTANTES DE GIRO
desloc_por_passo = {
    ANDAR : 2.0,              # cm por passada
    GIRAR_ESQUERDA : 5.3 * np.pi / 180,   # grau por passada
    GIRAR_DIREITA : 7.5 * np.pi / 180     # grau por passada
}

velocidade_ang_em_graus = [0,0,0]
velocidade_angular = [0,0,0]
velocidade_ang_em_graus[int(GIRAR_ESQUERDA)] = 10
velocidade_ang_em_graus[int(GIRAR_DIREITA)] = 10
velocidade_angular[int(GIRAR_ESQUERDA)] = velocidade_ang_em_graus[int(GIRAR_ESQUERDA)]*np.pi/180
velocidade_angular[int(GIRAR_DIREITA)] = velocidade_ang_em_graus[int(GIRAR_DIREITA)]*np.pi/180


# CONSTANTES DE VISAO

NAO_HA_RETA = 0
HA_DUAS_RETAS = 1
SO_ESQUERDA = 2
SO_DIREITA = 3

X1 = 0
Y1 = 1
X2 = 2
Y2 = 3


constraste_da_camera = 70
tolerancia_central = 15
tolerancia_para_frente = 60

## CONSTANTES FUNCOES
casos_dic = ["NAO_HA_RETA", "HA_DUAS_RETAS", "SO_ESQUERDA", "SO_DIREITA"]

ANG_PITCH_CABECA = 38.0
ANG_CABECA_DEGRAU = 0.0

DIST_MAXIMA = 63 * np.cos(ANG_PITCH_CABECA*np.pi/180)

## CONSTANTES DO DEGRAU

proximidade_subida = 10
proximidade_descida = 10

"""Constantes IMU6050"""

PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47
DEVICE_ADDRESS = 0x68
C = 20.0
B = 0.00025


## CONSTANTES PARA ALINHAMENTO COM VISÃO

bottomLeftCornerOfText = (10,30)
fontScale              = 1
fontColor              = (255,255,255)
lineType               = 2


## CONSTANTES PARA A CAMERA

WIDTH = 1280
HEIGHT = 720
FRAMERATE = 30
WARMUP_TIME = 2
CONTRAST = 70