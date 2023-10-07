"""Modulo responsavel pela a maquina de estados do robo."""
from time import sleep
import constantes as c
from serial_com import SerialMyrio

class Estado:
    """Classe responsavel pela a maquina de estados do robo."""
    def __init__(self):
        """
        Inicia variaveis de tempo de intervalo para cada estado.
        Instancia objeto da classe porta_Serial correspondente, que envia os estados do robo para a
        placa por meio de comunicacao serial.
        """
        self.tempo_do_passo = {
            "ANDAR" : c.TEMPO_ANDAR,
            "GIRAR_ESQUERDA" : c.TEMPO_GIRAR_ESQUERDA,
            "GIRAR_DIREITA" : c.TEMPO_GIRAR_DIREITA,
            "PARAR" : c.TEMPO_PARAR,
            "SUBIR" : c.TEMPO_SUBIR,
            "DESCER" : c.TEMPO_DESCER
        }
        self.atual = "PARAR"
        x = SerialMyrio()
        self.porta_serial = x.obter_porta()
        print(self.porta_serial)
        self.trocar_estado("PARAR")

    def obter_estado_atual(self):
        """Retorna o estado atual do robo."""
        return self.atual

    def __str__(self):
        """String associada ao objeto de "Estado". Sera mostrada ao printar um objeto desse tipo"""
        # Dicionario que associa o indice do estado a necessidade de correcao
        need = {
            "ANDAR" : "NAO ha necessidade de correcao",
            "GIRAR_ESQUERDA" : "Deve estar girando para esquerda",
            "GIRAR_DIREITA" : "Deve estar girando para direita",
            "PARAR" : "Deve estar parado",
            "SUBIR" : "Deve estar subindo o degrau",
            "DESCER" : "Deve estar descendo o degrau"
            }
        self.atual = self.obter_estado_atual()
        print("Estado atual: "+ self.atual + "\n")

    def trocar_estado(self, next_state):
        """Troca o estado atual do robo e o envia para a porta serial."""
        if next_state != self.atual:
            if next_state != "PARAR":
                self.atual = "PARAR"
                SerialMyrio.escrever_estado("PARAR")
            self.atual = next_state
            SerialMyrio.escrever_estado(next_state)
            print(self)
        else:
            print("Mantive o estado : " + self.atual + "\n")
