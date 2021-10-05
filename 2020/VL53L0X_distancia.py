#!/usr/bin/env python
# coding: utf-8


"""
Created on Sept 2020
    Funçoes
    GetDistance

@author: Domingos
"""



######################## Libraries #############################

import time
import VL53L0X                       




##"""Função"""
#Função que pede a distancia:
def Get_Distance(): 
    # Criar um objeto VL53L0X
    tof = VL53L0X.VL53L0X()
 
    # Colocar o modo de medida
    tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
    distance = tof.get_distance()
    
    return distance
    
