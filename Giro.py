#!/usr/bin/env python
# coding: utf-8

# In[ ]:


"""
Created on Oct 2020
    Funçoes
    GetDistance
@author: Domingos
"""

######################## Libraries #############################

import VL53L0X              
import time                                


##"""Função"""
#Função cronômetro
def cronometro(t):
    import time
    start = time.time()
    for x in range(t):

        time.sleep(1)
        if time.time() - start > t:
            break
    return True
#A função giro fará o robo se alinhar a direção zero, então oq queremos é que o yaw volte ao ponto zero
def giro(ang):#Deixe como argumento aqui o próprio Yaw
    while 1:
        if abs(GetYaw())>1e-4
            break
    return 3
    

