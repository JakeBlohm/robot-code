import math
from ArmPostioner import SEGMENT_ONE, SEGMENT_TWO

def getXY(mOneCAngle, mTwoCAngle, mThreeCAngle):
    try:
        curDistanceAngled = math.sqrt((SEGMENT_TWO**2)+(SEGMENT_ONE**2)-(2*SEGMENT_TWO*SEGMENT_ONE*math.cos(math.radians(180-mThreeCAngle))))
        AAngle = 90 - ((math.degrees(math.acos(((SEGMENT_ONE**2)+(curDistanceAngled**2)-(SEGMENT_TWO**2))/(2*SEGMENT_ONE*curDistanceAngled))))+mTwoCAngle)
        curDistance = math.cos(math.radians(AAngle))*curDistanceAngled
        X = round(curDistance*math.cos(math.radians(mOneCAngle)),2)
        Y = round(curDistance*math.sin(math.radians(mOneCAngle)),2)
        Z = round(curDistanceAngled*math.sin(math.radians(AAngle)),2)
        print("Current X: {} Y: {} Z: {}".format(X, Y, Z))
        return X, Y, Z
    except:
        print("NOPE")
        return 0, 0, 0

def GUIUpdate(allMCAngle):
    return getXY(allMCAngle[0], allMCAngle[1], allMCAngle[2])
