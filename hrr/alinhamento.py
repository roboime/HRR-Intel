from abc import ABC, abstractmethod

class Alinhamento(ABC):
    pass

class AlinhamentoIMU(Alinhamento):
    pass

class AlinhamentoCamera(Alinhamento):
    pass

class AlinhamentoCameraIMU(Alinhamento):
    pass