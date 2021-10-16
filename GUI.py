import math
from ArmPostioner import SEGMENT_ONE, SEGMENT_TWO

def getXY(mOneCAngle, mTwoCAngle, mThreeCAngle):
    try:
        curDistanceAngled = math.sqrt(((SEGMENT_ONE**2)+(SEGMENT_TWO**2))-(2*SEGMENT_ONE*SEGMENT_TWO*math.cos(math.radians(180-mThreeCAngle))))
        AAngle = (90 - (mTwoCAngle+math.degrees(math.acos(((SEGMENT_ONE**2)+(curDistanceAngled**2)-(SEGMENT_TWO**2))/(2*SEGMENT_ONE*curDistanceAngled)))))
        curDistance = curDistanceAngled*math.cos(math.radians(AAngle))
        Y = round(curDistance*math.cos(math.radians(mOneCAngle)),2)
        X = round(curDistance*math.sin(math.radians(mOneCAngle)),2)
        Z = round(curDistanceAngled*math.sin(math.radians(AAngle)),2)
        print("X: {} Y: {} Z: {}".format(X, Y, Z))
        return X, Y, Z
    except:
        print("NOPE")
        return 0, 0, 0

def GUIUpdate(allMCAngle):
    getXY(allMCAngle[0], allMCAngle[1], allMCAngle[2])

