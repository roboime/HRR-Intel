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
    ANDAR = "ANDAR"
    GIRAR_ESQUERDA = "GIRAR_ESQUERDA"
    GIRAR_DIREITA = "GIRAR_DIREITA"
    PARAR = "PARAR"
    SUBIR = "SUBIR"
    DESCER = "DESCER"

    