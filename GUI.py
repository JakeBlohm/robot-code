import math

from ArmPostioner import SEGMENT_ONE, SEGMENT_TWO

def getXY(mOneCAngle, mTwoCAngle, mThreeCAngle):
    print(mOneCAngle, mTwoCAngle, mThreeCAngle)
    try:
        curDistanceAngled = math.sqrt(((SEGMENT_ONE**2)+(SEGMENT_TWO**2))-(2*SEGMENT_ONE*SEGMENT_TWO*math.degrees(math.cos(180-mThreeCAngle))))
        AAngle = 90 - (mTwoCAngle+math.degrees(math.acos(((SEGMENT_ONE**2)+(curDistanceAngled**2)-(SEGMENT_TWO**2))/(2*SEGMENT_ONE*curDistanceAngled))))
        curDistance = curDistanceAngled*math.degrees(math.cos(AAngle))
        X = curDistance*math.degrees(math.cos(mOneCAngle))
        Y = curDistance*math.degrees(math.sin(mOneCAngle))
        Z = curDistanceAngled*math.degrees(math.sin(AAngle))
        print(X, Y, Z)
    except:
        print("NOPE")


def GUIUpdate(allMCAngle):
    getXY(allMCAngle[0], allMCAngle[1], allMCAngle[2])