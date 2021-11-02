import PySimpleGUI as sg
import numpy as np

# Main Stuff

from GUICalc import GUIUpdate
from MotorMovement import Motor
from ArmPostioner import AllMotorCalc
from Validation import CoordsValidation
import time
import os

Clear = (lambda: os.system("clear"))

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

# End of main stuff

SCALE = 9

tooltipCat = None

maxArmLength = 60
radius = maxArmLength*SCALE

layout = [
    [sg.Graph(canvas_size=(radius+1, radius+1), 
            graph_bottom_left=(-radius, -radius), 
            graph_top_right=(radius, radius), 
            background_color='white',
            enable_events = True, 
            key='graph')], 
    [sg.Text(tooltipCat, key='_coords_'),
    sg.Input(default_text="0", key='_coordInput_')]
            ]    

window = sg.Window('Arm Position Visualizer', layout, finalize=True)  
graph = window['graph']
coordText = window['_coords_']

graph.DrawCircle((0,0), radius, line_color='red') # 1
graph.DrawLine((-10000, 0), (10000,0)) # 2
graph.DrawLine((0,-10000),(0,10000)) # 3
graph.Widget.config(cursor='circle')


for x in range(-60,60,10):
    xTScale = x*SCALE
    graph.DrawLine((xTScale, -10),(xTScale, 10))
    graph.DrawText(x, (xTScale+15, -20), color='green')

for y in range(-60,60,10):
    yTScale = y*SCALE
    graph.DrawLine((-10, yTScale),(10, yTScale))
    graph.DrawText(y, (+20, yTScale+15), color='blue')

target = graph.DrawCircle((0,0), 0, line_color='blue')

def update(x, y):
    global target
    graph.delete_figure(target)
    target = graph.DrawCircle((x-1,y-1), SCALE*1.5, fill_color='blue', line_color='black')

while ((MotorOneRun ==  MotorTwoRun == MotorThreeRun == False) == False):
    event, values = window.read()  
    x = values['graph'][0]
    y = values['graph'][1]
    z = int(values['_coordInput_'])
    coordinates = "{},{}".format(int(x/SCALE),int(y/SCALE))

    if event == sg.WIN_CLOSED:
        break
    update(x,y)

    coordText.update('{}'.format(coordinates))

    # Main stuff

    coords, endEffector = [x, y, z], [0, 0, 0]

    if DEVMODE == False:
        Clear()
    allMCAngle = [motorOne[1], motorTwo[1], motorThree[1]]
    GUIUpdate(allMCAngle)
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
    if (DEVMODE == False):
        print("Motor One RPS: {}\nMotor Two RPS: {}\nMotor Three RPS: {}".format(motorOne[3], motorTwo[3], motorThree[3]))
        print("Motor One Angle: {}\nMotor Two Angle: {}\nMotor Three Angle: {}".format(motorOne[1], motorTwo[1], motorThree[1]))
    else:
        print(coords)
        print("Motor One RPS: {}\nMotor Two RPS: {}\nMotor Three RPS: {}".format(motorOne[3], motorTwo[3], motorThree[3]))
        print("Motor One Angle: {}\nMotor Two Angle: {}\nMotor Three Angle: {}".format(motorOne[1], motorTwo[1], motorThree[1]))
    time.sleep(1/Motor.CYCLESPERSECOND)


window.close()