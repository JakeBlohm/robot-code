import PySimpleGUI as sg
import math
import threading
from RobotArmControl import *
global coords
global endEffector


SCALE = 9

#temp

endEffector = [0, 0, 0]
coords = [0, 0, 0]


tooltipCat = None

maxArmLength = 60
radius = maxArmLength*SCALE
halfRadius = radius/2

layout = [
    [sg.Graph(canvas_size=(radius+1, radius+1), 
            graph_bottom_left=(-radius, -radius), 
            graph_top_right=(radius, radius), 
            background_color='white',
            enable_events = True, 
            key='graph'),
    sg.Graph(canvas_size=(halfRadius+1, halfRadius+1),
            graph_bottom_left=(-SCALE-1, -SCALE-1),
            graph_top_right=(halfRadius, halfRadius),
            background_color='white',
            #enable_events = True, 
            key='_side_')
    #sg.Text("TEMP WRITING HELLO THERE\nTEST", key='_coordOutput_')
    ], 
    [sg.Text(tooltipCat, key='_coords_'),
    sg.Input(default_text="0", key='_coordInput_')]
            ]    

window = sg.Window('Arm Position Visualizer', layout, finalize=True)  
graph = window['graph']
side = window['_side_']
coordText = window['_coords_']

graph.DrawCircle((0,0), radius, line_color='red') # 1
graph.DrawLine((-10000, 0), (10000,0)) # 2
graph.DrawLine((0,-10000),(0,10000)) # 3
graph.Widget.config(cursor='circle')

side.DrawLine((-1000, 0), (1000, 0))
side.DrawLine((0, -1000), (0, 1000))

gripper = side.DrawCircle((1,50*SCALE), SCALE*0.75, fill_color='red', line_color='black')
shoulder = side.DrawCircle((1,1), SCALE*0.75, fill_color='green', line_color='black')
elbow = side.DrawCircle((1,30*SCALE/2), SCALE*0.75, fill_color='blue', line_color='black')

for x in range(-60,60,10):
    xTScale = x*SCALE
    graph.DrawLine((xTScale, -10),(xTScale, 10))
    graph.DrawText(x, (xTScale+15, -20), color='green')

for y in range(-60,60,10):
    yTScale = y*SCALE
    graph.DrawLine((-10, yTScale),(10, yTScale))
    graph.DrawText(y, (+20, yTScale+15), color='blue')

current = graph.DrawCircle((0,0), 0, line_color='red')
target = graph.DrawCircle((0,0), 0, line_color='blue')

def UpdateLoop():
    global current
    global gripper
    global elbow

    while True:
        allMCAngle = mainLoop(coords, endEffector)

        endX, endY, endZ, endDis, midDis, midZ  = GUIUpdate(allMCAngle)

        corEndX, corEndY, corEndZ, corEndDis, corMidDis, corMidZ = endX*SCALE, endY*SCALE, endZ*SCALE, endDis*SCALE, midDis*SCALE, midZ*SCALE

        graph.delete_figure(current)
        side.delete_figure(gripper)
        side.delete_figure(elbow)

        current = graph.DrawCircle((corEndX,corEndY), SCALE*1.5, fill_color='red', line_color='black')
        gripper = side.DrawCircle((corEndDis/2, corEndZ/2), SCALE*0.75, fill_color='red', line_color='black')
        elbow = side.DrawCircle((corMidZ/2,corMidDis/2), SCALE*0.75, fill_color='blue', line_color='black')

def update(x, y):
    global target
    graph.delete_figure(target)
    target = graph.DrawCircle((x-1,y-1), SCALE*1.5, fill_color='blue', line_color='black')

Math = threading.Thread(target=UpdateLoop, args=(), daemon=True)
Math.start()

while True:
    event, values = window.read() 

    if event == sg.WIN_CLOSED:
        break

    x = values['graph'][0]
    y = values['graph'][1]
    z = int(values['_coordInput_'])

    coordinates = "{},{}".format(int(x/SCALE),int(y/SCALE))
    coords = [x/SCALE, y/SCALE, z]
    coordText.update('{}'.format(coordinates))
    
    update(x,y)



window.close()