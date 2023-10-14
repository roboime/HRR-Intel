class MyrioNotFoundException(Exception):
    """Raised when a myRIO is not found"""
    pass

class IMUNotFoundException(Exception):
    """Raised when an IMU is not found"""
    pass

class CameraNotFoundException(Exception):
    """Raised when a camera is not found"""
    pass

class SensorDistanciaNotFoundException(Exception):
    """Raised when a distance sensor is not found"""
    pass