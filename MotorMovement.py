# Jake Blohm, Isaac Roberts
# 23/9/2021
# Robot Arm code
import os
import math
import random
import time
# import numpy
global RUN
global ACCELERATION
global PRECISION
global MAXSPEED
global CYCLESPERSECOND
global MINSPEED

# Settings
PRECISION = 0.01
ACCELERATION = 3
MAXSPEED = 300
MINSPEED = 9
CYCLESPERSECOND = 1000
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
        if curSpeed == MAXSPEED:
            curSpeed -= ACCELERATION
        elif curSpeed == - MAXSPEED:
            curSpeed += ACCELERATION
        difAngle = (angles[0] - angles[1])
        if difAngle >= ((((curSpeed+ACCELERATION)/ACCELERATION)+1)*(((curSpeed+ACCELERATION))/2))/CYCLESPERSECOND:
            return MAXSPEED
        if difAngle <= 0:
            return -MAXSPEED
        elif difAngle > 0:
            return MINSPEED
        elif difAngle < 0:
            return -MINSPEED
        else:
            print("MAJOR ERROR")
            RUN = False

def VelCalc(tarSpeed, curSpeed):
    difSpeed = (tarSpeed - curSpeed)
    if difSpeed > 0 and curSpeed <= (MAXSPEED - ACCELERATION):
        curSpeed += ACCELERATION
    elif difSpeed < 0 and curSpeed >= (ACCELERATION - MAXSPEED):
        curSpeed -= ACCELERATION
    return curSpeed


# Encoder will replace
def EncoderOut(curSpeed, angles):
    angles[1] += (curSpeed / CYCLESPERSECOND)
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
    time.sleep(1/CYCLESPERSECOND)
    
#current error 34 and 36 need nth term instead of (curSpeed - 10)/ACCELERATION     nth term - ACCELERATION to work out amount of terns neaded   or triginometry with the curSpeed and 
