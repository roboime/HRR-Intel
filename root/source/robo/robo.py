
class Robo:
    def __init__(self, estado, imu, sensor_distancia, visao):
        self.estado = estado
        self.imu = imu
        self.sensor_distancia = sensor_distancia
        self.visao = visao
        
    def corrida():
        while(True):
            self.estado.trocar_estado(ANDAR)
            alinhamento(self)
    def corrida_obstaculo():
        while(True):
            self.estado.trocar_estado(ANDAR)
            alinhamento(self)
            desvio_obstaculo(self)
    def corrida_degrau():
        while(True):
            self.estado.trocar_estado(ANDAR)
            alinhamento(self)
            desvio_degrau(self)
        