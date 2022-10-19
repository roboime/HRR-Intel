"""Modulo responsavel pela leitura dos dados do sensor IMU"""
import smbus
from math import degrees
from time import time, sleep
import constantes as c

bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68 

class Imu6050():
    """Classe que instancia um objeto da biblioteca RTIMU para obtencao e
    analise de dados do sensor IMU.
    """
    def __init__(self):
        """Instancia um objeto da classe RTIMU e o configura a partir da calibracao feita"""
        # Constantes
        
        self.c = 20.0  #Constante de ajuste de precisao
        self.b = 0.000225
        self.IntgrGz = 0.0
        self.angulo_yaw_referencia = self.__calcular_angulo_yaw()
        bus.write_byte_data(Device_Address, c.SMPLRT_DIV, 7) 
        bus.write_byte_data(Device_Address, c.PWR_MGMT_1, 1)
        bus.write_byte_data(Device_Address, c.CONFIG, 0)
        bus.write_byte_data(Device_Address, c.GYRO_CONFIG, 24)
        bus.write_byte_data(Device_Address, c.INT_ENABLE, 1) 
        print("Gyro Inicializado")      
        

    def __calcular_angulo_yaw(self):
        """Retorna o angulo yaw atual em graus em relacao ao zero padrao da calibracao"""
        gyro_z = self._read_raw_data(c.GYRO_ZOUT_H)
        Gz = gyro_z/self.c
        self.IntgrGz = self.IntgrGz + (Gz * 1/2610 + self.b)*3.0
        print ("AnGz=%.2f" %self.IntgrGz)
        return abs(self.IntgrGz)

    def delta_angulo_yaw(self):
        """Retorna o desvio em graus entre o angulo yaw atual e o angulo yaw de referencia"""
        return self.__calcular_angulo_yaw() - self.angulo_yaw_referencia
    def mudar_referencia(self):
        """Muda o angulo de referencia para o calculo do delta_angulo_yaw()"""
        self.angulo_yaw_referencia = self.__calcular_angulo_yaw()
    def obter_angulo_yaw(self):
        """Externaliza o metodo privado __calcular_angulo_yaw()"""
        print("Angulo calculado:")
        a = self.__calcular_angulo_yaw()
        print(a)
        return a
    
    def _read_raw_data(addr):
	    #Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value
