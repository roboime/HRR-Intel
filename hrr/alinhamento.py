from abc import ABC, abstractmethod

class Alinhamento(ABC):
    @abstractmethod
    def __init__(self, robo) -> None:
        pass
    
    @abstractmethod
    def alinhar(self):
        pass 

class AlinhamentoIMU(Alinhamento):
    def __init__(self, robo) -> None:
        self.robo = robo

    def alinhar(self):
        pass

class AlinhamentoCamera(Alinhamento):
    def __init__(self, robo) -> None:
        self.robo = robo

    def alinhar(self):
        pass

class AlinhamentoCameraIMU(Alinhamento):
    def __init__(self, robo) -> None:
        self.robo = robo

    def alinhar(self):
        pass
