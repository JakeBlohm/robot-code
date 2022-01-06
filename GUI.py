import math
import PySimpleGUI as sg
import configparser
import threading
from GUICalc import GUIUpdate
from RobotArmControl import calcLoop

config = configparser.ConfigParser()
config.read('settings.ini')
scale = int(config['DEFAULT']['windowscale'])
controllerMode = config['DEFAULT']['controllermode'] == 'True'
if controllerMode:
    windowTitle = config['DEFAULT']['windowTitle'] + " (Controller)"
else:
    windowTitle = config['DEFAULT']['windowTitle'] + " (Mouse)"


def mainLoop():
    allMCAngle = [0, 0, 0, 0, 0, 0]
    while True:
        allMInfo = calcLoop(windowFrame.coords, windowFrame.endEffector)
        for i in range(6):
            allMCAngle[i] = allMInfo[i][1]

        wristX, wristY, wristZ, wristDis, elbowDis, elbowX, elbowY, elbowZ, gripperX, gripperY, gripperZ, gripperDis= GUIUpdate(allMCAngle)
        
        windowFrame.updateTopView(wristX, wristY, elbowX, elbowY, gripperX, gripperY)
        windowFrame.updateSideView(wristDis, wristZ, elbowDis, elbowZ, gripperDis, gripperZ)
        windowFrame.updateMotorInfo(gripperX, gripperY, gripperZ, allMInfo)


def createLayout():
    top_size = ((120 * scale) + (5 * scale), (120 * scale) + (5 * scale))
    top_bottomLeft = ((-60 * scale) - (5 * scale), (-60 * scale) - (5 * scale))
    top_topRight = ((60 * scale) + (5 * scale), (60 * scale) + (5 * scale))
    side_size = ((60 * scale) + (30 * scale), (60 * scale) + (0 * scale) + (5 * scale))
    side_bottomLeft = ((-30 * scale), (-0 * scale) - (5 * scale))
    side_topRight = ((60 * scale), (60 * scale))
    menu = sg.Menu(
        [["File", ["Settings", ["Scale", ["3::3", "4::4", "5::5", "6::6"], ["Mode", ["Mouse", "Controller"]]], "Exit"]]])

    leftColumn = sg.Column([
        [sg.Graph(canvas_size=top_size,
                  graph_bottom_left=top_bottomLeft,
                  graph_top_right=top_topRight,
                  background_color='white',
                  enable_events=True,
                  key='__topDown__')]
    ])
    manualInputColumn = sg.Column([
        [
            sg.Column([
                [sg.T("Z Input:")],
                [sg.T("Hori Input:")],
                [sg.T("Vert Input:")],
                [sg.T("Rota Input:")]
            ]),
            sg.Column([
                [sg.Input(default_text="0", key='__coordInput__', size=(5, 5))],
                [sg.Input(default_text='0', key='__endEffHori__', size=(5, 5))],
                [sg.Input(default_text='0', key='__endEffVert__', size=(5, 5))],
                [sg.Input(default_text='0', key='__gripperRotation__', size=(5, 5))]
            ])],
    ])

    def data():
        coord_labels = sg.Column([
            [sg.Text("Target Coords: ", key='__targetCoordsLabel')],
            [sg.Text("Current Coords: ", key='__currentCoordsLabel__')]
        ])
        coords = sg.Column([
            [sg.Text("{}".format(None), key='__targetCoords__')],
            [sg.Text("{}".format(None), key='__currentCoords__')]
        ])
        labels1 = sg.Column([
            [sg.Text("Motor 1 RPS: ", key='__mOneRPSLabel__')],
            [sg.Text("Motor 2 RPS: ", key='__mTwoRPSLabel__')],
            [sg.Text("Motor 3 RPS: ", key='__mThreeRPSLabel__')],
            [sg.Text("Motor 4 RPS: ", key='__mFourRPSLabel__')],
            [sg.Text("Motor 5 RPS: ", key='__mFiveRPSLabel__')],
            [sg.Text("Motor 6 RPS: ", key='__mSixRPSLabel__')]
        ])
        info1 = sg.Column([
            [sg.Text("{}".format(None), key='__mOneRPS__', size=(5, 1))],
            [sg.Text("{}".format(None), key='__mTwoRPS__', size=(5, 1))],
            [sg.Text("{}".format(None), key='__mThreeRPS__', size=(5, 1))],
            [sg.Text("{}".format(None), key='__mFourRPS__', size=(5, 1))],
            [sg.Text("{}".format(None), key='__mFiveRPS__', size=(5, 1))],
            [sg.Text("{}".format(None), key='__mSixRPS__', size=(5, 1))]
        ])
        labels2 = sg.Column([
            [sg.Text("Motor 1 Angle: ", key='__mOneAngleLabel__')],
            [sg.Text("Motor 2 Angle: ", key='__mTwoAngleLabel__')],
            [sg.Text("Motor 3 Angle: ", key='__mThreeAngleLabel__')],
            [sg.Text("Motor 4 Angle: ", key='__mFourAngleLabel__')],
            [sg.Text("Motor 5 Angle: ", key='__mFiveAngleLabel__')],
            [sg.Text("Motor 6 Angle: ", key='__mSixAngleLabel__')]
        ])
        info2 = sg.Column([
            [sg.Text("{}".format(None), key='__mOneAngle__', size=(5, 1))],
            [sg.Text("{}".format(None), key='__mTwoAngle__', size=(5, 1))],
            [sg.Text("{}".format(None), key='__mThreeAngle__', size=(5, 1))],
            [sg.Text("{}".format(None), key='__mFourAngle__', size=(5, 1))],
            [sg.Text("{}".format(None), key='__mFiveAngle__', size=(5, 1))],
            [sg.Text("{}".format(None), key='__mSixAngle__', size=(5, 1))]
        ])

        return sg.Column([
            [coord_labels, coords],
            [labels1, info1, labels2, info2]
        ])

    middleColumn = sg.Column([
        [data(), manualInputColumn],
        [sg.Graph(canvas_size=side_size,
                  graph_bottom_left=side_bottomLeft,
                  graph_top_right=side_topRight,
                  background_color='white',
                  # enable_events=True,
                  key='__sideOn__')]
    ], element_justification='center')

    layout = [[menu],[leftColumn, middleColumn]]
    return layout


