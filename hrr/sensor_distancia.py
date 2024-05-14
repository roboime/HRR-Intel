import VL53L0X
import constantes as c
from hrr.hardware import Hardware


class SensorDistancia(Hardware):
    def __init__(self):
        ######################################### Configuracoes do sensor de distancia #########################################
        # Criando o objeto associado ao sensor VL53L0X
        self.sensor_distancia = VL53L0X.VL53L0X()
        # configurando alcance e precisao do sensor
        self.sensor_distancia.start_ranging(
            VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

        # self.Save_config(self)
        self.anterior = c.DIST_MAXIMA
        self.atual = c.DIST_MAXIMA

    # ocorre divisao por 10 para passar para cm
    def get_distance(self):
        try:
            self.anterior = self.atual
            self.atual = self.sensor_distancia.get_distance()/10
            # retorna a distancia ate o obstaculo em cm
            return self.atual
        except KeyboardInterrupt:
            print("ctrl c detectado, saindo do get distance")

    def next_state(self): pass
