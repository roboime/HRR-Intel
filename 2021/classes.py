import serial
import RPi.GPIO as GPIO
import RTIMU
import VL53L0X
import time
import math
import picamera
import os

ANDAR="0"                 
GIRAR_ESQUERDA="1"        
GIRAR_DIREITA="2"         
PARAR="3"
SUBIR = "4"
DESCER = "5"

DIST_MAXIMA = 50

class Classe_camera():
    def __init__(self):
        self.camera = picamera.PiCamera()
        self.intervalo_foto = 2.5
        self.indice_atual = 0
        self.path_pasta = os.path.dirname(os.path.abspath(__file__))
        self.path_atual = self.path_pasta + "1.jpg"

    def Take_photo(self):
        self.camera.start_preview()
        time.sleep(self.intervalo_foto)
        try:
            self.path_atual = "/home/pi/Pictures/imagem_main" + str(self.indice_atual) + ".jpg"
            print(" foto tirada em " + self.path_atual)
            self.camera.capture(self.path_atual)
            self.camera.stop_preview()
            self.indice_atual = (self.indice_atual + 1) % 10
            print("Saindo do Take_photo()")
            return self.path_atual
        except KeyboardInterrupt: self.camera.stop_preview()


    def parar_fotografar(self, estado, myrio):
        atual = estado.Obter_estado_atual()
        estado.Trocar_estado(PARAR, myrio)
        img = self.Take_photo()
        estado.Trocar_estado(atual, myrio)
        return img

class Classe_giroscopio():
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



class Classe_distancia():
    def __init__(self):
        ######################################### Configuracoes do sensor de distancia #########################################
        self.sensor_distancia = VL53L0X.VL53L0X()                                 # Criando o objeto associado ao sensor VL53L0X
        self.sensor_distancia.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)     #configurando alcance e precisao do sensor
        
        #self.Save_config(self)
        self.anterior = DIST_MAXIMA
        self.atual = DIST_MAXIMA

    #ocorre divisao por 10 para passar para cm
    def Get_distance(self):
        self.anterior = self.atual
        self.atual = self.sensor_distancia.get_distance()/10
        return self.atual                             # retorna a distancia ate o obstaculo em cm



class Classe_porta_serial():
    def __init__(self):
        ################################################ Configuracoes da Rasp ################################################
        
        channel = 18                                                                                            #porta utilizada
        GPIO.setmode(GPIO.BCM)          
        GPIO.setup(channel, GPIO.OUT)

        ################################################ Configuracoes da MyRio ################################################
        porta = "/dev/ttyAMA0"                                                                             #nao e a porta AMA0**
        baudrate_myrio = 230400                                                                         #deve igualar a da myrio
        self.serial_output = serial.Serial(porta,baudrate_myrio)                   # porta serial que faz comunicacao coma MyRio
        
        #self.Save_config(self)

    def Escrever_estado(self, state):
        self.serial_output.write(state)

class Classe_estado:
    def __init__(self, myrio):
        self.atual = PARAR
        self.Trocar_estado(PARAR, myrio)

    def Obter_estado_atual(self):
        return self.atual

    def Trocar_estado(self, state, serial_obj):
        self.atual = state
        serial_obj.Escrever_estado(state)
    
    def __str__(self):          #string associada ao objeto de "Classe_estado". Sera mostrada ao printar um objeto desse tipo
        name = {    ANDAR : "ANDAR",
                    GIRAR_ESQUERDA : "GIRAR PARA A ESQUERDA",                      #Dicionario que associa o indice do estado ao nome
                    GIRAR_DIREITA : "GIRAR PARA A DIREITA",
                    PARAR : "PARAR",
                    SUBIR : "SUBIR",
                    DESCER : "DESCER"
                }
        need = {
            ANDAR : "NAO ha necessidade de correcao",   #Dicionario que associa o indice do estado a necessidade de correcao
            GIRAR_ESQUERDA : "Deve estar girando para esquerda",     
            GIRAR_DIREITA : "Deve estar girando para direita",
            PARAR : "Deve estar parado",
            SUBIR : "Deve estar subindo o degrau",
            DESCER : "Deve estar descendo o degrau"
                }
        atual = self.Obter_estado_atual()
        return "Estado atual: " + name[atual] + ".\nindice: " + str(atual) + ".\nCorrecao: " + need[atual] + ".\n\n"
