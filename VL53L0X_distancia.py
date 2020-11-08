#!/usr/bin/env python
# coding: utf-8


"""
Created on Sept 2020
    Funçoes
    GetDistance

@author: Domingos
"""



######################## Libraries #############################

import board
import busio
import adafruit_vl53l0x                        




##"""Função"""
#Função que pede a distancia:
def Get_Distance(): 
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_vl53l0x.VL53L0X(i2c)
    return sensor.range
    
    return dist
    
