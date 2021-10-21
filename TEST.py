import math
from ArmPostioner import ALL_HORIZONTAL_OFFSET, SEGMENT_ONE, SEGMENT_TWO


X = 10
Y = 10
Z = 10

mOneTAngle = math.degrees(math.atan(Y/X))
tarDistance = (math.sqrt((X**2)+(Y**2)+(Z**2)))
print("tarDistance {}".format(tarDistance))
mTwoTAngle = (90 - ((math.degrees(math.asin(Z/tarDistance)))+(math.degrees(math.acos(((SEGMENT_ONE**2)+(tarDistance**2)-(SEGMENT_TWO**2))/(2*SEGMENT_ONE*tarDistance))))))
mThreeTAngle = (180-(math.degrees(math.acos(((SEGMENT_TWO**2)+(SEGMENT_ONE**2)-(tarDistance**2))/(2*SEGMENT_TWO*SEGMENT_ONE)))))

print("One {}".format(mOneTAngle))
print("Two {}".format(mTwoTAngle))
print("Three {}".format(mThreeTAngle))

mOneCAngle = mOneTAngle
mTwoCAngle = mTwoTAngle
mThreeCAngle = mThreeTAngle

curDistanceAngled = math.sqrt((SEGMENT_TWO**2)+(SEGMENT_ONE**2)-(2*SEGMENT_TWO*SEGMENT_ONE*math.cos(math.radians(180-mThreeCAngle))))
print("curDistanceAngled {}".format(curDistanceAngled))
AAngle = 90 - ((math.degrees(math.acos(((SEGMENT_ONE**2)+(curDistanceAngled**2)-(SEGMENT_TWO**2))/(2*SEGMENT_ONE*curDistanceAngled))))+mTwoCAngle)
print("AAngle {}".format(AAngle))
curDistance = math.cos(math.radians(AAngle))*curDistanceAngled
print("curDistance {}".format(curDistance))
X = curDistance*math.sin(math.radians(mOneCAngle))
Y = curDistance*math.cos(math.radians(mOneCAngle))
Z = curDistanceAngled*math.sin(math.radians(AAngle))
print("X: {} Y: {} Z: {}".format(X, Y, Z))