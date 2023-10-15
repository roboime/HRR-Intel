from abc import ABC, abstractmethod

class Alinhamento(ABC):
    def __init__(self, robo) -> None:
        self.robo = robo
    
    @abstractmethod
    def alinhar(self):
        pass 

class AlinhamentoIMU(Alinhamento):
    def __init__(self, robo) -> None:
        super().__init__(robo)

    def alinhar(self):
        pass

class AlinhamentoCamera(Alinhamento):
    def __init__(self, robo) -> None:
        super().__init__(robo)

    def alinhar(self):
        pass

class AlinhamentoCameraIMU(Alinhamento):
    def __init__(self, robo) -> None:
        super().__init__(robo)

    def alinhar(self):
        pass
