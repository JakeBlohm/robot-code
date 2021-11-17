import PySimpleGUI as sg
import configparser
import threading
from RobotArmControl import *
global coords
global endEffector

SCALE = 10

allMCAngle = [0, 0, 0, 0, 0, 0]
endEffector = [0, 0, 0]
coords = [0, 0, 0]

tooltipCat = None
maxArmLength = 60
radius = maxArmLength*SCALE
halfRadius = radius/2

menu = [["File", ["Settings",["Scale", ["4::4",'5::5','6::6','7::7','8::8','9::9','10::10']],"Exit"]]]

sGBLx = -10*SCALE-1
sGBLy = -2*SCALE-1
sGCanSizeX = halfRadius+1+-sGBLx
sGCanSizeY = halfRadius+1+-sGBLy

data_column = sg.Column([
    [sg.Text("Target Coordinates:  {}".format(tooltipCat), key='_targetCoords_')],
    [sg.Text("Current Coordinates: ", key='_currentCoords_')],
    [sg.Text("Motor 1 RPS: ", key='_mOneRPS_'),sg.Text("Motor 1 Angle: ", key='_mOneAngle_')],
    [sg.Text("Motor 2 RPS: ", key='_mTwoRPS_'),sg.Text("Motor 2 Angle: ", key='_mTwoAngle_')],
    [sg.Text("Motor 3 RPS: ", key='_mThreeRPS_'),sg.Text("Motor 3 Angle: ", key='_mThreeAngle_')],
    [sg.Text("Motor 4 RPS: ", key='_mFourRPS_'),sg.Text("Motor 4 Angle: ", key='_mFourAngle_')],
    [sg.Text("Motor 5 RPS: ", key='_mFiveRPS_'),sg.Text("Motor 5 Angle: ", key='_mFiveAngle_')],
    [sg.Text("Motor 6 RPS: ", key='_mSixRPS_'),sg.Text("Motor 6 Angle: ", key='_mSixAngle_')],
    [sg.Graph(canvas_size=(sGCanSizeX, sGCanSizeY),
            graph_bottom_left=(sGBLx, sGBLy),
            graph_top_right=(halfRadius, halfRadius),
            background_color='white',
            #enable_events = True, 
            key='_side_')]
])

input_column = sg.Column([
    [sg.T("Z Input:              "),sg.Input(default_text="0", key='_coordInput_',size=(5,5))],
    [sg.T("Horizontal Input: "),sg.Input(default_text='0', key='_endEffHori_',size=(5,5))],
    [sg.T("Vertical Input:    "),sg.Input(default_text='0', key='_endEffVert_',size=(5,5))],
    [sg.T("Rotational Input: "),sg.Input(default_text='0', key='_gripperRotation_',size=(5,5))]
])

layout = [
    [sg.Menu(menu)],
    [sg.Graph(canvas_size=(radius+1, radius+1), 
            graph_bottom_left=(-radius, -radius), 
            graph_top_right=(radius, radius), 
            background_color='white',
            enable_events = True, 
            key='graph'),data_column,input_column
    ]]

window = sg.Window('Arm Position Visualizer', layout, finalize=True)  
graph = window['graph']
side = window['_side_']
coordText = window['_targetCoords_']

graph.DrawCircle((0,0), radius, line_color='red') # 1
graph.DrawLine((-10000, 0), (10000,0)) # 2
graph.DrawLine((0,-10000),(0,10000)) # 3
graph.Widget.config(cursor='circle')

side.DrawLine((-1000, 0), (1000, 0))
side.DrawLine((0, -1000), (0, 1000))

wristS = side.DrawCircle((1,1), SCALE*0.75, fill_color='red', line_color='black')
shoulderS = side.DrawCircle((1,1), SCALE*0.75, fill_color='black', line_color='black')
elbowS = side.DrawCircle((1,1), SCALE*0.75, fill_color='black', line_color='black')
gripperS = side.DrawCircle((1,1), SCALE*0.75, fill_color='green', line_color='black')

segmentOneS = side.DrawLine((0,0), (0,0))
segmentTwoS = side.DrawLine((0,0), (0,0))
segmentThreeS = side.DrawLine((0,0),(0,0))

def segOneVis():
    cirVis = side.DrawCircle((1,1),30*SCALE/2,line_color='red')
    cirVis2 = side.DrawCircle((1,30*SCALE/2), SCALE*0.75, fill_color='red', line_color='black')

#segOneVis()

for x in range(-60,60,10):
    xTScale = x*SCALE
    graph.DrawLine((xTScale, -10),(xTScale, 10))
    graph.DrawText(x, (xTScale+15, -20), color='green')

for y in range(-60,60,10):
    yTScale = y*SCALE
    graph.DrawLine((-10, yTScale),(10, yTScale))
    graph.DrawText(y, (+20, yTScale+15), color='blue')

wristG = graph.DrawCircle((0,0), 0, line_color='red')
target = graph.DrawCircle((0,0), 0, line_color='blue')
elbowG = graph.DrawCircle((0,0), 0, fill_color='black', line_color='black')
gripperG = graph.DrawCircle((0,0), 0, fill_color='green', line_color='black')

segmentOneG = graph.DrawLine((0,0), (0,0))
segmentTwoG = graph.DrawLine((0,0), (0,0))
segmentThreeG = graph.DrawLine((0,0),(0,0))


