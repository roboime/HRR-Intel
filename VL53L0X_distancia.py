#!/usr/bin/env python
# coding: utf-8


"""
Created on Sept 2020
    Funçoes
    GetDistance

@author: Domingos
"""



######################## Libraries #############################

import VL53L0X              
import time                                




##"""Função"""
#Função que pede a distancia:
def Get_Distance(sensor): #Coloque no argumento uma entrada do tipo (tof = VL53L0X.VL53L0X(address=0x29))
    sensor.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
    dist = sensor.get_distance()/float(10)
    
    return dist
    
