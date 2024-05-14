from abc import ABC, abstractmethod





class Hardware(ABC):
    
    @abstractmethod
    def retrieve_data(self): pass