class mainWindowFrame:
    def __init__(self, windowName, layout):
        self.side_gripper = None
        self.side_wrist = None
        self.side_endEffector = None
        self.side_elbow = None
        self.side_lowerArm = None
        self.side_upperArm = None
        self.top_gripper = None
        self.top_wrist = None
        self.top_elbow = None
        self.top_endEffector = None
        self.top_lowerArm = None
        self.top_upperArm = None
        self.targetCursorCoords = None
        self.target = None
        self.xVis = None
        self.yVis = None
        self.coords = [0, 0, 0]
        self.endEffector = [0, 0, 0]
        self.windowName = windowName
        self.layout = layout
        self.window = sg.Window(self.windowName, self.layout, finalize=True)
        self.topDown = self.window['__topDown__']
        self.sideOn = self.window['__sideOn__']
        self.initTopDown()
        self.initSideOn()

    def initTopDown(self):
        xAxis = self.topDown.DrawLine(((-60 * scale), 0), ((60 * scale), 0))
        yAxis = self.topDown.DrawLine((0, (-60 * scale)), (0, (60 * scale)))

        for x in range(-60, 61, 10):
            xScaled = x * scale
            self.topDown.DrawLine((xScaled, -10), (xScaled, 10))
            self.topDown.DrawText(x, (xScaled + 10, -10), color='green')
        for y in range(-60, 61, 10):
            yScaled = y * scale
            self.topDown.DrawLine((-10, yScaled), (10, yScaled))
            self.topDown.DrawText(y, (10, yScaled + 10), color='blue')

        armLimit = self.topDown.DrawCircle((0, 0), 60 * scale + 1, line_color='red')
        self.target = self.topDown.DrawCircle((0, 0), scale * 1.5, fill_color='blue', line_color='black')
        self.top_upperArm = self.topDown.DrawLine((0, 0), (0, 0))
        self.top_lowerArm = self.topDown.DrawLine((0, 0), (0, 0))
        self.top_endEffector = self.topDown.DrawLine((0, 0), (0, 0))
        self.top_elbow = self.topDown.DrawCircle((0, 0), scale * 1.5, fill_color='black', line_color='black')
        self.top_wrist = self.topDown.DrawCircle((0, 0), scale * 1.5, fill_color='red', line_color='black')
        self.top_gripper = self.topDown.DrawCircle((0, 0), scale * 1.5, fill_color='green', line_color='black')
        self.topDown.Widget.config(cursor='circle')

    def initSideOn(self):
        sDisAxis = self.sideOn.DrawLine(((-60 * scale), 0), ((60 * scale), 0))
        sZAxis = self.sideOn.DrawLine((0, (-60 * scale)), (0, (60 * scale)))

        for x in range(-60, 61, 10):
            xScaled = x * scale
            self.sideOn.DrawLine((xScaled, -10), (xScaled, 10))
            self.sideOn.DrawText(x, (xScaled + 10, -10), color='red')
        for y in range(-60, 61, 10):
            yScaled = y * scale
            self.sideOn.DrawLine((-10, yScaled), (10, yScaled))
            self.sideOn.DrawText(y, (10, yScaled + 10), color='goldenrod')

        self.side_upperArm = self.sideOn.DrawLine((0, 0), (0, 0))
        self.side_lowerArm = self.sideOn.DrawLine((0, 0), (0, 0))
        self.side_endEffector = self.sideOn.DrawLine((0, 0), (0, 0))
        self.side_elbow = self.sideOn.DrawCircle((0, 0), scale * 1.25, fill_color='black', line_color='black')
        self.side_wrist = self.sideOn.DrawCircle((0, 0), scale * 1.25, fill_color='red', line_color='black')
        self.side_gripper = self.sideOn.DrawCircle((0, 0), scale * 1.25, fill_color='green', line_color='black')

    def clickUpdate(self, newx, newy):
        self.topDown.delete_figure(self.target)
        self.target = self.topDown.DrawCircle((newx, newy), scale * 1.5, fill_color='blue', line_color='black')
        self.topDown.delete_figure(self.xVis)
        self.xVis = self.topDown.DrawLine((160 * scale, newy), (-160 * scale, newy))
        self.topDown.delete_figure(self.yVis)
        self.yVis = self.topDown.DrawLine((newx, 160 * scale), (newx, -160 * scale))
        self.topDown.delete_figure(self.targetCursorCoords)
        self.targetCursorCoords = self.topDown.DrawText("{} , {}".format(round(newx / scale, 2), round(newy / scale, 2)), (newx + 9 * scale, newy + 3 * scale))

    def updateTopView(self, wristX, wristY, elbowX, elbowY, gripperX, gripperY):
        # Top-Down View
        self.topDown.delete_figure(self.top_wrist)
        self.top_wrist = self.topDown.DrawCircle((wristX * scale, wristY * scale), scale * 1.5, fill_color='red', line_color='black')
        self.topDown.delete_figure(self.top_elbow)
        self.top_elbow = self.topDown.DrawCircle((elbowX * scale, elbowY * scale), scale * 1.5, fill_color='black', line_color='black')
        self.topDown.delete_figure(self.top_gripper)
        self.top_gripper = self.topDown.DrawCircle((gripperX * scale, gripperY * scale), scale * 1.5, fill_color='green', line_color='black')
        self.topDown.delete_figure(self.top_lowerArm)
        self.top_lowerArm = self.topDown.DrawLine((0, 0), (elbowX * scale, elbowY * scale))
        self.topDown.delete_figure(self.top_upperArm)
        self.top_upperArm = self.topDown.DrawLine((elbowX * scale, elbowY * scale), (wristX * scale, wristY * scale))
        self.topDown.delete_figure(self.top_endEffector)
        self.top_endEffector = self.topDown.DrawLine((wristX * scale, wristY * scale), (gripperX * scale, gripperY * scale))

    def updateSideView(self, wristDis, wristZ, elbowDis, elbowZ, gripperDis, gripperZ):
        self.sideOn.delete_figure(self.side_wrist)
        self.side_wrist = self.sideOn.DrawCircle((wristDis * scale, wristZ * scale), scale * 1.25, fill_color='red', line_color='black')
        self.sideOn.delete_figure(self.side_elbow)
        self.side_elbow = self.sideOn.DrawCircle((elbowDis * scale, elbowZ * scale), scale * 1.25, fill_color='black', line_color='black')
        self.sideOn.delete_figure(self.side_gripper)
        self.side_gripper = self.sideOn.DrawCircle((gripperDis * scale, gripperZ * scale), scale * 1.25, fill_color='green', line_color='black')
        self.sideOn.delete_figure(self.side_lowerArm)
        self.side_lowerArm = self.sideOn.DrawLine((0, 0), (elbowDis * scale, elbowZ * scale))
        self.sideOn.delete_figure(self.side_upperArm)
        self.side_upperArm = self.sideOn.DrawLine((elbowDis * scale, elbowZ * scale), (wristDis * scale, wristZ * scale))
        self.sideOn.delete_figure(self.side_endEffector)
        self.side_endEffector = self.sideOn.DrawLine((wristDis * scale, wristZ * scale), (gripperDis * scale, gripperZ * scale))

    def updateMotorInfo(self, gripperX, gripperY, gripperZ, allMInfo):
        self.window['__currentCoords__'].update("X:{}, Y:{}, Z:{}".format(int(gripperX), int(gripperY), int(gripperZ)))
        self.window['__mOneRPS__'].update("{}".format(allMInfo[0][3]))
        self.window['__mTwoRPS__'].update("{}".format(allMInfo[1][3]))
        self.window['__mThreeRPS__'].update("{}".format(allMInfo[2][3]))
        self.window['__mFourRPS__'].update("{}".format(allMInfo[3][3]))
        self.window['__mFiveRPS__'].update("{}".format(allMInfo[4][3]))
        self.window['__mSixRPS__'].update("{}".format(allMInfo[5][3]))
        self.window['__mOneAngle__'].update("{}".format(allMInfo[0][1]))
        self.window['__mTwoAngle__'].update("{}".format(allMInfo[1][1]))
        self.window['__mThreeAngle__'].update("{}".format(allMInfo[2][1]))
        self.window['__mFourAngle__'].update("{}".format(allMInfo[3][1]))
        self.window['__mFiveAngle__'].update("{}".format(allMInfo[4][1]))
        self.window['__mSixAngle__'].update("{}".format(allMInfo[5][1]))


