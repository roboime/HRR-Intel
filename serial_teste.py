# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 14:06:41 2020

@author: Mateus
"""

######################## BIBLIOTECAS #############################
import time
import serial
import RPi.GPIO as GPIO
######################## CONSTANTES #############################
channel = 14                    #porta utilizada (TX)
porta = "/dev/ttyS0"
baudrate = 9600                 #deve igualar a da myrio
GPIO.setmode(GPIO.BCM)          #configuraçoes das rasp
GPIO.setup(channel, GPIO.OUT)   #configurando a porta como modo saida

ser = serial.Serial(porta,baudrate) 
baudrate = 9600

try:
    while True:
        ser.write(3)
        print("numero 3 enviado")
        time.sleep(2)
        
except KeyboardInterrupt:
    print(" CTRL+C detectado. O loop foi interrompido.")




