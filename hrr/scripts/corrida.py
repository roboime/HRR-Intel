from hrr.hrr.robo import robo
from hrr.hrr.estado import estado
from hrr.hrr.imu_6050 import imu 
from hrr.hrr.visao import visao
from hrr.hrr.sensor_distancia import sensor_distancia

def main():
    robo_corrida = robo.Robo(estado = estado.Estado(),
        imu = imu.Imu6050(),
        visao = visao.Visao(),
        alinhamento= robo.Alinhamento_imu(),
        desvio= robo.DesvioObstaculo(),
        sensor_distancia= sensor_distancia.SensorDistancia())
    try:
        robo_corrida.corrida()
    except KeyboardInterrupt:
        print(" CTRL+C detectado. O loop foi interrompido.")
        robo.estado.trocar_estado("PARAR")
        