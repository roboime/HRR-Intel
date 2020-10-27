#!/usr/bin/env python
# coding: utf-8

# In[ ]:


"""
Created on Oct 2020
    Funçoes
    giro
@author: Domingos
"""

######################## Libraries #############################

import VL53L0X              
import time                                


##"""Função"""

#A função giro fará o robo se alinhar a direção zero, então oq queremos é que o yaw volte ao ponto zero
def giro(ang):#Deixe como argumento aqui o próprio Yaw
    while 1:
        if abs(GetYaw())>1:
            break
    return 3
    

