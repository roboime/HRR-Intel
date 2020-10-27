#!/usr/bin/env python
# coding: utf-8

# In[ ]:


"""
Created on Oct 2020
    Funçoes
    Cronometro
    Walk_Detour
@author: Domingos
"""

######################## Libraries #############################

import VL53L0X              
import time                                


##"""Função"""
#Função cronômetro

def cronometro(t): #t é o tempo em segundos 
    import time
    start = time.time()
    for x in range(t):
        time.sleep(1)
        if time.time() - start > t:
            break
    return True
#Ao avistar um alvo a uma distancia d, o robo deve dar uma virada até parar de vizualiza-lo
#Por meio de geometria, pode-se ver que a distancia que ele deve andar é d*cos(12,5-yaw)/cos(yaw)
#Assim iremos criar uma função cujos argumentos são a distancia avistada e o angulo yaw já medido
#Retornaremos 3 para ele parar

def Walk_Detour(d, yaw, vel): #A velocidade vel será medida e utilisaremos a velocidade média
    t=(d)/vel
    
    while 1:
        if cronometro(t):
            break
    return 3


# In[ ]:




