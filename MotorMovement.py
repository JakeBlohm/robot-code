# Jake Blohm, Isaac Roberts
# 23/9/2021
# Robot Arm code

import math
import random
import time
# import numpy
global RUN
global ACCELERATION
global PRECISION
global MAXSPEED

# Settings
PRECISION = 0.01
ACCELERATION = 3
MAXSPEED = 300
RUN = True

def Inputs():
    tarAngle = float(input("Target Angle: "))
    curAngle = float(input("Current Angle: "))
    angles = [tarAngle, curAngle]
    return angles

# Calculate the vector required to move thicc arm
def MaxVelCalc(angles, curSpeed):
    global RUN
    if angles[0] > (angles[1] - PRECISION) and angles[0] < (angles[1] + PRECISION):
        RUN = False
        return 0
    else:
        difAngle = (angles[0] - angles[1])
        if difAngle >= ((curSpeed - 10)*((curSpeed - 10)/ACCELERATION))/200:
            return 300
        if difAngle <= (-((curSpeed - 10)*((curSpeed - 10)/ACCELERATION))/200):
            return -300
        elif difAngle > 0:
            return 10
        elif difAngle < 0:
            return -10
        else:
            return random.randint(-36000,36000)

def VelCalc(tarSpeed, curSpeed):
    difSpeed = (tarSpeed - curSpeed)
    if difSpeed > 0 and curSpeed <= (MAXSPEED - ACCELERATION):
        curSpeed += ACCELERATION
    elif difSpeed < 0 and curSpeed >= (ACCELERATION - MAXSPEED):
        curSpeed -= ACCELERATION
    return curSpeed


# Encoder will replace
def EncoderOut(curSpeed, angles):
    angles[1] += (curSpeed / 100)
    return angles 

curSpeed = 0
tarSpeed = 0
angles = Inputs()

while RUN:
    tarSpeed = MaxVelCalc(angles, curSpeed)
    curSpeed = VelCalc(tarSpeed, curSpeed)
    angles = EncoderOut(curSpeed, angles)
    print(angles)
    print (curSpeed,tarSpeed)
    time.sleep(0.1)
    