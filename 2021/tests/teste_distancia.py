import time
import numpy as np
import VL53L0X

ANG_GIRADO = 0.0
ANG_PITCH_CABECA = 30.0
ANG_CABECA_DEGRAU = 0.0
DIST_MIN_OBST_ATUAL = 52
DIST_MAXIMA = 50
# teste conflito v2
# teste v3
class Classe_distancia():
    def __init__(self):
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

def quando_parar_de_girar(sensor_distancia, vel_ang, largura_robo):
    global DIST_MIN_OBST_ATUAL
    global ANG_GIRADO
    
    intervalo_medicoes = 0.2
    mult_dist = 4
    mult_largura = 0.55
    mult_ang_girado = 0
    sensor_distancia.Get_distance()
    sensor_distancia.atual *= np.cos(ANG_PITCH_CABECA*np.pi/180)
    DIST_MIN_OBST_ATUAL = sensor_distancia.atual
    
    t_0 = t_1 = time.time()
    while True:
        time.sleep(intervalo_medicoes)
        sensor_distancia.Get_distance()
        sensor_distancia.atual *= np.cos(ANG_PITCH_CABECA*np.pi/180)
       # print("Dist: ", sensor_distancia.atual)
        if sensor_distancia.atual < sensor_distancia.anterior:
            DIST_MIN_OBST_ATUAL = sensor_distancia.atual
            t_0 = t_1
        print("TEMPO: ", t_1-t_0)
        if(sensor_distancia.atual > DIST_MAXIMA):    
            t_1 = time.time() - intervalo_medicoes/2
            theta_vel_ang = vel_ang*(t_1 - t_0)
            #theta_trigo = np.arccos(DIST_MIN_OBST_ATUAL/sensor_distancia.anterior)
            ANG_GIRADO = np.arctan2( DIST_MIN_OBST_ATUAL*np.tan(theta_vel_ang) + largura_robo*mult_largura, DIST_MIN_OBST_ATUAL)
           # ANG_GIRADO_TRIGO = np.arctan2( DIST_MIN_OBST_ATUAL*np.tan(theta_trigo) + largura_robo*mult_largura, DIST_MIN_OBST_ATUAL)
        #    print("ANG_GIRADO_VEL_ANG: ", ANG_GIRADO_VEL_ANG, "\nANG_GIRADO_TRIGO: ", ANG_GIRADO_TRIGO, "\n")
           # ANG_GIRADO = mult_ang_girado*ANG_GIRADO_TRIGO + (1-mult_ang_girado)*ANG_GIRADO_VEL_ANG
            intervalo_seguranca = ANG_GIRADO/vel_ang - (t_1 - t_0)
            time.sleep(intervalo_seguranca)
            break
        t_1 = time.time()
 #   print("ANG GIRADO: ", ANG_GIRADO)
    return PARAR

if __name__ == "__main__":
    dist = Classe_distancia()
    quando_parar_de_girar(dist, np.pi/18, 25)
