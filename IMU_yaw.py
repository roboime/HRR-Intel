import RTIMU
import math
import time
import os.path
import sys
import getopt

sys.path.append('.')

SETTINGS_FILE = "/home/pi/RTIMULib2/Linux/RTIMULib"

# if not os.path.exists(SETTINGS_FILE + ".ini"):
#print("Settings file does not exist, will be created")

s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)

# if (not imu.IMUInit()):
#print("IMU Init Failed")
# sys.exit(1)

# this is a good time to set any fusion parameters

imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)

poll_interval = imu.IMUGetPollInterval()


# while True:


def get_yaw(time_limit):
    t_0 = time.time()
    t_1 = time.time()
    while (t_1 - t_0 < time_limit):
        t_1 = time.time()
        if imu.IMURead():
            data = imu.getIMUData()
            fusionPose = data["fusionPose"]
            y = math.degrees(fusionPose[2])
            time.sleep(poll_interval*10.0/1000.0)
    return y
