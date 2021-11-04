
import math
X = -10
Y = -10

if Y != 0:
    if X == 0 and Y < 0:
        MO = 180
    elif X== 0 and Y > 0:
        MO = 0
    else:
        if X < 0:
            TX = -X
        else:
            TX = X
        if Y < 0:
            TY = -Y
        else:
            TY = Y
        MO = (math.degrees(math.atan(TX/TY)))
elif X < 0:
    MO = -90
elif X > 0:
    MO = 90
else:
    MO = 0

if Y < 0:
    MO += 90

if X < 0:
    MO = -MO


print(MO)