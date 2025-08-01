from abc import ABC, abstractmethod

class DisplayInterface(ABC):
    @abstractmethod
    def power_on(self):
        pass

    @abstractmethod
    def power_off(self):
        pass
