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

ANDAR="0"                 
GIRAR_ESQUERDA="1"        
GIRAR_DIREITA="2"         
PARAR="3"
SUBIR = "4"
DESCER = "5"
# Configuracoes iniciais

#Variaveis auxiliares, a velocidade esta em cm/seg         
distancialimite = 50.0
angulo_limite = 10.0
intervalo_alinhamento = 5
intervalo_caminhada = 0.3
largura_do_robo = 25.0
tempo_para_parar = 1
intervalo_enquanto_gira = 1
tolerancia_central = 15
tolerancia_para_frente = 60
tempo_do_passo = [0,0,0]
tempo_do_passo[int(ANDAR)] = 0.8
tempo_do_passo[int(GIRAR_ESQUERDA)] = 0.7
tempo_do_passo[int(GIRAR_DIREITA)] = 0.7
rad_por_passo = [0,0,0]
cm_passo = 3
rad_por_passo[int(ANDAR)] = cm_passo
rad_por_passo[int(GIRAR_ESQUERDA)] = 0.4
rad_por_passo[int(GIRAR_DIREITA)] = 0.4


myrio = classes.Classe_porta_serial()
sensor_distancia = classes.Classe_distancia()
camera = classes.Classe_camera()
estado = classes.Classe_estado(myrio)

#Funcao main

def Loop_obstaculo():
    t_0 = time()
    t_1 = t_0 + intervalo_alinhamento
    while True:
        print("Estado padrao")
        estado.Trocar_estado(ANDAR)  
        print(estado)
        sleep(intervalo_caminhada)
        ########################################### Checando proximidade de obstaculo ##########################################

        print("Medida do sensor de distancia: {}\n".format(sensor_distancia.Get_distance()))

        if sensor_distancia.Get_distance() <= distancialimite:
            print ("obstaculo detectado ", sensor_distancia.atual)
            estado.Trocar_estado(PARAR)
            print(estado)
            estado.Trocar_estado(funcoes.decisao_desvio(camera))
            print(estado)
            
            if (estado.atual == GIRAR_ESQUERDA or estado.atual == GIRAR_DIREITA):
                direcao_girada  = estado.atual            
                estado.Trocar_estado(funcoes.quando_parar_de_girar_quantizado(sensor_distancia, tempo_do_passo, rad_por_passo, largura_do_robo, direcao_girada))    
                print(estado)
                estado.Trocar_estado(ANDAR)
                print(estado)
                estado.Trocar_estado(funcoes.quando_parar_de_andar_visaocomp_quantizado(tempo_do_passo, rad_por_passo))
                print(estado)
                print("obstaculo ultrapassado, iniciando compensasao de angulo")
                if(direcao_girada == GIRAR_ESQUERDA):
                    estado.Trocar_estado(GIRAR_DIREITA)
                    estado.Trocar_estado(funcoes.quando_parar_de_realinhar_quantizado(tempo_do_passo, rad_por_passo, GIRAR_DIREITA))
                if(direcao_girada == GIRAR_DIREITA):
                    estado.Trocar_estado(GIRAR_ESQUERDA)
                    estado.Trocar_estado(funcoes.quando_parar_de_realinhar_quantizado(tempo_do_passo, rad_por_passo, GIRAR_ESQUERDA))
                print("compensado o angulo girado")
            t_1 = time()

        ########################################### Checando alinhamento com a pista ###########################################
        if t_1 - t_0 > intervalo_alinhamento:
            print("hora de verificar alinhamento")
            estado.Trocar_estado(PARAR)
            sleep(tempo_para_parar)
            estado.Trocar_estado(funcoes.checar_alinhamento_pista_v1(camera, tolerancia_central, tolerancia_para_frente))  # Frente, GIRAR_ESQUERDA ou GIRAR_DIREITA
            while estado.Obter_estado_atual()  == GIRAR_ESQUERDA or estado.Obter_estado_atual() == GIRAR_DIREITA:
                print("desalinhado com a pista")
                sleep(tempo_do_passo[int(estado.Obter_estado_atual())])
                estado.Trocar_estado(funcoes.checar_alinhamento_pista_v1(camera, tolerancia_central, tolerancia_para_frente))
            print("REALINHOU!")
            t_0 = t_1 = time()
        else:
            print("ja estava alinhado com a pista")
            t_1 = time()

if __name__ == "__main__":
    try:
        print("Programa rodando... pode ser interrompido usando CTRL+C")
        Loop_obstaculo()
    except KeyboardInterrupt:
        print(" CTRL+C detectado. O loop foi interrompido.")
    estado.Trocar_estado(PARAR)
    print(estado)
