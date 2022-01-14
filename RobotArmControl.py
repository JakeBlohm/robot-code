import sys
from GUICalc import GUIUpdate
from MotorMovement import Motor
from ArmPositioner import AllMotorCalc
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
Motor.CYCLESPERSECOND = 100

DEVMODE = False
Motor.DEVMODE = DEVMODE
#Motor settings - Precision/Acceleration/Max Speed/Min Speed
MotorOne = Motor(0.1, 6, 600, 9)
MotorTwo = Motor(0.1, 2, 200, 9)
MotorThree = Motor(0.1, 3, 300, 9)
MotorFour = Motor(0.1, 3, 300, 9)
MotorFive = Motor(0.1, 3, 300, 9)
MotorSix = Motor(0.1, 3, 300, 9)

# will be replaced by encoder and other code

motorOne = [0, 0, 0, 0]
motorTwo = [0, 0, 0, 0]
motorThree =  [0, 90, 0, 0]
motorFour = [0, 0, 0, 0]
motorFive = [0, 0, 0, 0]
motorSix = [0, 0, 0, 0]

allMotors =[motorOne, motorTwo, motorThree, motorFour, motorFive, motorSix]

#Main Loop

def calcLoop(coords,endEffector,lastCoords):
    global allMCAngle

    coords = CoordsValidation(coords)
    allMTAngle = AllMotorCalc(coords, endEffector, lastCoords)
    motorOne[0], motorTwo[0], motorThree[0], motorFour[0], motorFive[0], motorSix[0] = allMTAngle
    
    MotorOne.MotorMove(motorOne)
    MotorTwo.MotorMove(motorTwo)
    MotorThree.MotorMove(motorThree)
    MotorFour.MotorMove(motorFour)
    MotorFive.MotorMove(motorFive)
    MotorSix.MotorMove(motorSix)

    allMInfo = [motorOne, motorTwo, motorThree, motorFour, motorFive, motorSix]
    allMCAngle = [motorOne[1], motorTwo[1], motorThree[1], motorFour[1], motorFive[1], motorSix[1]]

    time.sleep(1/Motor.CYCLESPERSECOND)
    
    return allMInfo