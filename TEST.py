from ArmPostioner import END_EFFECTOR_OFFSET
import math
END_EFFECTOR_OFFSET = 10
coords = [28,30,0]
endEffector = [90,0,0]

Temp = (END_EFFECTOR_OFFSET*math.cos(math.radians(endEffector[1])))
print(Temp)
if endEffector[0] < 0:
    Temp = -Temp
X = coords[0] - (Temp*math.sin(math.radians(endEffector[0])))
print(X)
Y = coords[1] - (Temp*math.cos(math.radians(endEffector[0])))
print(Y)
Z = coords[2] - (END_EFFECTOR_OFFSET*math.sin(math.radians(endEffector[1])))
print(Z)
XO, YO, ZO = coords[0] - X, coords[1] - Y, coords[2] - Z 

print(XO, YO, ZO)