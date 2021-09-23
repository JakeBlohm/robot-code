# Jake Blohm, Isaac Roberts
# 23/9/2021
# Robot Arm code

import math
import random
# import numpy
global RUN
global ACCELERATION
global PRECISION

# Settings
PRECISION = 0.01
ACCELERATION = 71.25
RUN = True

def Inputs():
    tarAngle = float(input("Target Angle: "))
    curAngle = float(input("Current Angle: "))
    angles = [tarAngle, curAngle]
    return angles

# Calculate the vector required to move thicc arm
def VelCalc(angles):
    global RUN
    if angles[0] > (angles[1] - PRECISION) and angles[0] < (angles[1] + PRECISION):
        RUN = False
        return 0
    else:
        difAngle = (angles[0] - angles[1])
        if difAngle >= 10:
            return 600
        if difAngle <= -10:
            return -600
        elif difAngle >= 2:
            return difAngle * ACCELERATION
        elif difAngle <= -2:
            return difAngle * ACCELERATION
        elif difAngle > 0.5:
            return 30
        elif difAngle < -0.5:
            return -30
        elif difAngle > 0:
            return 10
        elif difAngle < 0:
            return -10
        else:
            return random.randint(-36000,36000)

# Encoder will replace
def EncoderOut(motor, angles):
    angles[1] += (motor / 1000)
    return angles 

while RUN:
    motor = VelCalc(angles)
    angles = EncoderOut(motor, angles)
    print(angles)
    