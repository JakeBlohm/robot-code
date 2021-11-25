import math
from ArmPostioner import SEGMENT_ONE, SEGMENT_THREE, SEGMENT_TWO

def getXY(mOneCAngle, mTwoCAngle, mThreeCAngle, mFourCAngle, mFiveCAngle, mSixCAngle):
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
        midZ = SEGMENT_ONE*math.cos(math.radians(mTwoCAngle))
        
        tempDis = SEGMENT_THREE*math.sin(math.radians(mFiveCAngle))

        griXF = tempDis*math.cos(math.radians(mFourCAngle))
        griYF = SEGMENT_THREE*math.cos(math.radians(mFiveCAngle))
        h = math.sqrt((griXF**2)+(griYF**2))
        b = math.atan(griXF/griYF)
        griX = h*math.sin(math.radians(mOneCAngle) - b)
        griY = h*math.cos(math.radians(mOneCAngle) - b)

        griZF = tempDis*math.sin(math.radians(mFourCAngle))
        griDisF = math.sqrt(griXF**2+griYF**2)
        h = math.sqrt((griZF**2)+(griDisF**2))
        b = math.atan(griZF/griDisF)
        griZ = h * math.sin(math.radians(180-(mTwoCAngle+(180-mThreeCAngle))) - b)
        griDis = math.sqrt(griX**2+griY**2+griZ**2) + curDistance

        return X, Y, Z, curDistance, midDis, midX, midY, midZ, griX + X, griY + Y, griZ + Z, griDis
    except:
        return 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

def GUIUpdate(allMCAngle):
    return getXY(allMCAngle[0], allMCAngle[1], allMCAngle[2], allMCAngle[3], allMCAngle[4], allMCAngle[5])
