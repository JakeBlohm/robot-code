# Input: Coords + arm geo + joint limits
# Return: motor targetAngle
import math
from localMath import *

# GLOBAL is good - not really
global MOTOR_ONE_OFFSET
global MOTOR_TWO_OFFSET
global MOTOR_THREE_OFFSET
global MOTOR_FOUR_OFFSET
global MOTOR_FIVE_OFFSET
global SEGMENT_ONE
global SEGMENT_TWO
global BASE_HEIGHT
global ALL_HORIZONTAL_OFFSET
global lastAngles
global lastOff

# Home/Initial position of the thick arm
HOME_MOTOR_ONE = 0
HOME_MOTOR_TWO = 0
HOME_MOTOR_THREE = 0

# Motor Offsets 
# 'Horizontal' Offsets
MOTOR_TWO_OFFSET = 0
MOTOR_THREE_OFFSET = 0
MOTOR_FOUR_OFFSET = 0

ALL_HORIZONTAL_OFFSET = (MOTOR_TWO_OFFSET + MOTOR_THREE_OFFSET + MOTOR_FOUR_OFFSET)

# 'vertical' Offset
MOTOR_ONE_OFFSET = 0
MOTOR_FIVE_OFFSET = 0
GRIPPER_OFFSET = 0

# Segments
BASE_HEIGHT = 0
SEGMENT_ONE = 30
SEGMENT_TWO = 20
SEGMENT_THREE = 10

END_EFFECTOR_OFFSET = (SEGMENT_THREE + GRIPPER_OFFSET)
MAX_ARM_LENGTH = (SEGMENT_ONE + SEGMENT_TWO + SEGMENT_THREE)
# Memory

lastAngles = [0, 0, 0, 0, 0, 0]
lastOff = [0, 0, 60]


# MotorOne position calculation, E is end effector, O is coords offset from segment 3


def mRotCalc(a, b):
    if b != 0:
        if a == 0 and b < 0:
            m = 180
        elif a == 0 and b > 0:
            m = 0
        else:
            m = toa(None, a, b)
        if b < 0 and a > 0:
            m += 180
        elif b < 0 and a < 0:
            m -= 180
    elif a < 0:
        m = -90
    elif a > 0:
        m = 90
    else:
        m = 0
    return m


def endMotors(xF, yF, zF, GR, mOneTAngle, mTwoTAngle, mThreeTAngle):
    
    hyp = pT(xF,yF)
    ang = mOneTAngle - soh(None,xF,hyp)

    x = soh(ang,None,hyp)
    y = cah(ang,None,hyp)
            
    xy = round(pT(x,y),8)

    ang = cah(None, xy, END_EFFECTOR_OFFSET)
    z = soh(ang, None, END_EFFECTOR_OFFSET)

    mFourTAngle = toa(None,x,z)
    mFiveTAngle = cah(None,y,END_EFFECTOR_OFFSET)
    mSixTAngle = -mFourTAngle

    if x < 0:
        mFiveTAngle = -mFiveTAngle
        
    return mFourTAngle, mFiveTAngle, mSixTAngle


def MotorAngleCalc(x, y, z, xEnd, yEnd, zEnd, eH, eV, gR):
    global lastAngles
    mOneTAngle = mRotCalc(x, y)
    try:
        tarDistance = pT(x, y, z)
        mTwoTAngle = 90 - (soh(None, z, tarDistance) + cosrl(None, SEGMENT_ONE, tarDistance, SEGMENT_TWO))
        mThreeTAngle = 180 - cosrl(None, SEGMENT_TWO, SEGMENT_ONE, tarDistance)
        mFourTAngle, mFiveTAngle, mSixTAngle = endMotors(xEnd, yEnd, zEnd, gR, mOneTAngle, mTwoTAngle, mThreeTAngle)
        return [mOneTAngle, mTwoTAngle, mThreeTAngle, mFourTAngle, mFiveTAngle, mSixTAngle]
    except:
        print("Nah u Math Bad")
        return lastAngles


def AllMotorCalc(coords, endEffector, lastCoords):
    global lastAngles
    global lastOff
    if coords != lastCoords:
        Temp = (END_EFFECTOR_OFFSET * math.cos(math.radians(endEffector[1])))
        if endEffector[0] < 0:
            Temp = Temp
        xEnd = (soh(endEffector[0], None, Temp))
        yEnd = (cah(endEffector[0], None, Temp))
        zEnd = (soh(endEffector[1], None, END_EFFECTOR_OFFSET))
        print(endEffector)
        x, y, z = coords[0] - xEnd, coords[1] - yEnd, coords[2] - zEnd
        allMTAngle = MotorAngleCalc(x, y, z, xEnd, yEnd, zEnd, endEffector[0], endEffector[1], endEffector[2])
        Off = [xEnd, yEnd, 60-pT(xEnd, yEnd)]
        lastCoords = coords
        lastAngles = allMTAngle
        lastOff = Off
        return allMTAngle, Off
    else:
        return lastAngles, lastOff
