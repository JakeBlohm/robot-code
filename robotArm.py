global PRE
PRE = 0.1

def Inputs():
    tarAngle = float(input("Target Angle: "))
    curAngle = float(input("Current Angle: "))
    angles = [tarAngle, curAngle]
    return angles

def VelCalc(angles):
    if angles[0] > (angles[1] - PRE) and angles[0] < (angles[1] + PRE):
        print("Stop")
    else:
        print("Go")

while True:
    angles = Inputs()
    VelCalc(angles)