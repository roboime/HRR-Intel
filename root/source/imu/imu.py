import RTIMU

class SensorGiroscopio():
    def __init__(self):
        ########################################## configuracoes do sensor giroscopio ##########################################
        SETTINGS_FILE = "/home/pi/giroscopio/RTEllipsoidFit/RTIMULib.ini"     
        settings = RTIMU.Settings(SETTINGS_FILE)                               
        self.giroscopio = RTIMU.RTIMU(settings)                                            
        self.giroscopio.IMUInit()               
        self.giroscopio.setSlerpPower(0.02)     
        self.giroscopio.setGyroEnable(True)     
        self.giroscopio.setAccelEnable(True)    
        self.giroscopio.setCompassEnable(True)  

        ###################################################### Constantes ######################################################                        
        self.intervalo_verificacoes = 0.1                                                        #intervalo total de verificacao
        self.intervalo_poll = self.giroscopio.IMUGetPollInterval()                   #intervalo entre duas medidas do giroscopio
        self.angulo_yaw_inicial = self.__Calcular_angulo_yaw()
        self.angulo_yaw_limite = 10          #variacao angular (em graus) limite entre o angulo_yaw atual e o angulo_yaw_inicial

        #self.Save_config(self)

    
    def __Calcular_angulo_yaw(self):
        t_0 = time.time()
        t_1 = time.time()
        while (t_1 - t_0 < self.intervalo_verificacoes):
            t_1 = time.time()
            if self.giroscopio.IMURead():
                data = self.giroscopio.getIMUData()
                fusionPose = data["fusionPose"]
                angulo_yaw = math.degrees(fusionPose[2])
                time.sleep(self.intervalo_poll*1.0/1000.0)
        return angulo_yaw - self.angulo_yaw_inicial              # retorna o desvio em graus entre o angulo_yaw atual e o inicial 

    def Obter_angulo_yaw(self): return self.__Calcular_angulo_yaw() - self.angulo_yaw_inicial              # retorna o desvio em graus entre o angulo_yaw atual e o inicial 

