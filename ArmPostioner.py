# Input: Coords + arm geo + joint limits
# Return: motor targetAngle
import math

#GLOBAL is good - not really
global MOTOR_ONE_OFFSET
global MOTOR_TWO_OFFSET
global MOTOR_THREE_OFFSET
global MOTOR_FOUR_OFFSET
global MOTOR_FIVE_OFFSET
global SEGMENT_ONE
global SEGMENT_TWO
global ALL_HORIZONTAL_OFFSET

# Motor Offsets 
# 'Horizontal' Offsets
MOTOR_TWO_OFFSET = 0
MOTOR_THREE_OFFSET = 0
MOTOR_FOUR_OFFSET = 0

ALL_HORIZONTAL_OFFSET = (MOTOR_TWO_OFFSET + MOTOR_THREE_OFFSET + MOTOR_FOUR_OFFSET)

#'vertical' Offset
MOTOR_ONE_OFFSET = 0
MOTOR_FIVE_OFFSET = 0
GRIPPER_OFFSET = 0

#Segments
SEGMENT_ONE = 30
SEGMENT_TWO = 20

def TEMP_Input():
    Y = int(input("Y"))
    X = int(input("X"))
    return [X,Y]
    

#MotorOne position calculation

coords = TEMP_Input()

def MotorOneCalc(X, Y):
    motorOne = (math.sqrt(X^2*Y^2))

def AllMotorCalc(coords):
    MotorOneCalc(coords[0],coords[1])
    

# Math
'''
X^2 * Y^2 = hyp
bad + good = meh
meh = cos (all/Hyp)
bad = tan (Y/X)
good =cos (all/hyp) - tan(Y/X)

ALL TRIG IS IN RADIANS
'''

