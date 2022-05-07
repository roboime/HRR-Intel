import RTIMU
from time import time, sleep
from math import degrees
import constantes as c

class Imu():
    def __init__(self):
        ########################################## configuracoes do sensor giroscopio ##########################################
        settings = RTIMU.Settings(c.SETTINGS_FILE)                               
        self.giroscopio = RTIMU.RTIMU(settings)                                            
        self.giroscopio.IMUInit()               
        self.giroscopio.setSlerpPower(0.02)     
        self.giroscopio.setGyroEnable(True)     
        self.giroscopio.setAccelEnable(True)    
        self.giroscopio.setCompassEnable(True)  

        ###################################################### Constantes ######################################################                        
        self.intervalo_verificacoes = 0.1                                                        #intervalo total de verificacao
        self.intervalo_poll = self.giroscopio.IMUGetPollInterval()                   #intervalo entre duas medidas do giroscopio
        self.angulo_yaw_referencia = self.__calcular_angulo_yaw()

        #self.Save_config(self)

    def __calcular_angulo_yaw(self):
        t_0 = time()
        t_1 = time()
        while (t_1 - t_0 < self.intervalo_verificacoes):
            t_1 = time()
            if self.giroscopio.IMURead():
                data = self.giroscopio.getIMUData()
                fusionPose = data["fusionPose"]
                angulo_yaw = degrees(fusionPose[0]) # yaw corresponde ao fusion pose do eixo x (imu esta na vertical, com eixo x para cima)
                sleep(self.intervalo_poll*1.0/1000.0)
        return angulo_yaw              # retorna o desvio em graus entre o angulo_yaw atual e o inicial 

    def delta_angulo_yaw(self): return self.__calcular_angulo_yaw() - self.angulo_yaw_referencia              # retorna o desvio em graus entre o angulo_yaw atual e o inicial 
    def mudar_referencia(self): self.angulo_yaw_referencia = self.__calcular_angulo_yaw()
    def obter_angulo_yaw(self): self.__calcular_angulo_yaw()
    

