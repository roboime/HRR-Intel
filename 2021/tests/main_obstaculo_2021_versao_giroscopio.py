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

import time
import numpy as np
import math
import classes
import funcoes


#Variaveis auxiliares, a velocidade esta em cm/seg
#velocidade = ???                
distancialimite = 46
angulo_limite = 10 
#largura_do_robo = ???

ANDAR = "0"                 
GIRAR_ESQUERDA = "1"        
GIRAR_DIREITA = "2"         
PARAR = "3"                 

# Configuracoes iniciais

estado = classes.Classe_estado()
estado.Trocar_estado(PARAR, myrio)
myrio = classes.Classe_porta_serial()
sensor_distancia = classes.Classe_distancia()
sensor_giroscopio = classes.Classe_giroscopio()
camera = classes.Classe_camera()


#Funcao main

def Loop_obstaculo():
    print("Programa rodando... pode ser interrompido usando CTRL+C")
    while True:
        print("Estado padrao")
        estado.Trocar_estado(PARAR, myrio)  
        
        if (sensor_distancia.Get_distance() <= distancialimite):
            print ("obstaculo detectado")
            estado.Trocar_estado(PARAR, myrio)
            estado.Trocar_estado(funcoes.decisao_desvio(camera), myrio)             
            
            if (estado.atual == GIRAR_ESQUERDA or estado.atual == GIRAR_DIREITA):            
                estado.Trocar_estado(funcoes.quando_parar_de_girar(sensor_giroscopio,sensor_distancia), myrio)    
                estado.Trocar_estado(ANDAR, myrio)
                estado.Trocar_estado(funcoes.quando_parar_de_andar(sensor_giroscopio,sensor_distancia, velocidade, largura_do_robo), myrio)
                print("obstaculo ultrapassado")
            
        if (np.abs((sensor_giroscopio.Obter_angulo_yaw())) > angulo_limite):  
            print("desalinhado com a pista")
            if sensor_giroscopio.Obter_angulo_yaw() > 0:
                estado.Trocar_estado(GIRAR_DIREITA, myrio)
            else:
                estado.Trocar_estado(GIRAR_ESQUERDA, myrio)

            estado.Trocar_estado(funcoes.quando_parar_de_alinhar(angulo_limite/2, sensor_giroscopio)) 
            print("direçao corrigida")
                
 
if __name__ == "__main__":
    try:
        Loop_obstaculo()
    except KeyboardInterrupt:
        print(" CTRL+C detectado. O loop foi interrompido.")
    estado.Trocar_estado(PARAR, myrio)