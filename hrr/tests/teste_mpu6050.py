import smbus
import math
import time

# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
 
def read_byte(reg):
    return bus.read_byte_data(address, reg)
 
def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value
 
def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
 
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)
 
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
     
bus = smbus.SMBus(1) # bus = smbus.SMBus(0) for Revision 1
address = 0x68       # via i2cdetect
 
# Activate to be able to address the module 
bus.write_byte_data(address, power_mgmt_1, 0)
 
print ("Gyroscope")
print ("--------")
 
Gyroscope_xout = read_word_2c(0x43)
Gyroscope_yout = read_word_2c(0x45)
Gyroscope_zout = read_word_2c(0x47)
 
print ("Gyroscope_xout: ", ("%5d" % Gyroscope_xout), " scaled: ", (Gyroscope_xout / 131))
print ("Gyroscope_yout: ", ("%5d" % Gyroscope_yout), " scaled: ", (Gyroscope_yout / 131))
print ("Gyroscope_zout: ", ("%5d" % Gyroscope_zout), " scaled: ", (Gyroscope_zout / 131))
 
print ("Accelerometer")
print ("---------------------")
 
accelerometer_xout = read_word_2c(0x3b)
accelerometer_yout = read_word_2c(0x3d)
accelerometer_zout = read_word_2c(0x3f)
 
accelerometer_xout_scaled = accelerometer_xout / 16384.0
accelerometer_yout_scaled = accelerometer_yout / 16384.0
accelerometer_zout_scaled = accelerometer_zout / 16384.0
 
print ("accelerometer_xout: ", ("%6d" % accelerometer_xout), " scaled: ", accelerometer_xout_scaled)
print ("accelerometer_yout: ", ("%6d" % accelerometer_yout), " scaled: ", accelerometer_yout_scaled)
print ("accelerometer_zout: ", ("%6d" % accelerometer_zout), " scaled: ", accelerometer_zout_scaled)
 
print ("X Rotation: " , get_x_rotation(accelerometer_xout_scaled, accelerometer_yout_scaled, accelerometer_zout_scaled))
print ("Y Rotation: " , get_y_rotation(accelerometer_xout_scaled, accelerometer_yout_scaled, accelerometer_zout_scaled))

time.sleep(1)