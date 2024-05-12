class BaseHRRException(Exception):
    """Base exception for HRR"""
    def __init__(self, message='Erro encontrado'):
        super().__init__(message)

class MyrioNotFoundException(BaseHRRException):
    """Raised when a myRIO is not found"""

class IMUNotFoundException(BaseHRRException):
    """Raised when an IMU is not found"""

class CameraNotFoundException(BaseHRRException):
    """Raised when a camera is not found"""

class SensorDistanciaNotFoundException(BaseHRRException):
    """Raised when a distance sensor is not found"""

class RobotConfigException(BaseHRRException):
    """Raised when the robot configuration is invalid"""