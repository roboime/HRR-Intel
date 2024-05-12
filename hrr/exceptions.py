class BaseHRRException(Exception):
    """Base exception for HRR"""

class MyrioNotFoundException(BaseHRRException):
    """Raised when a myRIO is not found"""
    def __init__(self, message='MyRIO não encontrado.'):
        super().__init__(message)

class IMUNotFoundException(BaseHRRException):
    """Raised when an IMU is not found"""
    def __init__(self, message='IMU não encontrado.'):
        super().__init__(message)

class CameraNotFoundException(BaseHRRException):
    """Raised when a camera is not found"""
    def __init__(self, message='Câmera não encontrada.'):
        super().__init__(message)

class SensorDistanciaNotFoundException(BaseHRRException):
    """Raised when a distance sensor is not found"""
    def __init__(self, message='Sensor de distância não encontrado.'):
        super().__init__(message)

class RobotConfigException(BaseHRRException):
    """Raised when the robot configuration is invalid"""
    def __init__(self, message='Configuração do robô inválida.'):
        super().__init__(message)

class RobotCompileException(BaseHRRException):
    """Raised when the robot cannot be compiled"""
    def __init__(self, message='Erro ao compilar o robô.'):
        super().__init__(message)

class ModelNotFoundException(BaseHRRException):
    """Raised when a model is not found"""
    def __init__(self, message='Modelo não encontrado.'):
        super().__init__(message)