"""Modulo responsavel pela leitura dos dados do sensor IMU"""
from math import degrees
from time import time, sleep
try:
    import RTIMU
except ImportError:
    print('RTIMU not imported due to ImportError')
from . import constantes as c

class Imu():
    """Classe que instancia um objeto da biblioteca RTIMU para obtencao e
    analise de dados do sensor IMU.
    """
    def __init__(self):
        """Instancia um objeto da classe RTIMU e o configura a partir da calibracao feita"""
        # configuracoes do sensor imu
        settings = RTIMU.Settings(c.SETTINGS_FILE)
        self.imu = RTIMU.RTIMU(settings)
        self.imu.IMUInit()
        self.imu.setSlerpPower(0.02)
        self.imu.setGyroEnable(True)
        self.imu.setAccelEnable(True)
        self.imu.setCompassEnable(True)
        # Constantes
        self.intervalo_verificacoes = 0.1 #intervalo total de verificacao
        self.intervalo_poll = self.imu.IMUGetPollInterval() #intervalo entre duas medidas
        self.angulo_yaw_referencia = self.__calcular_angulo_yaw()

    def __calcular_angulo_yaw(self):
        """Retorna o angulo yaw atual em graus em relacao ao zero padrao da calibracao"""
        t_0 = time()
        t_1 = time()
        while t_1 - t_0 < self.intervalo_verificacoes:
            t_1 = time()
            if self.imu.IMURead():
                data = self.imu.getIMUData()
                fusion_pose = data["fusionPose"]
                # yaw corresponde ao fusion pose do eixo x
                # (imu esta na vertical, com eixo x para cima)
                angulo_yaw = degrees(fusion_pose[0])
                sleep(self.intervalo_poll*1.0/1000.0)
        return angulo_yaw # retorna o desvio em graus entre o angulo_yaw atual e o inicial

    def delta_angulo_yaw(self):
        """Retorna o desvio em graus entre o angulo yaw atual e o angulo yaw de referencia"""
        return self.__calcular_angulo_yaw() - self.angulo_yaw_referencia
    def mudar_referencia(self):
        """Muda o angulo de referencia para o calculo do delta_angulo_yaw()"""
        self.angulo_yaw_referencia = self.__calcular_angulo_yaw()
    def obter_angulo_yaw(self):
        """Externaliza o metodo privado __calcular_angulo_yaw()"""
        self.__calcular_angulo_yaw()
