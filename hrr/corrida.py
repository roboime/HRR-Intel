from hrr.robo.robo import Robo
from hrr.estado.estado import Estado
from hrr.imu_6050.imu import Imu6050 
from hrr.visao.visao import Visao
from hrr.sensor_distancia.sensor_distancia import SensorDistancia

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
        