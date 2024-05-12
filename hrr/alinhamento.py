from abc import ABC, abstractmethod

class Alinhamento(ABC):
    def __init__(self, robo) -> None:
        self.robo = robo
    
    @abstractmethod
    def alinhar(self):
        pass 

class AlinhamentoIMU(Alinhamento):c
    def alinhar(self):
        pass

class AlinhamentoCamera(Alinhamento):
    def alinhar(self):
        pass

class AlinhamentoCameraIMU(Alinhamento):
    def alinhar(self):
        pass
