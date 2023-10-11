"""Modulo base do robo de corrida"""
from time import sleep
from desvio import DesvioObstaculo
from estado import Estado
from serial_com import SerialMyrio
from visao import Classe_imagem, checar_alinhamento_pista_v2
from sensor_distancia import SensorDistancia
from camera import RaspCamera
from time import sleep, time
import constantes as c
import funcoes

class Robo:
    """Classe base do robo de corrida"""
    def __init__(self, estado: Estado = Estado(),
                  sensor_distancia: SensorDistancia= SensorDistancia(),
                  camera: RaspCamera = RaspCamera(),
                  discovery: SerialMyrio = SerialMyrio()):
        """Inicializa com instancias das classes Estado, Visao, Imu e Alinhamento"""
         
        self.estado: Estado = estado
        self.desvio: DesvioObstaculo = DesvioObstaculo(self)
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
                self.estado.trocar_estado(checar_alinhamento_pista_v2(Classe_imagem(self.camera.take_photo())))  # Frente, GIRAR_ESQUERDA ou GIRAR_DIREITA
                numero_de_giradas = 1
                while self.estado.obter_estado_atual() == "GIRAR_DIREITA" or self.estado.obter_estado_atual() == "GIRAR_ESQUERDA":
                    print("desalinhado com a pista, iniciando a ",numero_de_giradas, "a girada")
                    sleep(self.tempo_do_passo[self.estado.obter_estado_atual()])
                    self.estado.trocar_estado("PARAR")
                    sleep(c.tempo_do_passo["PARAR"])
                    self.estado.trocar_estado(checar_alinhamento_pista_v2(Classe_imagem(self.camera.take_photo())))
                    numero_de_giradas+=1
                print("direcao corrigida")
                numero_de_giradas = 1
                print(self.estado.atual)
                t_0 = t_1 = time()
            else:
                t_1 = time()
    
    def desvio_obstaculo_v2(self):
        t_0 = time()
        t_1 = t_0
        while True:
            print("Estado padrao")
            self.estado.trocar_estado("ANDAR")
            sleep(c.intervalo_caminhada)  
            print(self.sensor_distanciaestado)
            ########################################### Checando proximidade de obstaculo ##########################################

            print("Medida do sensor de distancia: {}\n".format(self.sensor_distancia.get_distance()))

            if self.sensor_distancia.Get_distance() <= c.distancialimite and self.sensor_distancia.get_distance() >= c.distanciaMedia:
                print ("obstaculo detectado ", self.sensor_distancia.atual)
                self.estado.trocar_estado("PARAR")
                print(self.estado.atual)
                self.estado.trocar_estado(funcoes.decisao_desvio(self.camera)) # int
                print(self.estado.atual)
                EstadoDesvio = self.estado.atual
                
                if (self.estado.atual == "GIRAR_ESQUERDA" or self.estado.atual == "GIRAR_DIREITA"):
                    direcao_girada  = self.estado.atual            
                    self.estado.trocar_estado(funcoes.quando_parar_de_girar(self.sensor_distancia, self.velocidade_angular, self.largura_do_robo,direcao_girada))    
                    print(self.estado)
                    self.estado.trocar_estado("ANDAR")
                    print(self.estado)
                    self.estado.trocar_estado(funcoes.quando_parar_de_andar_visaocomp(c.velocidade))
                    print(self.estado)
                    print("obstaculo ultrapassado, iniciando compensasao de angulo")
                    if(direcao_girada == "GIRAR_ESQUERDA"):
                        self.estado.trocar_estado("GIRAR_DIREITA")
                        self.estado.trocar_estado(funcoes.quando_parar_de_realinhar(c.velocidade_angular, "GIRAR_DIREITA"))
                    if(direcao_girada == "GIRAR_DIREITA"):
                        self.estado.trocar_estado("GIRAR_ESQUERDA")
                        self.estado.trocar_estado(funcoes.quando_parar_de_realinhar(c.velocidade_angular, "GIRAR_ESQUERDA"))
                    print("compensado o angulo girado")
                t_1 = time()
            elif self.sensor_distancia.get_distance()<=c.distanciaMedia and self.sensor_distancia.get_distance() >c.distanciaMinima:
                print("obstaculo muito proximo")
                if EstadoDesvio == "GIRAR_DIREITA":
                    self.estado.atual = "GIRAR_ESQUERDA"
                    EstadoDesvio = "GIRAR_ESQUERDA"
                else:
                    self.estado.atual = "GIRAR_DIREITA"
                    EstadoDesvio = "GIRAR_DIREITA"
                print(self.estado)
                
                if (self.estado.atual == "GIRAR_ESQUERDA" or self.estado.atual == "GIRAR_DIREITA"):
                    direcao_girada  = self.estado.atual            
                    self.estado.trocar_estado(funcoes.quando_parar_de_girar(self.sensor_distancia, c.velocidade_angular, c.largura_do_robo,direcao_girada))    
                    print(self.estado)
                    self.estado.trocar_estado("ANDAR")
                    print(self.estado)
                    self.estado.trocar_estado(funcoes.quando_parar_de_andar_visaocomp(c.velocidade))
                    print(self.estado)
                    print("obstaculo ultrapassado, iniciando compensasao de angulo")
                    if(direcao_girada == "GIRAR_ESQUERDA"):
                        self.estado.trocar_estado("GIRAR_DIREITA")
                        self.estado.trocar_estado(funcoes.quando_parar_de_realinhar(c.velocidade_angular, "GIRAR_DIREITA"))
                    if(direcao_girada == "GIRAR_DIREITA"):
                        self.estado.trocar_estado("GIRAR_ESQUERDA")
                        self.estado.trocar_estado(funcoes.quando_parar_de_realinhar(c.velocidade_angular, "GIRAR_ESQUERDA"))
                    print("compensado o angulo girado")
                t_1 = time()
                if (self.estado.atual == "GIRAR_ESQUERDA" or self.estado.atual == "GIRAR_DIREITA"):
                    direcao_girada  = self.estado.atual            
                    self.estado.trocar_estado(funcoes.quando_parar_de_girar(self.sensor_distancia, c.velocidade_angular, c.largura_do_robo))    
                    print(self.estado)
                    self.estado.trocar_estado("ANDAR")
                    print(self.estado)
                    self.estado.trocar_estado(funcoes.quando_parar_de_andar_visaocomp(c.velocidade))
                    print(self.estado)
                    print("obstaculo ultrapassado, iniciando compensasao de angulo")
                    if(direcao_girada == "GIRAR_ESQUERDA"):
                        self.estado.trocar_estado("GIRAR_DIREITA")
                        self.estado.trocar_estado(funcoes.quando_parar_de_realinhar(c.velocidade_angular, "GIRAR_DIREITA"))
                    if(direcao_girada == "GIRAR_DIREITA"):
                        self.estado.trocar_estado("GIRAR_ESQUERDA")
                        self.estado.trocar_estado(funcoes.quando_parar_de_realinhar(c.velocidade_angular, "GIRAR_ESQUERDA"))
                    print("compensado o angulo girado")
                t_1 = time()


            elif self.sensor_distancia.Get_distance()< c.distanciaMinima:
                print("obstaculo muito proximo")
                if EstadoDesvio == "GIRAR_DIREITA":
                    self.estado.atual = "GIRAR_DIREITA"
                    EstadoDesvio = "GIRAR_DIREITA"
                else:
                    self.estado.atual = "GIRAR_ESQUERDA"
                    EstadoDesvio = "GIRAR_ESQUERDA"
                print(self.estado)
                
                if (self.estado.atual == "GIRAR_ESQUERDA" or self.estado.atual == "GIRAR_DIREITA"):
                    direcao_girada  = self.estado.atual            
                    self.estado.trocar_estado(funcoes.quando_parar_de_girar(self.sensor_distancia, c.velocidade_angular, c.largura_do_robo,direcao_girada))    
                    print(self.estado)
                    self.estado.trocar_estado("ANDAR")
                    print(self.estado)
                    self.estado.trocar_estado(funcoes.quando_parar_de_andar_visaocomp(c.velocidade))
                    print(self.estado)
                    print("obstaculo ultrapassado, iniciando compensasao de angulo")
                    if(direcao_girada == "GIRAR_ESQUERDA"):
                        self.estado.trocar_estado("GIRAR_DIREITA")
                        self.estado.trocar_estado(funcoes.quando_parar_de_realinhar(c.velocidade_angular, "GIRAR_DIREITA"))
                    if(direcao_girada == "GIRAR_DIREITA"):
                        self.estado.trocar_estado("GIRAR_ESQUERDA")
                        self.estado.trocar_estado(funcoes.quando_parar_de_realinhar(c.velocidade_angular, "GIRAR_ESQUERDA"))
                    print("compensado o angulo girado")
                t_1 = time()
                if (self.estado.atual == "GIRAR_ESQUERDA" or self.estado.atual == "GIRAR_DIREITA"):
                    direcao_girada  = self.estado.atual            
                    self.estado.trocar_estado(funcoes.quando_parar_de_girar(self.sensor_distancia, c.velocidade_angular, c.largura_do_robo))    
                    print(self.estado)
                    self.estado.trocar_estado("ANDAR")
                    print(self.estado)
                    self.estado.trocar_estado(funcoes.quando_parar_de_andar_visaocomp(c.velocidade))
                    print(self.estado)
                    print("obstaculo ultrapassado, iniciando compensasao de angulo")
                    if(direcao_girada == "GIRAR_ESQUERDA"):
                        self.estado.trocar_estado("GIRAR_DIREITA")
                        self.estado.trocar_estado(funcoes.quando_parar_de_realinhar(c.velocidade_angular, "GIRAR_DIREITA"))
                    if(direcao_girada == "GIRAR_DIREITA"):
                        self.estado.trocar_estado("GIRAR_ESQUERDA")
                        self.estado.trocar_estado(funcoes.quando_parar_de_realinhar(c.velocidade_angular, "GIRAR_ESQUERDA"))
                    print("compensado o angulo girado")
                t_1 = time()
                
        

            ########################################### Checando alinhamento com a pista ###########################################
            if t_1 - t_0 >= c.intervalo_alinhamento:
                self.estado.trocar_estado("PARAR")
                sleep(c.tempo_para_parar)
                self.estado.trocar_estado(funcoes.checar_alinhamento_pista_v1(self.camera, c.tolerancia_central, c.tolerancia_para_frente))  # Frente, GIRAR_ESQUERDA ou GIRAR_DIREITA
                while self.estado.Obter_estado_atual() != "PARAR" and self.estado.Obter_estado_atual() != "ANDAR":
                    print("desalinhado com a pista")
                    sleep(c.intervalo_enquanto_gira)
                    self.estado.trocar_estado("PARAR")
                    sleep(c.tempo_para_parar)
                    self.estado.trocar_estado(funcoes.checar_alinhamento_pista_v1(self.camera, c.tolerancia_central, c.tolerancia_para_frente))
                print("direcao corrigida")
                print(self.estado.atual)
                t_0 = t_1 = time()
            else:
                print("alinhado com a pista")
                t_1 = time()


