
from MotorMovement import Motor
from ArmPostioner import AllMotorCalc
import time

#Main Settings
Motor.CYCLESPERSECOND = 1000

#Motor settings - Precision/Acceleration/Max Speed/Min Speed
MotorOne = Motor(0.01, 3, 300, 9)

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

while Motor.RUN:
    motorOne[0] = AllMotorCalc(coords)[0]
    MotorOne.MotorMove(motorOne)
	MotorTwo.MotorMove(motorTwo)
	MotorThree.MotorMove(motorThree)
    time.sleep(1/Motor.CYCLESPERSECOND)
