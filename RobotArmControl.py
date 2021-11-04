import sys
from GUICalc import GUIUpdate
from MotorMovement import Motor
from ArmPostioner import AllMotorCalc
from Validation import CoordsValidation
import time
import os

global allMCAngle

if sys.platform.startswith('darwin'):
    Clear = (lambda: os.system('clear'))
elif sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
    Clear = (lambda: os.system('cls'))
else:
    Clear = (lambda: os.system('clear'))


#Main Settings
Motor.CYCLESPERSECOND = 1000

DEVMODE = False
Motor.DEVMODE = DEVMODE
#Motor settings - Precision/Acceleration/Max Speed/Min Speed
MotorOne = Motor(0.01, 6, 600, 9)
MotorTwo = Motor(0.01, 2, 200, 9)
MotorThree = Motor(0.01, 3, 300, 9)
MotorFour = Motor(0.01, 3, 300, 9)
MotorFive = Motor(0.01, 3, 300, 9)
MotorSix = Motor(0.01, 3, 300, 9)

# will be replaced by encoder and other code

motorOne = [0, 0, 0, 0]
motorTwo = [0, 0, 0, 0]
motorThree =  [0, 90, 0, 0]
motorFour = [0, 0, 0, 0]
motorFive = [0, 0, 0, 0]
motorSix = [0, 0, 0, 0]

allMotors =[motorOne, motorTwo, motorThree, motorFour, motorFive, motorSix]

#Main Loop

def mainLoop(coords,endEffector):
    global allMCAngle

    coords = CoordsValidation(coords)

    allMTAngle = AllMotorCalc(coords, endEffector)
    
    motorOne[0], motorTwo[0], motorThree[0], motorFour[0], motorFive[0], motorSix[0] = allMTAngle
    
    MotorOne.MotorMove(motorOne)
    MotorTwo.MotorMove(motorTwo)
    MotorThree.MotorMove(motorThree)
    MotorFour.MotorMove(motorFour)
    MotorFive.MotorMove(motorFive)
    MotorSix.MotorMove(motorSix)
   
    allMCAngle = [motorOne[1], motorTwo[1], motorThree[1], motorFour[1], motorFive[1], motorSix[1]]

    CX, CY, CZ, t, t, t, t, t = GUIUpdate(allMCAngle)

    if DEVMODE == False:
        Clear()
    print("Current X: {} Y: {} Z: {}".format(CX, CY, CZ))
    print("Target  X: {} Y: {} Z: {}".format(round(coords[0],2), round(coords[1],2), round(coords[2],2)))
    print("Motor One RPS: {}\nMotor Two RPS: {}\nMotor Three RPS: {}\nMotor Four RPS: {}\nMotor Five RPS: {}\nMotor Six RPS: {}".format(motorOne[3], motorTwo[3], motorThree[3], motorFour[3], motorFive[3], motorSix[3]))
    print("Motor One Angle: {}\nMotor Two Angle: {}\nMotor Three Angle: {}\nMotor Four Angle: {}\nMotor Five Angle: {}\nMotor Six Angle: {}".format(motorOne[1], motorTwo[1], motorThree[1], motorFour[1], motorFive[1], motorSix[1]))
    
    time.sleep(1/Motor.CYCLESPERSECOND)
    
    return allMCAngle