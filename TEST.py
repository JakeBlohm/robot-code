import math
from ArmPostioner import END_EFFECTOR_OFFSET

def aTan(X,Y,mode):
	if Y != 0:
		if X == 0 and Y < 0:
			m = 180
		elif X== 0 and Y > 0:
			m = 0
		else:
			if mode == 1:
				m  = (math.degrees(math.atan(X/Y)))
			if mode == 2:
				m = (math.degrees(math.atan(X/Y)))
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

def endMotors(xT, yT, zT, GR, mOneTAngle, mTwoTAngle, mThreeTAngle):
	h = math.sqrt((xT**2)+(yT**2))
	b = aTan(xT,yT)
	xO = h*math.sin(math.radians(mOneTAngle) - b)
	print(xO)
	yO = h*math.cos(math.radians(mOneTAngle) - b)
	d = math.sqrt((yT**2)+(xT**2))
	h = math.sqrt((zT**2)+(d**2))
	b = aTan(zT,d,1)
	zO = h*math.sin(math.radians(mTwoTAngle - mThreeTAngle) - b)
	print(zO)
	print(math.sqrt((xO**2)+(zO**2))/END_EFFECTOR_OFFSET)
	if round(zO,0) != 0:
		mFourTAngle = aTan(xO,zO)
	else:
   		mFourTAngle = 0

	mFiveTAngle = math.degrees(math.asin(math.sqrt((xO**2)+(zO**2))/END_EFFECTOR_OFFSET))
	mSixTAngle = GR - mFourTAngle
	return mFourTAngle, mFiveTAngle, mSixTAngle

coords = [20, 15, 0]
endEffector = [0,0,0]

Temp = (END_EFFECTOR_OFFSET*math.cos(math.radians(endEffector[1])))
if endEffector[0] < 0:
	Temp = Temp

X = coords[0] - (Temp*math.sin(math.radians(endEffector[0])))
Y = coords[1] - (Temp*math.cos(math.radians(endEffector[0])))
Z = coords[2] - (END_EFFECTOR_OFFSET*math.sin(math.radians(endEffector[1])))
XO, YO, ZO = coords[0] - X, coords[1] - Y, coords[2] - Z 
print (XO, YO, ZO, coords[0], 80, 40, 20)
print(endMotors(XO, YO, ZO, coords[2], 80, 40, 20))