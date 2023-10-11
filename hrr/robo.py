"""Modulo base do robo de corrida"""
from time import sleep
from desvio import DesvioObstaculo
from estado import Estado
from serial_com import SerialMyrio
from imu6050 import Imu6050 
from visao import Classe_imagem, checar_alinhamento_pista_v2
from sensor_distancia import SensorDistancia
from camera import RaspCamera
from time import sleep, time
import constantes as c

class Robo:
    """Classe base do robo de corrida"""
    def __init__(self, estado: Estado = Estado(),
                  imu: Imu6050 = Imu6050(), 
                  visao: Classe_imagem = Classe_imagem(), 
                  desvio: DesvioObstaculo = DesvioObstaculo(), 
                  sensor_distancia: SensorDistancia= SensorDistancia(),
                  camera: RaspCamera = RaspCamera(),
                  discovery: SerialMyrio = SerialMyrio()):
        """Inicializa com instancias das classes Estado, Visao, Imu e Alinhamento"""
        self.estado: Estado = estado
        self.imu: Imu6050 = imu
        self.visao: Classe_imagem = visao
        self.desvio: DesvioObstaculo = desvio
        self.sensor_distancia: SensorDistancia = sensor_distancia
        self.camera: RaspCamera = camera
        self.discovery: SerialMyrio = discovery
    def corrida(self):
        """Metodo base da corrida do robo"""
        self.discovery.escrever_estado("ANDAR")
        print("Mandou Andar \n")
        while True:
            t_0 = time()
            t_1 =  t_0
            print("Andando em frente")
            self.estado.trocar_estado("ANDAR")
            sleep(c.intervalo_caminhada)  # Tentar maximizar intervalo_caminhada quando for botar o robo para andar
            ########################################### Checando alinhamento com a pista ###########################################
            if t_1 - t_0 >= self.intervalo_alinhamento:
                print("hora de alinhar")
                self.estado.trocar_estado("PARAR") ##tirar esse tempo ja que as pausas devem estar embutidas no tirar foto e na troca de estados
                sleep(c.tempo_para_parar)
                self.estado.trocar_estado(checar_alinhamento_pista_v2(self.visao))  # Frente, GIRAR_ESQUERDA ou GIRAR_DIREITA
                numero_de_giradas = 1
                while self.estado.obter_estado_atual() == "GIRAR_DIREITA" or self.estado.obter_estado_atual() == "GIRAR_ESQUERDA":
                    print("desalinhado com a pista, iniciando a ",numero_de_giradas, "a girada")
                    sleep(self.tempo_do_passo[self.estado.obter_estado_atual()])
                    self.estado.trocar_estado("PARAR")
                    sleep(c.tempo_do_passo["PARAR"])
                    self.estado.trocar_estado(checar_alinhamento_pista_v2(self.visao))
                    numero_de_giradas+=1
                print("direcao corrigida")
                numero_de_giradas = 1
                print(self.estado.atual)
                t_0 = t_1 = time()
            else:
                t_1 = time()
          


