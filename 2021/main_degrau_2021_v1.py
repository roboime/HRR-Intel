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





def Loop_degrau(Estado, proximidade):
    estado.Trocar_estado(ANDAR, myrio)                  
    while funcoes.checa_proximidade(proximidade):
        print("Andando em frente")

    if funcoes.esta_desalinhado(tolerancia_desalinhamento):
        estado.Trocar_estado(funcoes.decisao_alinhamento(), myrio)
        while(funcoes.esta_desalinhado(tolerancia_desalinhamento)):
            print("Alinhando...")

    estado.Trocar_estado(Estado , myrio)

def Loop_corrida():
    t_0 = time()
    while True:
        t_1 = time()
        print("Estado padrao")
        estado.Trocar_estado(ANDAR, myrio)  
        ########################################### Checando alinhamento com a pista ###########################################
        if t_1 - t_0 > intervalo_alinhamento:
            estado.Trocar_estado(PARAR, myrio)
            sleep(tempo_para_parar)
            estado.Trocar_estado(funcoes.checar_alinhamento_pista(camera, tolerancia_alinhamento), myrio) #PARAR, GIRAR_ESQUERDA ou GIRAR_DIREITA
            while estado.Obter_estado_atual() != PARAR or estado.Obter_estado_atual() != ANDAR: 
                print("desalinhado com a pista")
                estado.Trocar_estado(funcoes.checar_alinhamento_pista(camera, tolerancia_alinhamento), myrio)
                sleep(intervalo_enquanto_gira)
            print("direçao corrigida")
            t_0 = t_1 = time()
                
    

#Funcao main

            
        
if __name__ == "__main__":
    try:
        print("Programa rodando... pode ser interrompido usando CTRL+C")
        Loop_degrau(SUBIR, proximidade_subida)
        Loop_degrau(DESCER, proximidade_subida)
        Loop_corrida()

    except KeyboardInterrupt:
        print(" CTRL+C detectado. O loop foi interrompido.")
    estado.Trocar_estado(PARAR, myrio)