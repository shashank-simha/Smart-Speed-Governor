import RPi.GPIO as GPIO
from time import sleep
from threading import Thread
import time
import requests
import random


ledpin = 12				# PWM pin connected to LED
GPIO.setwarnings(False)			#disable warnings
GPIO.setmode(GPIO.BOARD)		#set pin numbering system
GPIO.setup(ledpin,GPIO.OUT)
pi_pwm = GPIO.PWM(ledpin,1000)		#create PWM instance with frequency
pi_pwm.start(0)				#start PWM of required Duty Cycle 


global speed
global flag # implementation of mutex

speed = 0.0
flag = 0

URL = "http://18.218.244.52/index.php"

def GetMaxSpeed():
    global flag
    global speed
    while True:
        while(flag == 1):
            pass
        flag = 1
        
        current_lat = round(random.uniform(11.2, 16.2), 4)
        current_lon = round(random.uniform(75.3, 89.1), 4)
        print("Current latitude: %s\tCurrent longitude: %s" %(current_lat, current_lon))

        PARAMS = {'lat': current_lat, 'lon': current_lon}
        r = requests.get(url = URL, params = PARAMS)
        data = r.json() 

        if data == -1:
            print("Speed Data not available for the given location")
            speed = 0
        else:
            speed = data
            print("Received new speed limit from Remote Server, %s Kmph" % (speed))
        flag = 0
        time.sleep(5)

def SetMaxSpeed():
    global flag
    global speed
    while True:
        while(flag == 1):
            pass
        flag = 1
        print("Setting the PWM value at %f%", (speed * 2)) # min: 0 kmph -> 0%  max: 50 kmph -> 100%
        pi_pwm.ChangeDutyCycle(speed * 2) # provide duty cycle in the range 0-100
        # code
        flag = 0
        time.sleep(1)

GetMaxSpeedThread = Thread(target=GetMaxSpeed)
GetMaxSpeedThread.start()

SetMaxSpeedThread = Thread(target=SetMaxSpeed)
SetMaxSpeedThread.start()

if __name__ == "__main__":
    while (1):
        pass
