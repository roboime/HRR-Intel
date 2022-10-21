"""Modulo responsavel pela leitura dos dados do sensor IMU"""
import smbus
from math import degrees
from time import time, sleep
import constantes as c

bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards

class Imu6050():
    """Classe que instancia um objeto da biblioteca RTIMU para obtencao e
    analise de dados do sensor IMU.
    """
    def __init__(self):
        """Instancia um objeto da classe RTIMU e o configura a partir da calibracao feita"""
        # Constantes
        
        self.angulo_yaw_referencia = 0.0
        bus.write_byte_data(c.DEVICE_ADDRESS, c.SMPLRT_DIV, 7) 
        bus.write_byte_data(c.DEVICE_ADDRESS, c.PWR_MGMT_1, 1)
        bus.write_byte_data(c.DEVICE_ADDRESS, c.CONFIG, 0)
        bus.write_byte_data(c.DEVICE_ADDRESS, c.GYRO_CONFIG, 24)
        bus.write_byte_data(c.DEVICE_ADDRESS, c.INT_ENABLE, 1) 
        print("Gyro Inicializado")      
        

    def calcular_w_yaw(self):
        """Retorna o angulo yaw atual em graus em relacao ao zero padrao da calibracao"""
        gyro_z = self._read_raw_data(c.GYRO_ZOUT_H)
        Gz = gyro_z/c.C
        return Gz

    def delta_angulo_yaw(self, ang):
        """Retorna o desvio em graus entre o angulo yaw atual e o angulo yaw de referencia"""
        return ang - self.angulo_yaw_referencia
    def mudar_referencia(self, ang):
        """Muda o angulo de referencia para o calculo do delta_angulo_yaw()"""
        self.angulo_yaw_referencia = ang

    def get_referencia(self):
        return self.angulo_yaw_referencia

    
    def _read_raw_data(self, addr):
	    #Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(c.DEVICE_ADDRESS, addr)
        low = bus.read_byte_data(c.DEVICE_ADDRESS, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value
