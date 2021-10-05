#import math
#import time
#import RTIMU

#SETTINGS_FILE = "/home/pi/IMU/RTEllipsoidFit/RTIMULib.ini"
#
#s = RTIMU.Settings(SETTINGS_FILE)
#imu = RTIMU.RTIMU(s)
#
#imu.IMUInit()
#imu.setSlerpPower(0.02)
#imu.setGyroEnable(True)
#imu.setAccelEnable(True)
#imu.setCompassEnable(True)
#
#poll_interval = imu.IMUGetPollInterval()
#print("Recommended Poll Interval: %dmS\n" % poll_interval)


def get_yaw(time_limit):
    t_0 = time.time()
    t_1 = time.time()
    while (t_1 - t_0 < time_limit):
        t_1 = time.time()
        if imu.IMURead():
            data = imu.getIMUData()
            fusionPose = data["fusionPose"]
            yaw = math.degrees(fusionPose[2])
            time.sleep(poll_interval*1.0/1000.0)
    return yaw
