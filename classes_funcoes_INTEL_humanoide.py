# -*- coding: utf-8 -*-
"""
Arquivo contendo as classes e funçoes utilizadas no arquivo main_INTEL_humanoid_2020.py

@autor: Mateus Souza
"""

######################## BIBLIOTECAS #############################
from math import degrees
import time
import VL53L0X
import IMU_yaw as Direcao
import numpy as np
import line_detector      #arquivos relacionados a visao computacional
import ob_detector
import cv2
######################## CONSTANTES #############################

intervalo = 0.1       #intervalo, em segundos, aceitavel entre as verificações de obstaculo e direção
yaw_0 = 0         #direçao da pista de corrida (direçao padrao)
Yaw = ([0])         #direçao instantanea de movimento do robo na pista, armazenada em formato lista
limDyaw = 10    #limite aceitavel, em graus, para diferença entre a direçao instantanea e a direçao correta
Dist = ([1000])       #menor distancia instantanea obtida pelo sensor, armazenada em formato lista
Vmed = 5                #velocidade media do robo, usada como argumento da funçao Desvio()
Dmin = 20               #Distancia, em cm, a partir da qual o obstáculo é considerado "detectado" pra iniciar desvio

tof = VL53L0X.VL53L0X()         # Criando o objeto associado ao sensor VL53L0X
tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)  #configurando alcance e precisao do sensor

######################## CLASSES #############################

class estado:
    """ classe para armazenar o estado instantaneo do robo humanoide """
    
    def __init__ (self, initName):
        
        self.name = initName #armazena o nome do estado, associando ele a um numero
                             #0: estado ANDAR #1: estado GIRAR PARA ESQUERDA
                             #2: estado GIRAR PARA DIREITA #3: estado PARAR                
        #definindo o atributo state:  armazena se há necessidade ou não de corrigir o estado (0 ou 1)
        if (initName == 1):
            self.state = 0 #se o estado for ANDAR, nao há necessidade de correçao
        else:
            self.state = 1
            
    def getState(self):         #retorna se há necessidade de correçao
        return (self.state)
    
    def getName(self):          #retorna o numero associado ao estado
        print("estado atual:")
        print(self.state)
        return(self.name)
    
    def __str__(self):          #string associada ao objeto do tipo "estado", será mostrada ao printar um objeto desse tipo
        if (self.name == 0):
            need = "  NAO ha necessidade de correcao"
            nome = "ANDAR\n"
        elif (self.name == 1):
            need ="  Ha necessidade de correcao"
            nome = "GIRAR PARA ESQUERDA\n"
        elif (self.name == 2):
            need ="  Ha necessidade de correcao"
            nome = "GIRAR PARA DIREITA\n"
        elif (self.name == 3):
            need ="  Ha necessidade de correcao"
            nome = "PARAR\n"
        else:
            need = "  Corrija o estado manualmente"
            nome = "Inexistente\n"            
        return "  Numero associado ao estado atual: " + str(self.name) +  ".\n  Estado: " + nome + need
    
######################## FUNÇOES #############################  
    
"""A função giro fará o robo parar de girar quando se alinhar a direção zero, então o que queremos
 é que o yaw volte ao yaw inicial yaw_0"""
def giro(ang):#Deixe como argumento aqui o próprio Yaw
    while True:
        print("ainda nao corrigiu direcao")
        if abs(Direcao.get_yaw()) <1:
            break
    return 3


"""Funçao auxiliar cronometro"""
def cronometro(t): #t é o tempo em segundos 
    start = time.time()
    for x in range(t):
        time.sleep(1)
        if time.time() - start > t:
            break
    return True


"""Apos avistar um alvo a uma distancia d, o robo deu uma virada até parar de vizualiza-lo
Por meio de geometria, pode-se ver que a distancia que ele deve andar é d*cos(12,5-yaw)/cos(yaw)
Assim iremos criar uma função cujos argumentos são a distancia avistada e o angulo yaw já medido
Retornaremos 3 para ele parar de andar, ou seja, após ele ultrapassar o obstáculo"""
def Walk_Detour(Dist, Yaw): #A velocidade Vmed será medida e utilisaremos a velocidade média
   d=Dist[0]*np.cos((np.pi /180 )*(12.5-Yaw[0]))/np.cos(np.pi/180 *Yaw[0])
   t=(d)/Vmed

   while True:
       print("ainda nao ultrapassou")
        if cronometro(t):
            break
   return 3

"""Funçao que mantem o robo girando até obter a direçao de desvio do obstaculo"""
def direcao_desvio(Yaw, Dist):
    #distancia_0 = 0
    Dist[0] = tof.get_distance()/10      #começa atualizando a distancia
    while True:
        print("ainda nao desviou")
        distancia_atual = Dist[0]               
        if distancia_atual > Dmin:
            Dist[0] = distancia_atual
            Yaw[0] = Direcao.get_yaw()
            print("direçao de desvio obtida")
            return 3
        time.sleep(0.1)                     #intervalo de segurança
        Dist[0] = tof.get_distance()/10  #atualiza o valor da distancia
        Yaw[0] = Direcao.get_yaw()           #atualiza a direcao
        
"""Funçao auxiliar, ocupa lugar da funçao que determina o lado para o qual deve desviar"""
def Decisao_desvio():
    print("deve girar para ESQUERDA")
    return 1
    
    
#"""funçao de teste"""
#def teste_v():
#    print(Dmin)             # testando o uso de variaveis declaradas fora da funçao
#    print ("deveria printar 46")    #funcionou
