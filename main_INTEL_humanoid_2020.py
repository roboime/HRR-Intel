# -*- coding: utf-8 -*-
"""
Função principal do projeto Humanoide RoboIME 2020

Tomada de decisão para transição entre os estados

Feita para ser utilizada em Raspberry Pi

Primeira versao

Ainda não importa os arquivos que terão as funções Decisao_desvio(), enviarestado(),
direcao_desvio nem Desvio()

@autores: Mateus Souza, Mateus Seppe, Matheus Domingos e Clarisse Rufino
"""

######################## BIBLIOTECAS #############################
import time
from math import degrees
import RTIMU
import RPi.GPIO as GPIO
import string
import classes_main_INTEL_humanoide as Estado
######################## CONSTANTES #############################
channel = 18                    #porta utilizada
GPIO.setmode(GPIO.BCM)          #configuraçoes das rasp
GPIO.setup(channel, GPIO.OUT)
intervalo = 1       #intervalo, em segundos, aceitavel entre as verificações de obstaculo e direção
yaw_0 = 0         #direçao da pista de corrida
yaw = 0         #direçao instantanea do robo
limDyaw = 10    #limite aceitavel para diferença entre a direçao instantanea e a direçao correta
dist = 1000       #menor distancia instantanea obtida pelo sensor
ANDAR=0                 #
GIRAR_ESQUERDA=1        #legenda dos estados
GIRAR_DIREITA=2         #
PARAR=3                 #

######################## Função main ############################
Atual = Estado.estado(3) #iniciando no estado PARAR
enviarestado()          #envia o estado para a placa myrio - diz qual arquivo de estado abrir e rodar nos motores


print("Programa rodando... pode ser interrompido usando CTRL+C")
try:                    #utilizado pra possibilitar o programa ser interrompido
    while True:
        print("Heavy task!")
        Atual = Estado.estado(0)        #Começar a andar
        enviarestado()                 
        dist = Distancia.getDistance()
        yaw = Direcao.getYaw() - yaw_0
        
        if (dist<=47):
            print ("obstaculo detectado")
            Atual = Estado.estado(3)    #parar para começar a desviar do obstaculo
            enviarestado()
            Atual = Estado.estado(Decisao_desvio()) #obtem o lado para o qual deve girar e retorna 1 ou 2 (esquerda ou direita)
            enviarestado()
            Atual = Estado.estado(direcao_desvio)    #retorna 3 depois que obter a direcao de desvio apos girar suficiente
            enviarestado()
            Atual = Estado.estado(0)                #volta a andar pra ultrapassar o obstaculo
            enviarestado()
            Atual = Estado.estado(Desvio())     #funçao retorna "3" dps que o robo terminar de ultrapassar
            enviarestado()
            print("obstaculo ultrapassado")
            
        if ((yaw-yaw_0) < (-limDyaw)):  
            print("direçao incorreta - virado para DIREITA")
            Atual = Estado.estado(2)    #se a diferença for negativa, tem que girar para direita
            enviarestado()
            Atual = Estado.estado(corrigirDirecao()) #funçao retorna "3" dps que o robo corrigir a direçao
            print("direçao corrigida")
        
        if ((yaw-yaw_0) > limDyaw):
            print("direçao incorreta - vire para ESQUERDA")
            Atual = Estado.estado(1)    #se a diferença for positiva, tem que girar para esquerda
            enviarestado()
            Atual = Estado.estado(corrigirDirecao()) #funçao retorna "3" dps que o robo corrigir a direçao
            enviarestado()
            print("direçao corrigida")
            
        time.sleep(intervalo)
        
except KeyboardInterrupt:
    print(" CTRL+C detectado. O loop foi interrompido.")

#print("Continuando execução do código")
Atual = Estado.estado(3)        #parar os motores por questao de segurança
enviarestado()
print(Atual)
    