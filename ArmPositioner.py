# Input: Coords + arm geo + joint limits
# Return: motor targetAngle
import math

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
global lastCoords
global lastAngles

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

lastCoords = [0, 0, 0]
lastAngles = [0, 0, 0, 0, 0, 0]


# MotorOne position calculation, E is end effector, O is coords offset from segment 3


def pT(a, b, c=0):
    return math.sqrt(a ** 2 + b ** 2 + c ** 2)


def soh(ang, opp, hyp):
    if opp is None:
        ans = hyp * math.sin(math.radians(ang))
    elif hyp is None:
        ans = opp / math.sin(math.radians(ang))
    elif ang is None:
        ans = math.degrees(math.asin(opp / hyp))
    else:
        print("Could not find missing data")
    return ans


def cah(ang, adj, hyp):
    if adj is None:
        ans = hyp * math.cos(math.radians(ang))
    elif hyp is None:
        ans = adj / math.cos(math.radians(ang))
    elif ang is None:
        ans = math.degrees(math.acos(adj / hyp))
    else:
        print("Could not find missing data")
    return ans


def toa(ang, opp, adj):
    if opp is None:
        ans = adj * math.tan(math.radians(ang))
    elif adj is None:
        ans = opp / math.tan(math.radians(ang))
    elif ang is None:
        ans = math.degrees(math.atan(opp / adj))
    else:
        print("Could not find missing data")
    return ans


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
	h = pT(xF,yF)
	angle = mOneTAngle - soh(None,xF,h)
	x = soh(angle,None,h)
	y = cah(angle,None,h)

	d = h
	h = pT(zF,d)
	angle = 180-(mTwoTAngle+(180-mThreeTAngle)) - soh(None, zF, h)
	z = soh(angle, None, h)
	if round(z,0) != 0:
		mFourTAngle = mRotCalc(x,z)
	else:
   		mFourTAngle = 0
	mFiveTAngle = cah(None, z, END_EFFECTOR_OFFSET)
	mSixTAngle = GR - mFourTAngle
	return mFourTAngle, mFiveTAngle, mSixTAngle

def MotorAngleCalc(x, y, z, xO, yO, zO, eH, eV, gR):
    global lastAngles
    mOneTAngle = mRotCalc(x, y)
    try:
        tarDistance = pT(x, y, z)
        mTwoTAngle = (90 - ((math.degrees(math.asin(z / tarDistance))) + (math.degrees(math.acos(
            ((SEGMENT_ONE ** 2) + (tarDistance ** 2) - (SEGMENT_TWO ** 2)) / (2 * SEGMENT_ONE * tarDistance))))))
        mThreeTAngle = (180 - (math.degrees(math.acos(
            ((SEGMENT_TWO ** 2) + (SEGMENT_ONE ** 2) - (tarDistance ** 2)) / (2 * SEGMENT_TWO * SEGMENT_ONE)))))
        mFourTAngle, mFiveTAngle, mSixTAngle = endMotors(xO, yO, zO, gR, mOneTAngle, mTwoTAngle, mThreeTAngle)
        lastAngles = [mOneTAngle, mTwoTAngle, mThreeTAngle, mFourTAngle, mFiveTAngle, mSixTAngle]
        return [mOneTAngle, mTwoTAngle, mThreeTAngle, mFourTAngle, mFiveTAngle, mSixTAngle]
    except:
        print("Nah u Math Bad")
        return lastAngles


def AllMotorCalc(coords, endEffector):
	global lastCoords
	global lastAngles
	if coords != lastCoords:
		Temp = (END_EFFECTOR_OFFSET*math.cos(math.radians(endEffector[1])))
		if endEffector[0] < 0:
			Temp = Temp
		x = coords[0] - (soh(endEffector[0],None,Temp))
		y = coords[1] - (cah(endEffector[0],None,Temp))
		z = coords[2] - (END_EFFECTOR_OFFSET*math.sin(math.radians(endEffector[1])))
		xO, yO, zO = coords[0] - x, coords[1] - y, coords[2] - z 
		allMTAngle = MotorAngleCalc(x, y, z, xO, yO, zO, endEffector[0], endEffector[1], endEffector[2])
		lastCoords = coords
		return allMTAngle
	else:
		return lastAngles
