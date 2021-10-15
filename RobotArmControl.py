
from GUI import GUIUpdate
from MotorMovement import Motor
from ArmPostioner import AllMotorCalc
import time

#Main Settings
Motor.CYCLESPERSECOND = 1000

#Motor settings - Precision/Acceleration/Max Speed/Min Speed
MotorOne = Motor(0.01, 3, 300, 9)
MotorTwo = Motor(0.01, 3, 300, 9)
MotorThree = Motor(0.01, 3, 300, 9)

MotorOneRun, MotorTwoRun, MotorThreeRun = True, True, True
# will be replaced by encoder and other code
def Inputs():
    curAngle = float(input("Current Angle: "))
    motor = [0, curAngle, 0, 0]
    return motor

def TEMP_Input():
	Y = int(input("Y"))
	X = int(input("X"))
	Z = int(input("Z"))
	return [X, Y, Z]

coords = TEMP_Input()
motorOne = Inputs()
motorTwo = Inputs()
motorThree = Inputs()

while MotorOneRun ==  MotorTwoRun == MotorThreeRun == True:
    allMCAngle = [motorOne[1], motorTwo[1], motorThree[1]]
    GUIUpdate(allMCAngle)
    allMTAngle = AllMotorCalc(coords)
    motorOne[0] = allMTAngle[0]
    motorTwo[0] = allMTAngle[1]
    motorThree[0] = allMTAngle[2]
    if motorOne[0] <= (motorOne[1] - MotorOne.PRECISION) or motorOne[0] >= (motorOne[1] + MotorOne.PRECISION):
        MotorOne.MotorMove(motorOne)
    else:
        MotorOneRun = False
    if motorTwo[0] <= (motorTwo[1] - MotorTwo.PRECISION) or motorTwo[0] >= (motorTwo[1] + MotorTwo.PRECISION):
        MotorTwo.MotorMove(motorTwo)
    else:
        MotorTwoRun = False
    if motorThree[0] <= (motorThree[1] - MotorThree.PRECISION) or motorThree[0] >= (motorThree[1] + MotorThree.PRECISION):
        MotorThree.MotorMove(motorThree)
    else:
        MotorThreeRun = False
    time.sleep(1/Motor.CYCLESPERSECOND)
