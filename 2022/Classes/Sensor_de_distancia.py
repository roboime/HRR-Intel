


import VL53L0X
from constantes import *


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
        try:
            self.anterior = self.atual
            self.atual = self.sensor_distancia.get_distance()/10
            return self.atual                             # retorna a distancia ate o obstaculo em cm
        except KeyboardInterrupt:
            print("ctrl c detectado, saindo do get distance")
            