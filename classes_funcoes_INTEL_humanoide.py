# -*- coding: utf-8 -*-
"""
Arquivo contendo as classes e funçoes utilizadas no arquivo main_INTEL_humanoid_2020.py

@autor: Mateus Souza
"""

######################## BIBLIOTECAS #############################
import serial
from math import degrees
from time import sleep
#import RTIMU
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
        return(self.name)
    
    def __str__(self):
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