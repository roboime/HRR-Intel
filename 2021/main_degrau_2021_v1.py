"""
Função para subir degrau do projeto Humanoide RoboIME 2021

Tomada de decisão para transição entre os estados
Feita para ser utilizada em Raspberry Pi
Segunda versao

    OBSERVAÇÕES:
    

Baseado em main_INTEL_humanoid_2020
@autores: 
"""

#Bibliotecas 

from time import *
import serial

import numpy as np
import math
import RTIMU
import get_yaw as Direcao
import RPi.GPIO as GPIO
import classes
import VL53L0X
from main_corrida_2021_v1 import Loop_corrida
import PiCamera as picamera

import funcoes


#Variaveis auxiliares, a velocidade esta em cm/seg                
tolerancia_desalinhamento = 10
proximidade_subida = 10
proximidade_descida = 10
tempo_para_parar = 1


ANDAR="0"                 
GIRAR_ESQUERDA="1"        
GIRAR_DIREITA="2"         
PARAR="3"                 
SUBIR= "4"
DESCER = "5"
# Configurações iniciais

estado = classes.Classe_estado()
myrio = classes.Classe_porta_serial()
camera = classes.Classe_camera()
estado.Trocar_estado(PARAR, myrio)

tolerancia_alinhamento = 10
intervalo_alinhamento = 10
intervalo_enquanto_gira = 0.5
tolerancia_centro = 20
tolerancia_para_frente = 60

# Anda até a proximidade do degrau desajada e realinha
def Loop_degrau(Estado, proximidade):
    estado.Trocar_estado(ANDAR, myrio)                  
    while funcoes.checa_proximidade(proximidade):
        print("Andando em frente")
    estado.Trocar_estado(PARAR, myrio)

    camera = picamera.PiCamera()
    decisao = funcoes.checar_alinhamento_pista(camera, tolerancia_centro, tolerancia_para_frente)

    if decisao != ANDAR:
        estado.Trocar_estado(decisao, myrio)
        while(funcoes.checar_alinhamento_pista(camera, tolerancia_centro, tolerancia_para_frente) != ANDAR):
            print("Alinhando...")

    estado.Trocar_estado(Estado, myrio)

#Funcao main
        
if __name__ == "__main__":
    try:
        print("Programa rodando... pode ser interrompido usando CTRL+C")
        Loop_degrau(SUBIR, proximidade_subida)
        Loop_degrau(DESCER, proximidade_descida)
        Loop_corrida()

    except KeyboardInterrupt:
        print(" CTRL+C detectado. O loop foi interrompido.")
    estado.Trocar_estado(PARAR, myrio)