import math
from ArmPostioner import SEGMENT_ONE, SEGMENT_TWO

def getXY(mOneCAngle, mTwoCAngle, mThreeCAngle):
    try:
        curDistanceAngled = math.sqrt((SEGMENT_TWO**2)+(SEGMENT_ONE**2)-(2*SEGMENT_TWO*SEGMENT_ONE*math.cos(math.radians(180-mThreeCAngle))))
        AAngle = 90 - ((math.degrees(math.acos(((SEGMENT_ONE**2)+(curDistanceAngled**2)-(SEGMENT_TWO**2))/(2*SEGMENT_ONE*curDistanceAngled))))+mTwoCAngle)
        curDistance = math.cos(math.radians(AAngle))*curDistanceAngled
        X = curDistance*math.sin(math.radians(mOneCAngle))
        Y = curDistance*math.cos(math.radians(mOneCAngle))
        Z = curDistanceAngled*math.sin(math.radians(AAngle))

        midDis= SEGMENT_ONE*math.sin(math.radians(mTwoCAngle))
        midX = midDis*math.sin(math.radians(mOneCAngle))
        midY = midDis*math.cos(math.radians(mOneCAngle))
        midZ= SEGMENT_ONE*math.cos(math.radians(mTwoCAngle))
        print (midZ)
        return X, Y, Z, curDistance, midDis, midX, midY, midZ
    except:
        return 0, 0, 0, 0, 0, 0, 0, 0

def GUIUpdate(allMCAngle):
    return getXY(allMCAngle[0], allMCAngle[1], allMCAngle[2])
