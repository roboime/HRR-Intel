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

import time
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
#tolerancia_desalinhamento = ???
#proximidade_subida = ???
#proximidade_descida = ???
#tempo_de_subida = ???
#tempo_de_descida = ???


ANDAR="0"                 
GIRAR_ESQUERDA="1"        
GIRAR_DIREITA="2"         
PARAR="3"                 
SUBIR= "4"
DESCER = "5"
# Configurações iniciais

estado = classes.Classe_estado()
myrio = classes.Classe_porta_serial()
estado.Trocar_estado(PARAR, myrio)

s_distancia = classes.Classe_distancia()

giroscopio = classes.Classe_giroscopio()


#Funcao main

def Loop_degrau():
    estado.Trocar_estado(ANDAR, myrio)                  
    while funcoes.checa_proximidade(proximidade_subida):
        print("Andando em frente")

    if funcoes.checa_desalinhamento(tolerancia_desalinhamento):
        estado.Trocar_estado(funcoes.decisao_alinhamento(), myrio)
        while(funcoes.checa_desalinhamento(tolerancia_desalinhamento) ):
            print("Alinhando...")

    estado.Trocar_estado(SUBIR, myrio)   
    time.sleep(tempo_de_subida)

    
    estado.Trocar_estado(ANDAR, myrio)                  
    while funcoes.checa_proximidade(proximidade_descida):
        print("Andando em frente")

    if funcoes.checa_desalinhamento(tolerancia_desalinhamento):
        estado.Trocar_estado(funcoes.decisao_alinhamento(), myrio)
        while(funcoes.checa_desalinhamento(tolerancia_desalinhamento) ):
            print("Alinhando...")

    estado.Trocar_estado(DESCER, myrio)   
    time.sleep(tempo_de_descida)

    estado.Trocar_estado(ANDAR, myrio)

            
        
if __name__ == "__main__":
    try:
        print("Programa rodando... pode ser interrompido usando CTRL+C")
        Loop_degrau()
    except KeyboardInterrupt:
        print(" CTRL+C detectado. O loop foi interrompido.")
    estado.Trocar_estado(PARAR, myrio)