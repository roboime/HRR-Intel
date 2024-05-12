from abc import ABC, abstractmethod

class Alinhamento(ABC):
    '''
    Classe abstrata que define operações de alinhamento do robô, operando a nível hardware.
    '''
    def __init__(self, robo) -> None:
        self.robo = robo
    
    @abstractmethod
    def alinhar(self):
        pass 

class AlinhamentoIMU(Alinhamento):
    '''
    Implementação da classe Alinhamento que utiliza o giroscópio IMU para alinhar o robô.
    '''
    def alinhar(self):
        pass

class AlinhamentoCamera(Alinhamento):
    '''
    Implementação da classe Alinhamento que utiliza a câmera para alinhar o robô.
    '''
    def alinhar(self):
        pass

class AlinhamentoCameraIMU(Alinhamento):
    '''
    Implementação da classe Alinhamento que utiliza a câmera e o giroscópio IMU para alinhar o robô.
    '''
    def alinhar(self):
        pass
