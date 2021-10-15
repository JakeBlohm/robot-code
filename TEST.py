import math



from ArmPostioner import SEGMENT_ONE, SEGMENT_TWO

def getXY(mOneCAngle, mTwoCAngle, mThreeCAngle):
    curDistanceAngled = math.sqrt((SEGMENT_ONE**2)+(SEGMENT_TWO**2)-(2*SEGMENT_ONE*SEGMENT_TWO*math.cos(math.radians(180-mThreeCAngle))))
    print(curDistanceAngled)
    AAngle = 90 - (mTwoCAngle+math.degrees(math.acos(((SEGMENT_ONE**2)+(curDistanceAngled**2)-(SEGMENT_TWO**2))/(2*SEGMENT_ONE*curDistanceAngled))))
    curDistance = curDistanceAngled*math.degrees(math.cos(AAngle))
    X = curDistance*math.cos(math.radians(mOneCAngle))
    Y = curDistance*math.sin(math.radians(mOneCAngle))
    Z = curDistanceAngled*math.sin(math.radians(AAngle))
    print(X, Y, Z)
    return X, Y, Z


getXY(3.384, 3.384, 3.384)