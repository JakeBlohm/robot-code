import math
from decimal import Decimal
from ArmPostioner import ALL_HORIZONTAL_OFFSET

SEGMENT_TWO = str(20)
SEGMENT_ONE = str(30)
ALL_HORIZONTAL_OFFSET = str(0)

X = str(10)
Y = str(10)
Z = str(10)



mOneCAngle = round((math.degrees(math.atan(Decimal(X)/Decimal(Y)))))
print (mOneCAngle)
tarDistance = (math.sqrt(Decimal(Z)**2)+(math.sqrt((Decimal(X)**2)+(Decimal(Y)**2))**2))
mTwoCAngle = (90 - ((math.degrees(math.atan(Decimal(Z)/Decimal(X))))+(math.degrees(math.acos(((Decimal(SEGMENT_ONE)**2)+(Decimal(tarDistance)**2)-(Decimal(SEGMENT_TWO)**2))/(2*Decimal(SEGMENT_ONE)*Decimal(tarDistance)))))))
mThreeCAngle = (180 - (math.degrees(math.acos(((Decimal(SEGMENT_TWO)**2)+(Decimal(SEGMENT_ONE)**2)-(Decimal(tarDistance)**2))/(2*Decimal(SEGMENT_TWO)*Decimal(SEGMENT_ONE))))))


curDistanceAngled = round((math.sqrt(((Decimal(SEGMENT_ONE)**2)+(Decimal(SEGMENT_TWO)**2))-(2*Decimal(SEGMENT_ONE)*Decimal(SEGMENT_TWO)*math.cos(math.radians(180-Decimal(mThreeCAngle)))))),0)
AAngle = round((90 - (Decimal(mTwoCAngle) + math.degrees(math.acos(((Decimal(SEGMENT_ONE)**2)+(Decimal(curDistanceAngled)**2)-(Decimal(SEGMENT_TWO)**2))/(2*Decimal(SEGMENT_ONE)*Decimal(curDistanceAngled)))))),0)
curDistance = curDistanceAngled*math.cos(math.radians(AAngle))
Y = round(curDistance*math.cos(math.radians(mOneCAngle)),2)
X = round(curDistance*math.sin(math.radians(mOneCAngle)),2)
Z = round(curDistanceAngled*math.sin(math.radians(AAngle)),2)
print(X, Y, Z)