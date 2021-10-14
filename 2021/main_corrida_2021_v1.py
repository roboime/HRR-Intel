"""
Funcao principal do projeto Humanoide RoboIME 2021

Tomada de decisao para transicao entre os estados
Feita para ser utilizada em Raspberry Pi
Segunda versao

    OBSERVACOES:
    

Baseado em main_INTEL_humanoid_2020
@autores: 
"""

#Bibliotecas 

from time import *
import numpy as np
import math
import classes
import funcoes


#Variaveis auxiliares, a velocidade esta em cm/seg

intervalo_alinhamento = 2
intervalo_caminhada = 0.4
intervalo_enquanto_gira = 0.5
tolerancia_central = 10
tolerancia_para_frente = 15
tempo_para_parar = 1

ANDAR="0"                 
GIRAR_ESQUERDA="1"        
GIRAR_DIREITA="2"         
PARAR="3"
SUBIR = "4"
DESCER = "5"
# Configuracoes iniciais

myrio = classes.Classe_porta_serial()
camera = classes.Classe_camera()
estado = classes.Classe_estado(myrio)

#Funcao main

def Loop_corrida():
    t_0 = time()
    t_1 = intervalo_alinhamento + t_0
    while True:
        print("Andando em frente")
        estado.Trocar_estado(ANDAR, myrio)
        sleep(intervalo_caminhada)
        ########################################### Checando alinhamento com a pista ###########################################
        if t_1 - t_0 > intervalo_alinhamento:
            print("hora de alinhar")
            estado.Trocar_estado(PARAR, myrio)
            sleep(tempo_para_parar)
            estado.Trocar_estado(funcoes.checar_alinhamento_pista_v1(camera, tolerancia_central, tolerancia_para_frente), myrio)  # Frente, GIRAR_ESQUERDA ou GIRAR_DIREITA
            while estado.Obter_estado_atual() != PARAR or estado.Obter_estado_atual() != ANDAR:
                print("desalinhado com a pista")
                sleep(intervalo_enquanto_gira)
                estado.Trocar_estado(PARAR, myrio)
                sleep(tempo_para_parar)
                estado.Trocar_estado(funcoes.checar_alinhamento_pista_v1(camera, tolerancia_central, tolerancia_para_frente), myrio)
            print("direcao corrigida")
            print(estado.atual)
            t_0 = t_1 = time()
        else:
            t_1 = time()

def get_camera():
    return camera

if __name__ == "__main__":
    try:
        print("Programa rodando... pode ser interrompido usando CTRL+C")
        Loop_corrida()
    except KeyboardInterrupt:
        print(" CTRL+C detectado. O loop foi interrompido.")
    estado.Trocar_estado(PARAR, myrio)
    print(estado)
