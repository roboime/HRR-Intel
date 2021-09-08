from main_2021_v1 import Atual
import serial
import RPi.GPIO as GPIO
import RTIMU
import VL53L0X
import pickle
import time
import math

## ideia: setar o angulo inicial como sendo a primeira leitura do sensor em vez de ser 0
class Classe_giroscopio():
    def __init__(self):
        ########################################## configurações do sensor giroscópio ##########################################
        SETTINGS_FILE = "/home/pi/giroscopio/RTEllipsoidFit/RTIMULib.ini"     
        settings = RTIMU.Settings(SETTINGS_FILE)                               
        self.giroscopio = RTIMU.RTIMU(settings)                                            
        self.giroscopio.IMUInit()               
        self.giroscopio.setSlerpPower(0.02)     
        self.giroscopio.setGyroEnable(True)     
        self.giroscopio.setAccelEnable(True)    
        self.giroscopio.setCompassEnable(True)  

        ###################################################### Constantes ######################################################                        
        self.intervalo_verificacoes = 0.1                                                        #intervalo total de verificação
        self.intervalo_poll = self.giroscopio.IMUGetPollInterval()                   #intervalo entre duas medidas do giroscópio
        self.angulo_yaw_inicial = 0
        self.angulo_yaw_limite = 10          #variação angular (em graus) limite entre o angulo_yaw atual e o angulo_yaw_inicial

        self.Save_config(self)

    def Save_config(self, obj):
        with open('IMU_config.pkl', 'wb') as outp:  
            pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)                             # guarda o objeto criado no arquivo .pkl
 
    def Obter_angulo_yaw(self):
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



class Classe_distancia():
    def __init__(self):
        ######################################### Configurações do sensor de distância #########################################
        self.sensor_distancia = VL53L0X.VL53L0X()                                 # Criando o objeto associado ao sensor VL53L0X
        self.sensor_distancia.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)     #configurando alcance e precisao do sensor
        
        self.Save_config(self)
        self.anterior = 100
        self.atual = 100

    def Save_config(self, obj):
        with open('VL53L0X_config.pkl', 'wb') as outp:  
            pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)                             # guarda o objeto criado no arquivo .pkl
    #ocorre divisao por 10 para passar para cm
    def Get_distance(self):
        self.anterior = self.atual
        self.atual = self.sensor_distancia.get_distance()/10
        return self.atual                             # retorna a distância até o obstáculo em cm



class Classe_porta_serial():
    def __init__(self):
        ################################################ Configurações da Rasp ################################################
        
        channel = 18                                                                                            #porta utilizada
        GPIO.setmode(GPIO.BCM)          
        GPIO.setup(channel, GPIO.OUT)

        ################################################ Configurações da MyRio ################################################
        porta = "/dev/ttyAMA0"                                                                             #nao é a porta AMA0**
        baudrate_myrio = 230400                                                                         #deve igualar a da myrio
        self.serial_output = serial.Serial(porta,baudrate_myrio)                   # porta serial que faz comunicação coma MyRio
        
        self.Save_config(self)

    def Save_config(self, obj):
        with open('MyRio_config.pkl', 'wb') as outp:  
            pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)                             # guarda o objeto criado no arquivo .pkl

    def Escrever_estado(self, state):
        self.serial_output.write(state)

class Classe_estado:
    def __init__(self):
        self.atual = "0"

    def Obter_estado_atual(self):
        return self.atual

    def Trocar_estado(self, state, myrio):
        self.atual = state
        myrio.Escrever_estado(state)
    
    def __str__(self):          #string associada ao objeto de "Classe_estado". Será mostrada ao printar um objeto desse tipo
        name = {    '0' : "PARAR",
                    '1' : "ANDAR",                      #Dicionário que associa o índice do estado ao nome
                    '2' : "GIRAR PARA ESQUERDA",
                    '3' : "GIRAR PARA DIREITA"
                    }
        need = {
            '0' : "Deve estar parado",
            '1' : "NAO ha necessidade de correcao",         #Dicionário que associa o índice do estado à necessidade de correção
            '2' : "Deve estar girando para esquerda",
            '3' : "Deve estar girando para direita"
        }
        atual = self.Obter_estado_atual()
        return "Estado atual: " + name[atual] + ".\nÍndice: " + str(atual) + ".\nCorreção: " + need[atual] + "\n"


def Load_config(filename):
    with open(filename, 'wb') as inp:
        return pickle.load(inp)                                        # retorna um objeto que esteja salvo em um arquivo .pkl

