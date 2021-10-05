import time
import numpy as np
import VL53L0X

class Classe_distancia():
    def __init__(self):
        self.sensor_distancia = VL53L0X.VL53L0X()                                 # Criando o objeto associado ao sensor VL53L0X
        self.sensor_distancia.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)     #configurando alcance e precisao do sensor
        
        #self.Save_config(self)
        self.anterior = 100
        self.atual = 100

    #ocorre divisao por 10 para passar para cm
    def Get_distance(self):
        self.anterior = self.atual
        self.atual = self.sensor_distancia.get_distance()/10
        return self.atual                             # retorna a distancia ate o obstaculo em cm

sensor_distancia = Classe_distancia()
DIST_MIN_OBST_ATUAL = 46.0
largura_robo = 25.0
vel_ang = np.pi/18

tempo1 = tempo2 = time.time()
while (tempo2 - tempo1 < 2):
    print(sensor_distancia.Get_distance())
    tempo2 = time.time()

intervalo_medicoes = 0.1
mult_dist = 1
mult_largura = 0.75
mult_ang_girado = 0.5
DIST_MIN_OBST_ATUAL = sensor_distancia.Get_distance()

t_0 = t_1 = time.time()
while True:
    time.sleep(intervalo_medicoes)
    dist = sensor_distancia.Get_distance()
    print(dist)
    if sensor_distancia.atual < sensor_distancia.anterior:
        DIST_MIN_OBST_ATUAL = sensor_distancia.atual
        t_0 = t_1
    if(abs(sensor_distancia.atual - sensor_distancia.anterior) > mult_dist*sensor_distancia.anterior):    
        t_1 = time.time() - intervalo_medicoes/2
        theta_vel_ang = vel_ang*(t_1 - t_0)
        theta_trigo = np.arccos(DIST_MIN_OBST_ATUAL/sensor_distancia.anterior)
        ANG_GIRADO_VEL_ANG = np.arctan2( DIST_MIN_OBST_ATUAL*np.tan(theta_vel_ang) + largura_robo*mult_largura, DIST_MIN_OBST_ATUAL)
        ANG_GIRADO_TRIGO = np.arctan2( DIST_MIN_OBST_ATUAL*np.tan(theta_trigo) + largura_robo*mult_largura, DIST_MIN_OBST_ATUAL)
        print("ANG_GIRADO_VEL_ANG: ", ANG_GIRADO_VEL_ANG, "\nANG_GIRADO_TRIGO: ", ANG_GIRADO_TRIGO, "\n")
        ANG_GIRADO = mult_ang_girado*ANG_GIRADO_TRIGO + (1-mult_ang_girado)*ANG_GIRADO_VEL_ANG
        intervalo_seguranca = ANG_GIRADO/vel_ang - (t_1 - t_0)
        time.sleep(intervalo_seguranca)
        break
        
print("Saimo familia")
