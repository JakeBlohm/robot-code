from ArmPositioner import END_EFFECTOR_OFFSET
from localMath import *



mOneTAngle = 90
mTwoTAngle = 0
mThreeTAngle = 0
END_EFFECTOR_OFFSET = 10
good, bad = 0, 0

for i in range(360212222):
    mOneTAngle = i - 180
    xF = 0
    yF = 10
    zF = 0

    print(xF,yF,zF)
    hyp = pT(xF,yF)
    ang = mOneTAngle - soh(None,xF,hyp)

    x = round(soh(ang,None,hyp),8)
    y = round(cah(ang,None,hyp),8)
        
    hyp = pT(xF,yF,zF)
    ang = (mThreeTAngle - mTwoTAngle) - soh(None,zF,hyp)

    z = round(soh(ang,None,hyp),8)

    mFourTAngle = toa(None,x,z)
    mFiveTAngle = cah(None,y,END_EFFECTOR_OFFSET)
    mSixTAngle = -mFourTAngle
    print(x,y,z)
    print(mFourTAngle,mFiveTAngle)


    mFiveCAngle = mFiveTAngle
    mFourCAngle = mFourTAngle
    mThreeCAngle = mThreeTAngle
    mTwoCAngle = mTwoTAngle 
    mOneCAngle = mOneTAngle

    yF = cah(mFiveCAngle,None,END_EFFECTOR_OFFSET)

    hyp = soh(mFiveCAngle,None,END_EFFECTOR_OFFSET)

    xF = soh(mFourCAngle,None,hyp)
    zF = cah(mFourCAngle,None,hyp)
            
    hyp = pT(xF,yF)

    ang = mOneCAngle - soh(None,xF,hyp)

    griX = round(soh(ang,None,hyp),6)
    griY = round(cah(ang,None,hyp),6)
        
    hyp = pT(xF,yF,zF)
    ang = (mThreeCAngle - mTwoCAngle) - soh(None,zF,hyp)

    griZ = round(soh(ang,None,hyp),6)

    griDis = griY
    print(griX,griY,griZ)
    if griX == 0 and griY == 10 and griZ == 0:
        print("GOOD they are the same like they should be at {}".format(mOneTAngle))
        good += 1
    else:
        print("BAD they are not the same at {}".format(mOneTAngle))
        bad += 1

print("GOODS: {} BADS: {}".format(good, bad))