#import serial
#import RPi.GPIO as GPIO
import RTIMU
#import VL53L0X
import pickle
import time
import math


class giroscopio():
    def __init__(self):
        SETTINGS_FILE = "/home/pi/giroscopio/RTEllipsoidFit/RTIMULib.ini"     
        settings = RTIMU.Settings(SETTINGS_FILE)                               
        self.giroscopio = RTIMU.RTIMU(settings)                                            
        self.giroscopio.IMUInit()               
        self.giroscopio.setSlerpPower(0.02)     
        self.giroscopio.setGyroEnable(True)     
        self.giroscopio.setAccelEnable(True)    
        self.giroscopio.setCompassEnable(True)  
        
        self.intervalo_verificacoes = 0.1                                                        
        self.intervalo_poll = self.giroscopio.IMUGetPollInterval()                   
        self.angulo_yaw_inicial = 0
        self.angulo_yaw_limite = 10          

        self.Save_config(self)

    def Save_config(self, obj):
        with open('IMU_config.pkl', 'wb') as outp:  
            pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)    
 
    def Obter_angulo_yaw(self):
        t_0 = time.time()
        t_1 = time.time()
        angulo_yaw = 0
        while (t_1 - t_0 < self.intervalo_verificacoes):
            t_1 = time.time()
            angulo_yaw = self.angulo_yaw_inicial
            if self.giroscopio.IMURead():
                print("leu")
                data = self.giroscopio.getIMUData()
                fusionPose = data["fusionPose"]
                angulo_yaw = math.degrees(fusionPose[2])
                time.sleep(self.intervalo_poll*1.0/1000.0)
            else: print("nao leu")
        return angulo_yaw - self.angulo_yaw_inicial            

giro = giroscopio()

while True:
    print(giro.Obter_angulo_yaw())