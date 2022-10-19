from robo import Robo
from estado import Estado
from imu6050 import Imu6050 
from visao import Visao
from sensor_distancia import SensorDistancia

def main():
    robo_corrida = Robo(estado = Estado(),
        imu = Imu6050(),
        visao = Visao(),
        alinhamento= Robo.Alinhamento_imu(),
        desvio= Robo.DesvioObstaculo(),
        sensor_distancia= SensorDistancia())
    try:
        robo_corrida.corrida()
    except KeyboardInterrupt:
        print(" CTRL+C detectado. O loop foi interrompido.")
        Robo.estado.trocar_estado("PARAR")
        