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

from time import sleep, time
import numpy as np
import math
import classes
import funcoes
from constantes import *


# Configuracoes iniciais

myrio = classes.Classe_porta_serial()
camera = classes.Classe_camera()
estado = classes.Classe_estado(myrio, tempo_do_passo)

#Funcao main

def Loop_corrida():
    t_0 = time()
    t_1 = intervalo_alinhamento + t_0
    while True:
        print("Andando em frente")
        estado.Trocar_estado(ANDAR)
        sleep(intervalo_caminhada)  # Tentar maximizar intervalo_caminhada quando for botar o robo para andar
        ########################################### Checando alinhamento com a pista ###########################################
        if t_1 - t_0 >= intervalo_alinhamento:
            print("hora de alinhar")
            estado.Trocar_estado(PARAR)
            sleep(tempo_para_parar)
            estado.Trocar_estado(funcoes.checar_alinhamento_pista_v2(camera))  # Frente, GIRAR_ESQUERDA ou GIRAR_DIREITA
            numero_de_giradas = 1
            while estado.Obter_estado_atual() == GIRAR_DIREITA or estado.Obter_estado_atual() == GIRAR_ESQUERDA:
                print("desalinhado com a pista, iniciando a ",numero_de_giradas, "a girada")
                sleep(intervalo_enquanto_gira)
                estado.Trocar_estado(PARAR)
                sleep(tempo_para_parar)
                estado.Trocar_estado(funcoes.checar_alinhamento_pista_v2(camera))
                numero_de_giradas+=1
            print("direcao corrigida")
            numero_de_giradas = 1
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
    estado.Trocar_estado(PARAR)
    print(estado)
