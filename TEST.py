import math
from localMath import cosrl, pT

SEGMENT_ONE = 30
SEGMENT_TWO = 20
tarDistance = pT(20, 25)
mTwoCAngle = 45
mThreeCAngle = 90
curDistanceAngled = pT(10,20,10)

print(90 - ((math.degrees(math.acos(((SEGMENT_ONE**2)+(curDistanceAngled**2)-(SEGMENT_TWO**2))/(2*SEGMENT_ONE*curDistanceAngled))))+mTwoCAngle))
print(90 - (cosrl(None, SEGMENT_ONE, curDistanceAngled, SEGMENT_TWO) + mTwoCAngle))
