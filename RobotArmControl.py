from GUICalc import GUIUpdate
from MotorMovement import Motor
from ArmPostioner import AllMotorCalc
from Validation import CoordsValidation
import time
import os

global allMCAngle

Clear = (lambda: os.system('cls'))

#Main Settings
Motor.CYCLESPERSECOND = 1000

DEVMODE = False
Motor.DEVMODE = DEVMODE
#Motor settings - Precision/Acceleration/Max Speed/Min Speed
MotorOne = Motor(0.01, 3, 300, 9)
MotorTwo = Motor(0.01, 3, 300, 9)
MotorThree = Motor(0.01, 3, 300, 9)

MotorOneRun, MotorTwoRun, MotorThreeRun = True, True, True
# will be replaced by encoder and other code

motorOne = [0, 0, 0, 0]
motorTwo = [0, 0, 0, 0]
motorThree =  [0, 90, 0, 0]

allMotors =[motorOne, motorTwo, motorThree]

#Main Loop

#while ((MotorOneRun ==  MotorTwoRun == MotorThreeRun == False) == False):
def mainLoop(coords,endEffector):
    global allMCAngle
    if DEVMODE == False:
        Clear()
    print("Target  X: {} Y: {} Z: {}".format(round(coords[0],2), round(coords[1],2), round(coords[2],2)))
    coords = CoordsValidation(coords)
    allMTAngle = AllMotorCalc(coords, endEffector)
    motorOne[0] = allMTAngle[0]
    motorTwo[0] = allMTAngle[1]
    motorThree[0] = allMTAngle[2]
    if motorOne[0] <= (motorOne[1] - MotorOne.PRECISION) or motorOne[0] >= (motorOne[1] + MotorOne.PRECISION):
        MotorOne.MotorMove(motorOne)
    else:
        MotorOneRun = False
        motorOne[3] = 0
    if motorTwo[0] <= (motorTwo[1] - MotorTwo.PRECISION) or motorTwo[0] >= (motorTwo[1] + MotorTwo.PRECISION):
        MotorTwo.MotorMove(motorTwo)
    else:
        MotorTwoRun = False
        motorTwo[3] = 0
    if motorThree[0] <= (motorThree[1] - MotorThree.PRECISION) or motorThree[0] >= (motorThree[1] + MotorThree.PRECISION):
        MotorThree.MotorMove(motorThree)
    else:
        MotorThreeRun = False
        motorThree[3] = 0
    allMCAngle = [motorOne[1], motorTwo[1], motorThree[1]]
    GUIUpdate(allMCAngle)
    if (DEVMODE == False):
        print("Motor One RPS: {}\nMotor Two RPS: {}\nMotor Three RPS: {}".format(motorOne[3], motorTwo[3], motorThree[3]))
        print("Motor One Angle: {}\nMotor Two Angle: {}\nMotor Three Angle: {}".format(motorOne[1], motorTwo[1], motorThree[1]))
    else:
        print(coords)
        print("Motor One RPS: {}\nMotor Two RPS: {}\nMotor Three RPS: {}".format(motorOne[3], motorTwo[3], motorThree[3]))
        print("Motor One Angle: {}\nMotor Two Angle: {}\nMotor Three Angle: {}".format(motorOne[1], motorTwo[1], motorThree[1]))
    time.sleep(1/Motor.CYCLESPERSECOND)
    return allMCAngle