if __name__ == '__main__':
    windowFrame = mainWindowFrame(windowTitle, createLayout())
    topDown = windowFrame.topDown
    update = threading.Thread(target=mainLoop, args=(), daemon=True)
    update.start()
    while True:
        event, values = windowFrame.window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == '3::3':
            config.set('DEFAULT', 'windowscale', '3')
            with open('settings.ini', 'w') as configfile:
                config.write(configfile)
            scale = int(config['DEFAULT']['windowscale'])
            windowFrame.window.close()
            windowFrame = mainWindowFrame(windowTitle, createLayout())
        elif event == '4::4':
            config.set('DEFAULT', 'windowscale', '4')
            with open('settings.ini', 'w') as configfile:
                config.write(configfile)
            scale = int(config['DEFAULT']['windowscale'])
            windowFrame.window.close()
            windowFrame = mainWindowFrame(windowTitle, createLayout())
        elif event == '5::5':
            config.set('DEFAULT', 'windowscale', '5')
            with open('settings.ini', 'w') as configfile:
                config.write(configfile)
            scale = int(config['DEFAULT']['windowscale'])
            windowFrame.window.close()
            windowFrame = mainWindowFrame(windowTitle, createLayout())
        elif event == '6::6':
            config.set('DEFAULT', 'windowscale', '6')
            with open('settings.ini', 'w') as configfile:
                config.write(configfile)
            scale = int(config['DEFAULT']['windowscale'])
            windowFrame.window.close()
            windowFrame = mainWindowFrame(windowTitle, createLayout())
        elif event == 'Mouse':
            config.set('DEFAULT', 'controllermode', 'False')
            with open('settings.ini', 'w') as configfile:
                config.write(configfile)
            controllerMode = config['DEFAULT']['controllermode']
            windowTitle = config['DEFAULT']['windowTitle'] + " (Mouse)"
            windowFrame.window.TKroot.title(windowTitle)
        elif event == 'Controller':
            config.set('DEFAULT', 'controllermode', 'True')
            with open('settings.ini', 'w') as configfile:
                config.write(configfile)
            controllerMode = config['DEFAULT']['controllermode']
            windowTitle = config['DEFAULT']['windowTitle'] + " (Controller)"
            windowFrame.window.TKroot.title(windowTitle)
        try:
            if controllerMode:
                pass
            else:
                xIn = values['__topDown__'][0]
                yIn = values['__topDown__'][1]
                zIn = int(values['__coordInput__'])
                windowFrame.clickUpdate(xIn, yIn)

            coordinates = "X:{}, Y:{}, Z:{}".format(int(xIn / scale), int(yIn / scale), zIn)
            windowFrame.coords = [xIn/scale, yIn/scale, zIn]
            windowFrame.endEffector = [int(values['__endEffHori__']), int(values['__endEffVert__']), int(values['__gripperRotation__'])]
            windowFrame.window['__targetCoords__'].update("{}".format(coordinates))
        except:
            print("GUI Exception: Coordinate Error")

windowFrame.window.close()
