"""Modulo que define a porta serial que faz coneccao com a MyRIO"""

from .serial_base import SerialBase

PATH = './data/serial_teste/serial_teste.txt'

class SerialTeste(SerialBase):
    """Classe herdada da classe SeriaBase e define uma porta serial ficticia
    por meio do arquivo de saida no path indicado"""
    def __init__(self):
        """Herda o __init__ da SerialBase e define o local do arquivo destino"""
        SerialBase.__init__(self)
        self.output_path = PATH
    def escrever_estado(self, state):
        """Metodo que envia o estado atual para o arquivo destino,
        simulando uma comunicacao serial"""
        with open(self.output_path, 'a') as output:
            output.write(f'{state}\n')
