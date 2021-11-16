import math
from ArmPostioner import END_EFFECTOR_OFFSET



coords = [20,10,5]
endEffector = [45,15,0]


Temp = (END_EFFECTOR_OFFSET*math.cos(math.radians(endEffector[1])))
X = coords[0] - (Temp*math.sin(math.radians(endEffector[0])))
Y = coords[1] - (Temp*math.cos(math.radians(endEffector[0])))
Z = coords[2] - (END_EFFECTOR_OFFSET*math.sin(math.radians(endEffector[1])))
XO, YO, ZO = coords[0] - X, coords[1] - Y, coords[2] - Z 
print(XO,YO,ZO)