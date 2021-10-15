"""
Funcao para subir degrau do projeto Humanoide RoboIME 2021

Tomada de decisao para transicao entre os estados
Feita para ser utilizada em Raspberry Pi
Segunda versao

    OBSERVACOES:
    

Baseado em main_INTEL_humanoid_2020
@autores: 
"""

#Bibliotecas 

from time import *
import serial

import numpy as np
import math
import RTIMU
import RPi.GPIO as GPIO
import classes
import VL53L0X
print("Antes da Loop_corrida")
import main_corrida_2021_v1
print("Depois da Loop_corrida")
import picamera
import visao
import funcoes
from constantes import *


# Configuracoes iniciais

myrio = classes.Classe_porta_serial()
estado = classes.Classe_estado(myrio)
print("Antes da Classe_camera")
camera = main_corrida_2021_v1.get_camera()
estado.Trocar_estado(PARAR)


# Anda ate a proximidade do degrau desejada e realinha
def Loop_degrau(Estado, proximidade,numero_de_passos):
    estado.Trocar_estado(ANDAR)
    print("Dentro do Loop_degrau")
    ##ponto em que seria bom parar para tirar a foto                  
    while visao.checar_proximidade(proximidade, camera.Take_photo()):
        print("Andando em frente")
    sleep(intervalo_caminhada*numero_de_passos)
    
        
    estado.Trocar_estado(PARAR)

    situacao = funcoes.checar_alinhamento_pista_v2(camera)

    while situacao != ANDAR:
        estado.Trocar_estado(situacao)
        sleep(intervalo_enquanto_gira)
        estado.Trocar_estado(PARAR)
        sleep(tempo_para_parar)
        situacao = funcoes.checar_alinhamento_pista_v2(camera)
        print("Alinhando...")

    estado.Trocar_estado(Estado)

#Funcao main
        
if __name__ == "__main__":
    numero_de_passos_subida = int(input("entre com o numero de passos antes de subir"))
    numero_de_passos_descida = int(input("entre com o numero de passos antes de descer"))
    try:
        print("Programa rodando... pode ser interrompido usando CTRL+C")
        Loop_degrau(SUBIR, proximidade_subida,numero_de_passos_subida)
        Loop_degrau(DESCER, proximidade_descida,numero_de_passos_descida)
        main_corrida_2021_v1.Loop_corrida()

    except KeyboardInterrupt:
        print(" CTRL+C detectado. O loop foi interrompido.")
    estado.Trocar_estado(PARAR)