def UpdateLoop():
    global wristG
    global elbowG
    global segmentOneG
    global segmentTwoG
    global segmentThreeG
    global gripperG
    global wristS
    global elbowS
    global gripperS
    global segmentOneS
    global segmentTwoS
    global segmentThreeS

    while True:
        allMInfo = mainLoop(coords, endEffector)
        
        for i in range(6):
	        allMCAngle[i] = allMInfo[i][1]

        endX, endY, endZ, endDis, midDis, midX, midY, midZ, griX, griY, griZ, griDis  = GUIUpdate(allMCAngle)

        window['_currentCoords_'].update("Current Coordinates: X:{}, Y:{}, Z:{}".format(int(griX),int(griY),int(griZ)))
        window['_mOneRPS_'].update("Motor 1 RPS: {}".format(allMInfo[0][3]))
        window['_mTwoRPS_'].update("Motor 2 RPS: {}".format(allMInfo[1][3]))
        window['_mThreeRPS_'].update("Motor 3 RPS: {}".format(allMInfo[2][3]))
        window['_mFourRPS_'].update("Motor 4 RPS: {}".format(allMInfo[3][3]))
        window['_mFiveRPS_'].update("Motor 5 RPS: {}".format(allMInfo[4][3]))
        window['_mSixRPS_'].update("Motor 6 RPS: {}".format(allMInfo[5][3]))
        window['_mOneAngle_'].update("Motor 1 Angle: {}".format(allMInfo[0][1]))
        window['_mTwoAngle_'].update("Motor 2 Angle: {}".format(allMInfo[1][1]))
        window['_mThreeAngle_'].update("Motor 3 Angle: {}".format(allMInfo[2][1]))
        window['_mFourAngle_'].update("Motor 4 Angle: {}".format(allMInfo[3][1]))
        window['_mFiveAngle_'].update("Motor 5 Angle: {}".format(allMInfo[4][1]))
        window['_mSixAngle_'].update("Motor 6 Angle: {}".format(allMInfo[5][1]))

        corEndX, corEndY, corEndZ, corEndDis, corMidDis, corMidX, corMidY, corMidZ, corGriX, corGriY, corGriZ, corGriDis = endX*SCALE, endY*SCALE, endZ*SCALE, endDis*SCALE, midDis*SCALE, midX*SCALE, midY*SCALE, midZ*SCALE, griX*SCALE, griY*SCALE, griZ*SCALE, griDis*SCALE
        
        graph.delete_figure(segmentOneG)
        segmentOneG = graph.DrawLine((0,0), (corMidX,corMidY))
        graph.delete_figure(segmentTwoG)
        segmentTwoG = graph.DrawLine((corMidX,corMidY), (corEndX, corEndY))
        graph.delete_figure(segmentThreeG)
        segmentThreeG = graph.DrawLine((corEndX,corEndY), (corGriX, corGriY))

        graph.delete_figure(gripperG)
        gripperG = graph.DrawCircle((corGriX, corGriY), SCALE*1.5, fill_color='green', line_color='black')
        graph.delete_figure(wristG)
        wristG = graph.DrawCircle((corEndX, corEndY), SCALE*1.5, fill_color='red', line_color='black')
        graph.delete_figure(elbowG)
        elbowG = graph.DrawCircle((corMidX, corMidY), SCALE*1.5, fill_color='black', line_color='black')

        side.delete_figure(segmentOneS)
        segmentOneS = side.DrawLine((0,0), (corMidDis/2,corMidZ/2))
        side.delete_figure(segmentTwoS)
        segmentTwoS = side.DrawLine((corMidDis/2,corMidZ/2), (corEndDis/2, corEndZ/2))
        side.delete_figure(segmentThreeS)
        segmentThreeS = side.DrawLine((corEndDis/2,corEndZ/2), (corGriDis/2, corGriZ/2))

        side.delete_figure(gripperS)
        gripperS = side.DrawCircle((corGriDis/2, corGriZ/2), SCALE*0.75, fill_color='green', line_color='black')
        side.delete_figure(wristS)
        wristS = side.DrawCircle((corEndDis/2, corEndZ/2), SCALE*0.75, fill_color='red', line_color='black')
        side.delete_figure(elbowS)
        elbowS = side.DrawCircle((corMidDis/2, corMidZ/2), SCALE*0.75, fill_color='black', line_color='black')

def clickUpdate(x, y):
    global target
    graph.delete_figure(target)
    target = graph.DrawCircle((x-1,y-1), SCALE*1.5, fill_color='blue', line_color='black')

Math = threading.Thread(target=UpdateLoop, args=(), daemon=True)
Math.start()

while True:
    event, values = window.read() 

    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == '4::4':
        pass
    elif event == '5::5':
        pass
    elif event == '6::6':
        pass
    elif event == '7::7':
        pass
    elif event == '8::8':
        pass
    elif event == '9::9':
        pass
    elif event == '10::10':
        pass

    x = values['graph'][0]
    y = values['graph'][1]
    z = int(values['_coordInput_'])

    coordinates = "X:{}, Y:{}, Z:{}".format(int(x/SCALE),int(y/SCALE),z)
    coords = [x/SCALE, y/SCALE, z]
    endEffector = [int(values['_endEffHori_']),int(values['_endEffVert_']),int(values['_gripperRotation_'])]
    coordText.update("Target Coordinates:  {}".format(coordinates))
    
    clickUpdate(x,y)

window.close()