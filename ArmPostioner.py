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
SEGMENT_THREE = 10

END_EFFECTOR_OFFSET = (SEGMENT_THREE + GRIPPER_OFFSET)
MAX_ARM_LENGTH = (SEGMENT_ONE + SEGMENT_TWO + SEGMENT_THREE)
# Memory

lastCoords = [0, 0, 0]
lastAngles = [0, 0, 0]

#MotorOne position calculation, E is end effector, O is coords offset from segment 3

def MotorAngleCalc(X, Y, Z, XO, YO, ZO, EH, EV, GA):
	if (ALL_HORIZONTAL_OFFSET == 0 and X == 0 and Y > 0) or (X == 0 and Y == 0):
		mOneTAngle = 0
	else:#if ALL_HORIZONTAL_OFFSET == 0 and X == 0 and Y < 0:
		mOneTAngle = 180
		mOneTAngle = math.degrees(math.atan(Y/X))
	if X < 0:
		mOneTAngle -= 180
	tarDistance = (math.sqrt((X**2)+(Y**2)+(Z**2)))
	mTwoTAngle = (90 - ((math.degrees(math.asin(Z/tarDistance)))+(math.degrees(math.acos(((SEGMENT_ONE**2)+(tarDistance**2)-(SEGMENT_TWO**2))/(2*SEGMENT_ONE*tarDistance))))))
	mThreeTAngle = (180-(math.degrees(math.acos(((SEGMENT_TWO**2)+(SEGMENT_ONE**2)-(tarDistance**2))/(2*SEGMENT_TWO*SEGMENT_ONE)))))
	#mFourTAngle = (math.degrees(math.atan(YO/XO)))
	#mFiveTAngle = (math.degrees(math.acos(Y/END_EFFECTOR_OFFSET)))
	#mSixTAngle = GA
	return mOneTAngle, mTwoTAngle, mThreeTAngle#, mFourTAngle, mFiveTAngle, mSixTAngle
	

def AllMotorCalc(coords, endEffector):
	global lastCoords
	global lastAngles
	if coords != lastCoords:
		Temp = (END_EFFECTOR_OFFSET*math.cos(math.radians(endEffector[1])))
		X = coords[0]# - (Temp*math.sin(math.radians(endEffector[0])))
		Y = coords[1]# - (Temp*math.cos(math.radians(endEffector[0])))
		Z = coords [2]# - (END_EFFECTOR_OFFSET*math.sin(math.radians(endEffector[1])))
		XO, YO, ZO = coords[0] - X, coords[1] - Y, coords[2] - Z, 
		mOneTAngle, mTwoTAngle, mThreeTAngle = MotorAngleCalc(X, Y, Z, XO, YO, ZO, endEffector[0], endEffector[1], endEffector[2])
		allMTAngle = [mOneTAngle, mTwoTAngle, mThreeTAngle]#, mFourTAngle, mFiveTAngle, mSixTAngle]
		lastCoords = coords
		lastAngles = allMTAngle
		return allMTAngle
	else:
		return lastAngles