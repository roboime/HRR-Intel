"""Modulo responsavel pela a maquina de estados do robo."""
from time import sleep
import hrr.constantes as c
# from serial_com import SerialMyrio


class Estado:
    """Classe responsavel pela a maquina de estados do robo."""
    def __init__(self):
        """
        Inicia variaveis de tempo de intervalo para cada estado.
        Instancia objeto da classe porta_Serial correspondente, que envia os estados do robo para a
        placa por meio de comunicacao serial.
        """

    @property
    def atual(self):
        """Retorna o estado atual do robo."""
        return self.__atual

    def __str__(self):
        """String associada ao objeto de "Estado". Sera mostrada ao printar um objeto desse tipo"""
        print("Estado atual: "+ self.atual + "\n")

    def trocar_estado(self, next_state):
        """Troca o estado atual do robo e o envia para a porta serial."""
