import math
from ArmPositioner import SEGMENT_ONE, SEGMENT_THREE, SEGMENT_TWO
from localMath import *


def getXY(mOneCAngle, mTwoCAngle, mThreeCAngle, mFourCAngle, mFiveCAngle, mSixCAngle):
    try:
        curDistanceAngled = cosrl(180 - mThreeCAngle, SEGMENT_TWO, SEGMENT_ONE, None)
        AAngle = 90 - (cosrl(None, SEGMENT_ONE, curDistanceAngled, SEGMENT_TWO) + mTwoCAngle)
        curDistance = cah(AAngle, None, curDistanceAngled)
        x = soh(mOneCAngle, None, curDistance)
        y = cah(mOneCAngle, None, curDistance)
        z = soh(AAngle, None, curDistanceAngled)

        midDis = soh(mTwoCAngle, None, SEGMENT_ONE)
        midX = soh(mOneCAngle, None, midDis)
        midY = cah(mOneCAngle, None, midDis)
        midZ = cah(mTwoCAngle, None, SEGMENT_ONE)
        
        tempDis = soh(mFiveCAngle, None, SEGMENT_THREE)

        griXF = cah(mFourCAngle, None, tempDis)
        griYF = cah(mFiveCAngle, None, SEGMENT_THREE)
        h = pT(griXF, griYF)
        angle = mOneCAngle - soh(None, griXF, h)
        griX = soh(angle, None, h)
        griY = cah(angle, None, h)

        griZF = soh(mFourCAngle, None, tempDis)
        griDisF = h
        h = pT(griZF, griDisF)
        angle = ((180-mThreeCAngle)- mTwoCAngle) - soh(None, griZF, h)
        griZ = soh(angle, None, h)
        griDis = pT(griX, griY, griZ) + curDistance

        return x, y, z, curDistance, midDis, midX, midY, midZ, griX + x, griY + y, griZ + z, griDis
    except:
        return 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0


def GUIUpdate(allMCAngle):
    return getXY(allMCAngle[0], allMCAngle[1], allMCAngle[2], allMCAngle[3], allMCAngle[4], allMCAngle[5])
