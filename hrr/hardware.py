from abc import ABC, abstractmethod


class Hardware(ABC):

    @abstractmethod
    def next_state(self): pass
