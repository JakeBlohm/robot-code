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

# Home/Initial position of the thicc arm
HOME_MOTOR_ONE = 0

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

#MotorOne position calculation


def MotorOneCalc(X, Y):
    if (ALL_HORIZONTAL_OFFSET == 0 and X == 0 and Y > 0) or (X == 0 and Y == 0):
        return HOME_MOTOR_ONE
    elif ALL_HORIZONTAL_OFFSET == 0 and X == 0 and Y < 0:
        return 180
    tarAngle = ((math.degrees(math.acos(ALL_HORIZONTAL_OFFSET/(math.sqrt((X**2)+(Y**2))))))-(math.degrees(math.atan(Y/X))))
    if X < 0:
        tarAngle -= 180
    return tarAngle

def AllMotorCalc(coords):
    motorOneTarAngle = MotorOneCalc(coords[0],coords[1])
    return motorOneTarAngle
