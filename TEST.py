import math

SEGMENT_TWO = 20
SEGMENT_ONE = 30


mOneCAngle = 45

mTwoCAngle = 45

mThreeCAngle = 90


curDistanceAngled = math.sqrt(((SEGMENT_ONE**2)+(SEGMENT_TWO**2))-(2*SEGMENT_ONE*SEGMENT_TWO*math.cos(math.radians(180-mThreeCAngle))))

AAngle = (90 - (mTwoCAngle + math.degrees(math.acos(((SEGMENT_ONE**2)+(curDistanceAngled**2)-(SEGMENT_TWO**2))/(2*SEGMENT_ONE*curDistanceAngled)))))



print (AAngle)


#curDistance = curDistanceAngled*math.cos(math.radians(AAngle))
#Y = round(curDistance*math.cos(math.radians(mOneCAngle)),2)
#X = round(curDistance*math.sin(math.radians(mOneCAngle)),2)
#Z = round(curDistanceAngled*math.sin(math.radians(AAngle)),2)

print (AAngle)