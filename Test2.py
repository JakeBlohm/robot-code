from ArmPositioner import END_EFFECTOR_OFFSET
from localMath import *



mOneTAngle = 90
mTwoTAngle = 0
mThreeTAngle = 0
END_EFFECTOR_OFFSET = 10
good, bad = 0, 0

for w in range(180):
    mThreeTAngle = w - 90
    for i in range(360):
        mOneTAngle = i - 180
        xF = 0
        yF = 0
        zF = 10
        
        print(xF,yF,zF)

        hyp = pT(xF,yF)
        ang = mOneTAngle - soh(None,xF,hyp)

        x = soh(ang,None,hyp)
        y = cah(ang,None,hyp)
            
        xy = round(pT(x,y),8)

        ang = cah(None, xy, END_EFFECTOR_OFFSET)
        z = soh(ang, None, END_EFFECTOR_OFFSET)

        mFourTAngle = toa(None,x,z)
        mFiveTAngle = cah(None,y,END_EFFECTOR_OFFSET)
        mSixTAngle = -mFourTAngle

        if x < 0:
            mFiveTAngle = -mFiveTAngle
        print(x,y,z)
        print(mFourTAngle,mFiveTAngle)


        mFiveCAngle = mFiveTAngle
        mFourCAngle = mFourTAngle
        mThreeCAngle = mThreeTAngle
        mTwoCAngle = mTwoTAngle 
        mOneCAngle = mOneTAngle

        yF = cah(mFiveCAngle,None,END_EFFECTOR_OFFSET)

        xF = soh(mFiveCAngle,None,END_EFFECTOR_OFFSET)


        temp = round((END_EFFECTOR_OFFSET**2-((xF**2)+(yF**2))),8)

        zF = math.sqrt(temp)

        print (xF,yF,zF)

        hyp = pT(xF,yF) 

        if yF < 0:
            hyp = -hyp

        ang = mOneCAngle - soh(None,xF,hyp)

        griX = soh(ang,None,hyp)
        griY = cah(ang,None,hyp)
            
        griXY = round(pT(griX,griY),8)

        ang = cah(None, griXY, END_EFFECTOR_OFFSET)
        griZ = soh(ang, None, END_EFFECTOR_OFFSET)

        griDis = griY
        print(round(griX,8),round(griY,8),round(griZ,8))
        if round(griX,8) == 0 and round(griY,8) == 10 and round(griZ,8) == 0:
            print("GOOD they are the same like they should be at {}, {}".format(mOneTAngle,mThreeTAngle))
            good += 1
        else:
            print("BAD they are not the same at {}, {}".format(mOneTAngle,mThreeTAngle))
            bad += 1

print("GOODS: {} BADS: {}".format(good, bad))