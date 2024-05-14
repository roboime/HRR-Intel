"""Modulo responsavel pela a maquina de estados do robo."""
from time import sleep
import constantes as c
from enum import Enum, auto

# from serial_com import SerialMyrio


class Estado(Enum):
    '''
    Classe Enum que representa os estados do robô, que são:
    - Parado
    - Andando
    - Desviando
    - Alinhando
    - Finalizado 

    O estado atual do robô é armazenado em na propriedade "atual", e é enviada por comunicação serial à placa.
    '''
    ANDAR = "0"
    GIRAR_ESQUERDA = "1"
    GIRAR_DIREITA = "2"
    PARAR = "3"
    SUBIR = "6"
    DESCER = "7"

    