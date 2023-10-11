import VL53L0X
import constantes as c

class SensorDistancia():
    def __init__(self):
        ######################################### Configuracoes do sensor de distancia #########################################
        self.sensor_distancia = VL53L0X.VL53L0X()                                 # Criando o objeto associado ao sensor VL53L0X
        self.sensor_distancia.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)     #configurando alcance e precisao do sensor
        
        #self.Save_config(self)
        self.anterior = c.DIST_MAXIMA
        self.atual = c.DIST_MAXIMA

    #ocorre divisao por 10 para passar para cm
    def get_distance(self):
        try:
            self.anterior = self.atual
            self.atual = self.sensor_distancia.get_distance()/10
            return self.atual                             # retorna a distancia ate o obstaculo em cm
        except KeyboardInterrupt:
            print("ctrl c detectado, saindo do get distance")
            
    
