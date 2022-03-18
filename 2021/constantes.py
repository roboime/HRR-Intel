import numpy as np

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
    ANDAR : 0.04,
    GIRAR_ESQUERDA : 0.04,
    GIRAR_DIREITA : 0.04,
    PARAR : 0.04
}

intervalo_alinhamento = 0.04
intervalo_caminhada = 1     # Tentar maximizar intervalo_caminhada quando for botar o robo para andar
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

RANGE_INCLINACAO = 75 #Em graus

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


