import math
from ArmPostioner import ALL_HORIZONTAL_OFFSET, SEGMENT_ONE, SEGMENT_TWO
import numpy as np

X = 10
Y = 10
Z = 10


mOneCAngle = ((np.degrees(np.arccos(ALL_HORIZONTAL_OFFSET/(np.sqrt((X**2)+(Y**2))))))-(np.degrees(np.arctan(Y/X))))


tarDistance = (np.sqrt((Z**2)+((np.sqrt((X**2)+(Y**2)))**2)))
mTwoCAngle = (90 - ((np.degrees(np.arctan(Z/X)))+(np.degrees(np.arccos(((SEGMENT_ONE**2)+(tarDistance**2)-(SEGMENT_TWO**2))/(2*SEGMENT_ONE*tarDistance))))))
mThreeCAngle = (180 - (np.degrees(np.arccos(((SEGMENT_TWO**2)+(SEGMENT_ONE**2)-(tarDistance**2))/(2*SEGMENT_TWO*SEGMENT_ONE)))))

print(mOneCAngle, mTwoCAngle, mThreeCAngle)

curDistanceAngled = np.sqrt(((SEGMENT_ONE**2)+(SEGMENT_TWO**2))-(2*SEGMENT_ONE*SEGMENT_TWO*np.cos(np.radians(180-mThreeCAngle))))
AAngle = (90 - (mTwoCAngle+np.degrees(np.arccos(((SEGMENT_ONE**2)+(curDistanceAngled**2)-(SEGMENT_TWO**2))/(2*SEGMENT_ONE*curDistanceAngled)))))
curDistance = curDistanceAngled*np.cos(np.radians(AAngle))
Y = (curDistance*np.cos(np.radians(mOneCAngle)),2)
X = (curDistance*np.sin(np.radians(mOneCAngle)),2)
Z = (curDistanceAngled*np.sin(np.radians(AAngle)),2)

print(X, Y, Z)