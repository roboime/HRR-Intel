import RTIMU
import time
import math
import sys
import os

yaw_old = 0.0
pitch_old = 0.0
roll_old = 0.0

SETTINGS_FILE1 = os.path.join("home", "pi", "RTIMULib2", "Linux", "RTIMUlibCal", "Output", "RTIMULib.ini") 
SETTINGS_FILE2 = os.path.join("home", "pi", "RTIMULib2", "RTEllipsoidFit", "RTIMULib.ini") 

if not os.path.exists(SETTINGS_FILE1):
    print("Settings file does not exist, will be created")

s = RTIMU.Settings(SETTINGS_FILE1)
imu = RTIMU.RTIMU(s)

print("IMU Name: " + imu.IMUName())

if not imu.IMUInit():
    print("IMU Init Failed")
    sys.exit(1)
else:
    print("IMU Init Succeeded")
imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)

poll_interval = imu.IMUGetPollInterval()
dt = poll_interval*1.0/1000.0

while True:
    if imu.IMURead():
        data = imu.getIMUData()
        compass = data["compass"]
        gyro = data["gyro"]
        accel = data["accel"]
        print("compass : ", compass)
        print("gyro : ", gyro)
        print("accel : ", accel)        
        time.sleep(dt)


#########################################################################
