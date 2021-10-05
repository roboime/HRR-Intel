"""
Função principal do projeto Humanoide RoboIME 2021

Tomada de decisão para transição entre os estados
Feita para ser utilizada em Raspberry Pi
Segunda versao

    OBSERVAÇÕES:
    

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

intervalo_alinhamento = 10
intervalo_enquanto_gira = 0.5
tolerancia_alinhamento = 10
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
        print(estado.atual)
        ########################################### Checando alinhamento com a pista ###########################################
        if t_1 - t_0 >= intervalo_alinhamento:
            estado.Trocar_estado(funcoes.checar_alinhamento_pista(), myrio) #PARAR, GIRAR_ESQUERDA ou GIRAR_DIREITA
            print(estado.atual)
            while estado.Obter_estado_atual() != PARAR: 
                print("desalinhado com a pista")
                estado.Trocar_estado(funcoes.checar_alinhamento_pista(), myrio)
                print(estado)
                sleep(0.5)
            print("direçao corrigida")
            t_0 = t_1 = time()
        else: t_1 = time()

if __name__ == "__main__":
    try:
        print("Programa rodando... pode ser interrompido usando CTRL+C")
        Loop_corrida()
    except KeyboardInterrupt:
        print(" CTRL+C detectado. O loop foi interrompido.")
    estado.Trocar_estado(PARAR, myrio)
    print(estado)