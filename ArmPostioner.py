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
global BASE_HIGHT
global ALL_HORIZONTAL_OFFSET
global lastCoords
global lastAngles

# Home/Initial position of the thicc arm
HOME_MOTOR_ONE = 0
HOME_MOTOR_TWO = 0
HOME_MOTOR_THREE = 0

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
BASE_HIGHT = 0
SEGMENT_ONE = 30
SEGMENT_TWO = 20

# Memory

lastCoords = [HOME_MOTOR_ONE, HOME_MOTOR_TWO, HOME_MOTOR_THREE]
lastAngles = []

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

def MotorTwoPlusThreeCalc(X, Y, Z):
	tarDistance = (math.sqrt((Z**2)+((math.sqrt((X**2)+(Y**2)))**2)))
	mTwoTAngle = 90-(math.sin(math.radians(Z/tarDistance)))+(math.degrees(math.acos(((SEGMENT_ONE**2)+(tarDistance**2)-(SEGMENT_TWO**2))/(2*SEGMENT_ONE*tarDistance))))
	mThreeTAngle = 180-(math.degrees(math.acos(((SEGMENT_ONE**2)+(SEGMENT_TWO**2)-(tarDistance**2))/(2*SEGMENT_ONE*SEGMENT_TWO))))
	return [mTwoTAngle, mThreeTAngle]
	

def AllMotorCalc(coords):
	global lastCoords
	global lastAngles
	if coords != lastCoords:
		mOneTAngle = MotorOneCalc(coords[0], coords[1])
		mTwoTAngle = MotorTwoPlusThreeCalc(coords[0], coords[1], coords[2])[0]
		mThreeTAngle = MotorTwoPlusThreeCalc(coords[0], coords[1], coords[2])[1]
		allMTAngle = [mOneTAngle, mTwoTAngle, mThreeTAngle]
		lastCoords = coords
		lastAngles = allMTAngle
		return allMTAngle
	else:
		return lastAngles