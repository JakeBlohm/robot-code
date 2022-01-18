import math
from ArmPositioner import END_EFFECTOR_OFFSET, SEGMENT_ONE, SEGMENT_THREE, SEGMENT_TWO
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

        yF = cah(mFiveCAngle,None,END_EFFECTOR_OFFSET)

        xF = soh(mFiveCAngle,None,END_EFFECTOR_OFFSET)

        hyp = pT(xF,yF) 

        if yF < 0:
            hyp = -hyp

        ang = mOneCAngle - soh(None,xF,hyp)

        griX = soh(ang,None,hyp)
        griY = cah(ang,None,hyp)
            
        griXY = pT(griX,griY)

        ang = cah(None, griXY, END_EFFECTOR_OFFSET)
        griZ = soh(ang, None, END_EFFECTOR_OFFSET)

        griDis = griY

        armLimit = 60 - griXY

        return x, y, z, curDistance, midDis, midX, midY, midZ, griX, griY, griZ + z, griDis + curDistance, armLimit
    except:
        print("GUI Math Error")
        return 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 60


def GUIUpdate(allMCAngle):
    return getXY(allMCAngle[0], allMCAngle[1], allMCAngle[2], allMCAngle[3], allMCAngle[4], allMCAngle[5])
