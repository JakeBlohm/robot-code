# Jake Blohm, Isaac Roberts
# 23/9/2021
# Robot Arm code

from MotorMovement import Motor
import time

#Main Settings
Motor.CYCLESPERSECOND = 1000

#Motor settings - Precision/Acceleration/Max Speed/Min Speed
MotorOne = Motor(0.01, 3, 300, 9)

# will be replaced by encoder and other code
def Inputs():
    tarAngle = float(input("Target Angle: "))
    curAngle = float(input("Current Angle: "))
    motor = [tarAngle, curAngle, 0, 0]
    return motor


motorOne = Inputs()

while Motor.RUN:
    MotorOne.MotorMove(motorOne)
    time.sleep(1/Motor.CYCLESPERSECOND)

