import math

from ArmPostioner import END_EFFECTOR_OFFSET

def mRotCalc(X,Y):
	if Y != 0:
		if X == 0 and Y < 0:
			m = 180
		elif X== 0 and Y > 0:
			m = 0
		else:
			m  = (math.degrees(math.atan(X/Y)))

		if Y < 0 and X > 0:
			m += 180
		elif Y < 0 and X < 0:
    			m -= 180
	elif X < 0:
		m = -90
	elif X > 0:
		m = 90
	else:
		m = 0
	return m

GR = 0
XO = 10
YO = 0
ZO = 0
END_EFFECTOR_OFFSET = 10


Temp = math.sqrt((XO**2)+(YO**2))
if ZO != 0:
    mFourTAngle = mRotCalc(Temp/ZO)
else:
    mFourTAngle = 0
mFiveTAngle = math.degrees(math.asin((math.sqrt((Temp**2)+(ZO**2)))/END_EFFECTOR_OFFSET))
mSixTAngle = GR - mFourTAngle

