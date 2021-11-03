import PySimpleGUI as sg
import numpy as np
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

layout = [
    [sg.Graph(canvas_size=(radius+1, radius+1), 
            graph_bottom_left=(-radius, -radius), 
            graph_top_right=(radius, radius), 
            background_color='white',
            enable_events = True, 
            key='graph')#,
    #sg.Text("TEMP WRITING HELLO THERE\nTEST", key='_coordOutput_')
    ], 
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

current = graph.DrawCircle((0,0), 0, line_color='red')
target = graph.DrawCircle((0,0), 0, line_color='blue')

def UpdateLoop():
    global current
    while True:
        allMCAngle = mainLoop(coords, endEffector)
        currentX, currentY, currentZ = GUIUpdate(allMCAngle)
        print(currentX,currentY)
        graph.delete_figure(current)
        current = graph.DrawCircle((currentX*SCALE,currentY*SCALE), SCALE*1.5, fill_color='red', line_color='black')


        

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