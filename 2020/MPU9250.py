# -*- coding: utf-8 -*-
"""
Código de feedback do angulo yaw (direção que o robô aponta) dado pela MPU9250
versão 1 - sem testes
"""

from math import degrees
from time import sleep
import RTIMU

SETTINGS_FILE = "/home/pi/IMU/RTEllipsoidFit/RTIMULib.ini" #local do arquivo .ini

s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)

if (not imu.IMUInit()):
print("IMU init failed")
exit(1)
else:
print("IMU init succeeded")

#defindo parametros
imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)

poll_interval = imu.IMUGetPollInterval()
print("Recommended Poll Interval: %dmS\n" % poll_interval)

 while True:
if imu.IMURead():
data = imu.getIMUData()
fusionPose = data["fusionPose"]
global yaw
yaw = degrees(fusionPose[2])
print(str(yaw))
sleep(poll_interval*1.0/1000.0)
