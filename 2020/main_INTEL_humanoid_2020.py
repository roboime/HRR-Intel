# -*- coding: utf-8 -*-
"""
Função principal do projeto Humanoide RoboIME 2020

Tomada de decisão para transição entre os estados
Feita para ser utilizada em Raspberry Pi
Primeira versao

    OBSERVAÇÕES:
    
Ainda não importa os arquivos que terão as funções Decisao_desvio(), corrigirDirecao(),
direcao_desvio() nem Desvio().

O angulo de visão do sensor VL53L0X é de 25°

Decisao_desvio()  --> funçao que determina para qual lado o robo tem que girar para desviar (SEPPE)
direcao_desvio    --> funçao que mantem o robo girando até atingir a direçao correta pra realizar o desvio (CLARISSE)
Desvio()          --> funçao que mantem o robo andando até ultrapassar o obstaculo desviado  (DOMINGOS)
corrigirDirecao() --> funçao que mantem o robo girando até voltar para a direçao padrao da pista (DOMINGOS)


@autores: Mateus Souza, Mateus Seppe, Matheus Domingos e Clarisse Rufino
"""

######################## BIBLIOTECAS #############################
import time
import serial
import math
import RTIMU
import get_yaw as Direcao
import RPi.GPIO as GPIO
import classes_funcoes_INTEL_humanoide as Estado
import VL53L0X
######################## CONSTANTES #############################
channel = 18                    #porta utilizada
porta = "/dev/ttyAMA0"          #nao é a porta AMA0**
baudrate = 230400                 #deve igualar a da myrio
GPIO.setmode(GPIO.BCM)          #configuraçoes das rasp
GPIO.setup(channel, GPIO.OUT)

tof = VL53L0X.VL53L0X()         # Criando o objeto associado ao sensor VL53L0X
tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)  #configurando alcance e precisao do sensor

SETTINGS_FILE = "/home/pi/IMU/RTEllipsoidFit/RTIMULib.ini"     #
                                                                #iniciando o sensor giroscopio
s = RTIMU.Settings(SETTINGS_FILE)                               #
imu = RTIMU.RTIMU(s)                                            #

imu.IMUInit()               #
imu.setSlerpPower(0.02)     #   confirgurações giroscopio
imu.setGyroEnable(True)     #
imu.setAccelEnable(True)    #
imu.setCompassEnable(True)  #

poll_interval = imu.IMUGetPollInterval()    #configuraçao de intervalo de giroscopio


intervalo = 0.1       #intervalo, em segundos, aceitavel entre as verificações de obstaculo e direção
dt = 1              #intervalo para facilitar teste da main enquanto nao temos o robo
yaw_0 = 0         #direçao da pista de corrida (direçao padrao)
Yaw = ([0])         #direçao instantanea de movimento do robo na pista, armazenada em formato lista
limDyaw = 10    #limite aceitavel, em graus, para diferença entre a direçao instantanea e a direçao correta
Dist = ([100])       #menor distancia instantanea obtida pelo sensor, armazenada em formato lista
Tmed = 5                #tempo medio, em segundos, pro robo andar 2cm, usado como argumento da funçao Desvio()
Dmin = 46               #Distancia, em cm, a partir da qual o obstáculo é considerado "detectado" pra iniciar desvio

ANDAR="0"                 #
GIRAR_ESQUERDA="1"        #legenda dos estados
GIRAR_DIREITA="2"         #
PARAR="3"                 #

ser = serial.Serial(porta,baudrate)       #configura a porta serial para fazer comunicação com a myrio


######################## Função main ############################
Atual = Estado.estado("3") #iniciando no estado 3 - PARAR
#ser.write(Atual.getName()) #envia o estado atual pra porta serial, pra ser lido depois pela myrio

print("Programa rodando... pode ser interrompido usando CTRL+C")
try:                    #utilizado pra possibilitar o programa ser interrompido
    while True:
        print("Estado padrao")
        Atual = Estado.estado(0)        #Começar a andar
        ser.write(Atual.getName())    
             
        Dist[0] = tof.get_distance()/10 #distancia obtida pelo sensor em centimetros
        Yaw[0] = (Direcao.get_yaw(intervalo)-yaw_0)
        
        """if (Dist[0] <= Dmin):
            print ("obstaculo detectado")
            Atual = Estado.estado("3")    #parar para começar a desviar do obstaculo
            ser.write(Atual.getName())
            
            time.sleep(dt) #apenas pra teste
            
            Atual = Estado.estado(Estado.Decisao_desvio()) #obtem o lado para o qual deve girar e retorna 1, 2 ou 0
            ser.write(Atual.getName())                      #(esquerda, direita ou para frente)
            
            time.sleep(dt) #apenas pra teste
            
            if (Atual.getName() == "1" || Atual.getName()=="2"): #Se nao for um ou dois, basta seguir em frente           
                Atual = Estado.estado(Estado.direcao_desvio(Yaw,Dist))    #retorna 3 depois que obter a direcao de desvio apos girar suficiente
                ser.write(Atual.getName())
 Célula de               
 detecçao e     time.sleep(dt) #apenas pra teste
 desvio de  
 obstaculo      Atual = Estado.estado("0")                #volta a andar pra ultrapassar o obstaculo
                ser.write(Atual.getName())
                
                time.sleep(dt) #apenas pra teste
                
                Atual = Estado.estado(Estado.Walk_Detour(Dist,Yaw))     #funçao retorna "3" dps que o robo terminar de ultrapassar, alem de alterar os valores
                ser.write(Atual.getName())                  # de Yaw e Dist obtidos no fim do processo
                
            print("obstaculo ultrapassado")
            """
            
            
        if ((Yaw[0]) < (-limDyaw)):  
            print("direçao incorreta - virado para DIREITA")
            Atual = Estado.estado("2")    #se a diferença for negativa, tem que girar para direita
            ser.write(Atual.getName())
            
            time.sleep(dt) #apenas pra teste
            
            Atual = Estado.estado(Estado.giro(limDyaw)) #funçao retorna "3" dps que o robo corrigir a direçao
            ser.write(Atual.getName())
            
            time.sleep(dt) #apenas pra teste
            
            print("direçao corrigida")
        
        if ((Yaw[0]) > limDyaw):
            print("direçao incorreta - vire para ESQUERDA")
            Atual = Estado.estado("1")    #se a diferença for positiva, tem que girar para esquerda
            ser.write(Atual.getName())
            
            Atual = Estado.estado(Estado.giro(limDyaw)) #funçao retorna "3" dps que o robo corrigir a direçao
            ser.write(Atual.getName())
            print("direçao corrigida")
            
        
except KeyboardInterrupt:
    print(" CTRL+C detectado. O loop foi interrompido.")

Atual = Estado.estado("3")        #parar os motores por questao de segurança
ser.write(Atual.getName())
print(Atual)
    
