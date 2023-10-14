from abc import ABC, abstractmethod


class Gyro(ABC):
    
    @abstractmethod
    def get_angulo_yaw(self):
        pass


class IMU(Gyro):
    def __init__(self) -> None:
        pass

    def get_angulo_yaw(self):
        pass