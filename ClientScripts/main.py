import RPi.GPIO as GPIO
from time import sleep
from threading import Thread
import time
import requests
import random


ledpin = 12				# PWM pin connected to LED
button = 16             # Push button 


global max_speed
global current_speed
global flag # implementation of mutex
global pi_pwm

def setup():
    global pi_pwm
    GPIO.setwarnings(False)			# disable warnings
    GPIO.setmode(GPIO.BOARD)		# set pin numbering systemGPIO.setup(ledpin,GPIO.OUT)
    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP) # setup input pin with pull up config
    GPIO.setup(ledpin,GPIO.OUT)
    pi_pwm = GPIO.PWM(ledpin,1000)		# create PWM instance with frequency
    pi_pwm.start(0)				# start PWM of required Duty Cycle 


max_speed = 50.0
current_speed = 0.0
flag = 0

URL = "http://18.218.244.52/index.php"

def GetMaxSpeed():
    global flag
    global max_speed
    global current_speed

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
            max_speed = 50 # some high value (in this case 50 since we are using 100% dutycycle for 50Kmph)
        else:
            max_speed = data
            print("Received new speed limit from Remote Server, %s Kmph" % (max_speed))
            if current_speed > max_speed:
                current_speed = max_speed
                
        flag = 0
        time.sleep(5)

def ControlSpeed():
    global flag
    global max_speed
    global current_speed
    global pi_pwm

    while True:
        while(flag == 1):
            pass
        
        button_state = GPIO.input(button)
        
        if  button_state == False:
            if current_speed < max_speed:
                current_speed += 1
            else:
                print("Cannot accelerate beyond max_speed")
        else:
            if current_speed > 0:
                current_speed -= 1
        
        dutycycle = current_speed * 2 # map # Speed to PWM dutycycle (min: 0 kmph -> 0%  max: 50 kmph -> 100%)
        if dutycycle < 0:
            dutycycle = 0
        elif dutycycle > 100:
            dutycycle = 100            
        pi_pwm.ChangeDutyCycle(dutycycle) # provide duty cycle in the range 0-100
        pi_pwm.ChangeDutyCycle(current_speed * 2) # provide duty cycle in the range 0-100
            
        time.sleep(0.01) # 10ms delay
        

GetMaxSpeedThread = Thread(target=GetMaxSpeed)
GetMaxSpeedThread.start()

ControlSpeedThread = Thread(target=ControlSpeed)
ControlSpeedThread.start()

if __name__ == "__main__":
    setup() # call setup function
    while (1):
        pass
