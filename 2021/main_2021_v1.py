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
import serial

import numpy as np
import math

import RTIMU
import get_yaw as Direcao
import RPi.GPIO as GPIO
import classes
import VL53L0X



#Variaveis auxiliares
percorrer_2cm = 5                
distancialimite = 46  

ANDAR="0"                 
GIRAR_ESQUERDA="1"        
GIRAR_DIREITA="2"         
PARAR="3"                 

# Configurações iniciais


#Funcao main

Atual = Estado.estado(PARAR) 
serial_output.write(Atual.name)

print("Programa rodando... pode ser interrompido usando CTRL+C")
try:                    
    while True:
        print("Estado padrao")
        Atual.trocar_para(ANDAR)
        serial_output.write(Atual.getName())    
        
        #ocorre divisao por 10 para passar para cm
        distancia_atual[0] = sensor_distancia.get_distance()/10 
        angulo_atual[0] = Direcao.get_angulo_atual(intervalo_verificacoes) - angulo_inicial
        
        if (distancia_atual[0] <= distancialimite):
            print ("obstaculo detectado")
            Atual.trocar_para(PARAR)    
            serial_output.write(Atual.getName())
            Atual.trocar_para(Estado.Decisao_desvio()) 
            serial_output.write(Atual.name)                    
            
            if (Atual.name == GIRAR_ESQUERDA or Atual.name == GIRAR_DIREITA):            
                Atual.trocar_para(Estado.quando_parar_de_girar(angulo_atual,distancia_atual))    
                serial_output.write(Atual.name)
                
                Atual.trocar_para(ANDAR)
                serial_output.write(Atual.name)
                
                Atual.trocar_para(Estado.quando_parar_de_andar(distancia_atual,angulo_atual))
                serial_output.write(Atual.name)                  
                
            print("obstaculo ultrapassado")
            
            

        angulo_atual[0] = Direcao.get_angulo_atual(intervalo_verificacoes) - angulo_inicial
        if (np.abs((angulo_atual[0])) > angulo_limite):  
            print("desalinhado com a pista")
            if angulo_atual[0] > 0:
                Atual.trocar_para(GIRAR_DIREITA)
            else:
                Atual.trocar_para(GIRAR_ESQUERDA)
            serial_output.write(Atual.getName())
            Atual.trocar_para(Estado.quando_parar_de_alinhar(angulo_limite/2)) 
            serial_output.write(Atual.getName())
            print("direçao corrigida")
            
        
except KeyboardInterrupt:
    Atual.trocar_para(PARAR)    
    serial_output.write(Atual.getName())
    print(" CTRL+C detectado. O loop foi interrompido.")

Atual.trocar_para(PARAR)
serial_output.write(Atual.getName())
print(Atual)
    
