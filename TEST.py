from ArmPositioner import END_EFFECTOR_OFFSET
from localMath import *
import math



mOneTAngle = 90
mTwoTAngle = 0
mThreeTAngle = 0
END_EFFECTOR_OFFSET = 10
good, bad = 0, 0

for w in range(18):
    mThreeTAngle = w*10 - 90
    for i in range(36):
        mOneTAngle = i*10 - 180
        xF = 0
        yF = 10
        zF = 0

        hyp = pT(xF,yF)
        ang = mOneTAngle - soh(None,xF,hyp)

        x = soh(ang,None,hyp)
        y = cah(ang,None,hyp)

        xy = round(pT(x,y),8)

        ang = cah(None, xy, END_EFFECTOR_OFFSET)
        z = soh(ang, None, END_EFFECTOR_OFFSET)

        print(x, y, z)
        print(round(pT(x,y,z),8))
