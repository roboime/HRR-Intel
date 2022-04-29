import RPi.GPIO as GPIO
import serial

channel = 18                    #porta utilizada
porta = "/dev/ttyAMA0"          #nao é a porta AMA0**
baudrate = 230400
GPIO.setmode(GPIO.BCM)          #configuraçoes das rasp
GPIO.setup(channel, GPIO.OUT)
ser = serial.Serial(porta,baudrate)
ser.write('1')