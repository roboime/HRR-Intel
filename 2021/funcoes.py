from main_2021_v1 import Atual
import serial
import RPi.GPIO as GPIO
import RTIMU
import VL53L0X
import pickle
import time
import numpy as np


ANDAR="0"                 
GIRAR_ESQUERDA="1"        
GIRAR_DIREITA="2"         
PARAR="3"  


#peguei o giroscopio pois imaginei que o robo poderia precisar fazer alguma correcao 
# durante a trajetoria futuramente
def quando_parar_de_andar(giroscopio, s_distancia, velocidade, largura_do_robo):
    projecao_horizontal_trajetoria = s_distancia.anterior*np.cos(np.pi/180 * giroscopio.Obter_angulo_yaw()) + largura_do_robo
    projecao_vertical_trajetoria = s_distancia.anterior*np.sin(np.pi/180 * giroscopio.Obter_angulo_yaw())
    trajetoria = ( projecao_vertical_trajetoria**2 +projecao_horizontal_trajetoria**2 ) ** (1/2)
    tempo_necessario = trajetoria/velocidade
    instante_inicial = time.time()

    while (time.time() - instante_inicial < tempo_necessario):
        print("andamos ", velocidade*time.time() - instante_inicial(), " de ", trajetoria)

    return PARAR