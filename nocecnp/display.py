from abc import ABC, abstractmethod

class DisplayInterface(ABC):
    @abstractmethod
    def power_on(self):
        pass

    @abstractmethod
    def power_off(self):
        pass

    @abstractmethod
    def set_volume(self, level: int):
        pass

    @abstractmethod
    def launch_app(self, app_name: str):
        pass
