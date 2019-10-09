from threading import Thread
import time

global speed
global flag # implementation of mutex
speed = 0.0

flag = 0

def GetMaxSpeed():
    global flag
    global speed
    while True:
        while(flag == 1):
            pass
        flag = 1
        print("Got the speed from server")
        speed = 0
        flag = 0
        time.sleep(5)

def SetMaxSpeed():
    global flag
    global speed
    while True:
        while(flag == 1):
            pass
        flag = 1
        print("Setting the PWM value")
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