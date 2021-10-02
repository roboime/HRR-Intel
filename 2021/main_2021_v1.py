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
myrio = classes.Classe_porta_serial()
s_distancia = classes.Classe_distancia()
s_giroscopio = classes.Classe_giroscopio()

estado = classes.Classe_estado()
myrio = classes.Classe_porta_serial()
estado.Trocar_estado(PARAR, myrio)

s_distancia = classes.Classe_distancia()

giroscopio = classes.Classe_giroscopio()


#Funcao main

def main():
    print("Programa rodando... pode ser interrompido usando CTRL+C")
    try:                    
        while True:
            print("Estado padrao")
            estado.Trocar_estado(PARAR, myrio)  
            
            if (s_distancia.Get_distance() <= distancialimite):
                print ("obstaculo detectado")
                estado.Trocar_estado(PARAR, myrio)
                estado.Trocar_estado(funcoes.decisao_desvio(), myrio)             
                
                if (estado.atual == GIRAR_ESQUERDA or estado.atual == GIRAR_DIREITA):            
                    estado.Trocar_estado(funcoes.quando_parar_de_girar(s_giroscopio,s_distancia), myrio)    
                    estado.Trocar_estado(ANDAR, myrio)
                    estado.Trocar_estado(funcoes.quando_parar_de_andar(s_giroscopio,s_distancia, velocidade, largura_do_robo), myrio)
                    print("obstaculo ultrapassado")
                
            if (np.abs((s_giroscopio.Obter_angulo_yaw())) > angulo_limite):  
                print("desalinhado com a pista")
                if s_giroscopio.Obter_angulo_yaw() > 0:
                    estado.Trocar_estado(GIRAR_DIREITA, myrio)
                else:
                    estado.Trocar_estado(GIRAR_ESQUERDA, myrio)

                estado.Trocar_estado(funcoes.quando_parar_de_alinhar(angulo_limite/2, s_giroscopio)) 
                print("direçao corrigida")
                
            
    except KeyboardInterrupt:
        estado.Trocar_estado(PARAR, myrio)
        print(" CTRL+C detectado. O loop foi interrompido.")

    estado.Trocar_estado(PARAR, myrio)
        
if __name__ == "__main__": main()
