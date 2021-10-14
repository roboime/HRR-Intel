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

distancialimite = 50.0
distanciaMedia = 35.0
distanciaMinima = 20.0

######################## CONSTANSTES A SE AJUSTAR ########################


DIST_MAXIMA = 80


# CONSTANTES DE PASSO

## CONSTANTES DE TEMPO
tempo_do_passo = {
    ANDAR : 2,
    GIRAR_ESQUERDA : 0.7,
    GIRAR_DIREITA : 0.7,
    PARAR : 1
}

intervalo_alinhamento = 10
intervalo_caminhada = 2     # Tentar maximizar intervalo_caminhada quando for botar o robo para andar
intervalo_enquanto_gira = 3
tempo_para_parar = 1


## CONSTANTES DE GIRO
desloc_por_passo = {
    ANDAR : 3,              # cm por passada
    GIRAR_ESQUERDA : 0.4,   # rad por passada
    GIRAR_DIREITA : 0.4     # rad por passada
}

velocidade_ang_em_graus = [0,0,0]
velocidade_angular = [0,0,0]
velocidade_ang_em_graus[int(GIRAR_ESQUERDA)] = 10
velocidade_ang_em_graus[int(GIRAR_DIREITA)] = 10
velocidade_angular[int(GIRAR_ESQUERDA)] = velocidade_ang_em_graus[int(GIRAR_ESQUERDA)]*np.pi/180
velocidade_angular[int(GIRAR_DIREITA)] = velocidade_ang_em_graus[int(GIRAR_DIREITA)]*np.pi/180


# CONSTANTES DE VISAO

camera_constraste = 90
tolerancia_central = 15
tolerancia_para_frente = 60

## CONSTANTES DO DEGRAU

proximidade_subida = 10
proximidade_descida = 10


