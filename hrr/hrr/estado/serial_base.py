"""Modulo base para implementacao de classes para a comunicacao serial"""

class SerialBase():
    """Classe base para implementacao de classes para a comunicacao serial"""
    def __init__(self):
        self.states = {
            "ANDAR" : "0",
            "GIRAR_ESQUERDA" : "1",
            "GIRAR_DIREITA" : "2",
            "PARAR" : "3",
            "SUBIR"  :  "6",
            "DESCER" : "7"
        }
    def escrever_estado(self, state):
        """Metodo que envia o estado atual por meio de comunicacao serial"""
