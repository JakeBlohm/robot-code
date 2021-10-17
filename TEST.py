import math

from ArmPostioner import ALL_HORIZONTAL_OFFSET

SEGMENT_TWO = 20
SEGMENT_ONE = 30
ALL_HORIZONTAL_OFFSET = 0

X = 10
Y = 10
Z = 10



mOneCAngle = (math.degrees(math.atan(X/Y)))

tarDistance = (math.sqrt((Z**2)+(math.sqrt((X**2)+(Y**2)))**2))
mTwoCAngle = (90 - ((math.degrees(math.atan(Z/X)))+(math.degrees(math.acos(((SEGMENT_ONE**2)+(tarDistance**2)-(SEGMENT_TWO**2))/(2*SEGMENT_ONE*tarDistance))))))
mThreeCAngle = (180 - (math.degrees(math.acos(((SEGMENT_TWO**2)+(SEGMENT_ONE**2)-(tarDistance**2))/(2*SEGMENT_TWO*SEGMENT_ONE)))))


curDistanceAngled = math.sqrt(((SEGMENT_ONE**2)+(SEGMENT_TWO**2))-(2*SEGMENT_ONE*SEGMENT_TWO*math.cos(math.radians(180-mThreeCAngle))))
AAngle = (90 - (mTwoCAngle + math.degrees(math.acos(((SEGMENT_ONE**2)+(curDistanceAngled**2)-(SEGMENT_TWO**2))/(2*SEGMENT_ONE*curDistanceAngled)))))
curDistance = curDistanceAngled*math.cos(math.radians(AAngle))
Y = round(curDistance*math.cos(math.radians(mOneCAngle)),2)
X = round(curDistance*math.sin(math.radians(mOneCAngle)),2)
Z = round(curDistanceAngled*math.sin(math.radians(AAngle)),2)
print(X, Y, Z)