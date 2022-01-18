import PySimpleGUI as sg
import inputs
from inputs import get_gamepad
import configparser
import threading
import time
import localMath
from GUICalc import GUIUpdate
from RobotArmControl import calcLoop

config = configparser.ConfigParser()
config.read('settings.ini')
scale = int(config['DEFAULT']['windowscale'])
run = True


class controller:
    def __init__(self):
        self.gamepadXAccel = 0
        self.gamepadYAccel = 0
        self.moving = False
        self.controllerMode = config['DEFAULT']['controllermode'] == 'True'

    def getGamepadValues(self):
        events = get_gamepad()
        for ctrevent in events:
            # Get user input values
            self.moving = ctrevent.ev_type == 'Absolute'
            if self.moving:
                # Get left stick inputs and convert into acceleration value
                # ===========
                # Get X axis values
                if ctrevent.code == 'ABS_X':
                    self.gamepadXAccel = (ctrevent.state / 32768)  # ** 3
                    if 0.1 >= localMath.truncate(self.gamepadXAccel, 1) >= -0.1:
                        self.gamepadXAccel = 0

                # Get Y axis values
                elif ctrevent.code == 'ABS_Y':
                    self.gamepadYAccel = (ctrevent.state / 32768)  # ** 3
                    if 0.1 >= localMath.truncate(self.gamepadYAccel, 1) >= -0.1:
                        self.gamepadYAccel = 0


class windowcls:
    def __init__(self):
        self.endEffector = [0, 0, 0]
        self.side_gripper = None
        self.side_wrist = None
        self.side_elbow = None
        self.side_endEffector = None
        self.side_lowerArm = None
        self.side_upperArm = None
        self.top_gripper = None
        self.top_wrist = None
        self.top_endEffector = None
        self.top_lowerArm = None
        self.top_upperArm = None
        self.top_elbow = None
        self.target = None
        self.armLimit = None
        self.mx = 0
        self.my = 0
        self.mz = 0
        if controller.controllerMode:
            self.windowName = 'Arm Visualiser [Controller]'
        else:
            self.windowName = 'Arm Visualiser [Mouse]'
        self.window = sg.Window(self.windowName, self.layout(), finalize=True)
        self.topDown = self.window['__topDown__']
        self.sideOn = self.window['__sideOn__']
        self.initGraphs()
        self.targetCurrentCoords = [0, 0, 0]

    def targetUpdate(self, mx, my, cx, cy, mz):
        if controller.controllerMode:
            self.topDown.move_figure(self.target, cx, cy)
            self.targetCurrentCoords[0] += cx / scale
            self.targetCurrentCoords[1] += cy / scale
            self.targetCurrentCoords[2] = mz

        else:
            self.topDown.delete_figure(self.target)
            self.target = self.topDown.DrawCircle((mx, my), scale * 1.5, fill_color='blue', line_color='black')
            self.targetCurrentCoords[0] = mx / scale
            self.targetCurrentCoords[1] = my / scale
            self.targetCurrentCoords[2] = mz

    def initGraphs(self):
        # Initialize the shapes drawn to the graph objects
        # ======
        # Top-Down View
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

        self.armLimit = self.topDown.DrawCircle((0, 0), 60 * scale + 1, line_color='black')
        self.topDown.DrawCircle((0, 0), 60 * scale + 1, line_color='red')
        self.target = self.topDown.DrawCircle((0, 0), scale * 1.5, fill_color='blue', line_color='black')
        self.top_upperArm = self.topDown.DrawLine((0, 0), (0, 0))
        self.top_lowerArm = self.topDown.DrawLine((0, 0), (0, 0))
        self.top_endEffector = self.topDown.DrawLine((0, 0), (0, 0))
        self.top_elbow = self.topDown.DrawCircle((0, 0), scale * 1.5, fill_color='black', line_color='black')
        self.top_wrist = self.topDown.DrawCircle((0, 0), scale * 1.5, fill_color='red', line_color='black')
        self.top_gripper = self.topDown.DrawCircle((0, 0), scale * 1.5, fill_color='green', line_color='black')
        self.topDown.Widget.config(cursor='circle')

        # Side-On View
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

    def updateTopView(self, wristX, wristY, elbowX, elbowY, gripperX, gripperY, armLimitRad, offX, offY):
        # Top-Down View
        self.topDown.delete_figure(self.armLimit)
        self.armLimit = self.topDown.DrawCircle((offX * scale, offY * scale), armLimitRad * scale + 1, line_color='black')

        self.topDown.delete_figure(self.top_wrist)
        self.top_wrist = self.topDown.DrawCircle((wristX * scale, wristY * scale), scale * 1.5, fill_color='red',
                                                 line_color='black')
        self.topDown.delete_figure(self.top_elbow)
        self.top_elbow = self.topDown.DrawCircle((elbowX * scale, elbowY * scale), scale * 1.5, fill_color='black',
                                                 line_color='black')
        self.topDown.delete_figure(self.top_gripper)
        self.top_gripper = self.topDown.DrawCircle((gripperX * scale, gripperY * scale), scale * 1.5,
                                                   fill_color='green', line_color='black')
        self.topDown.delete_figure(self.top_lowerArm)
        self.top_lowerArm = self.topDown.DrawLine((0, 0), (elbowX * scale, elbowY * scale))
        self.topDown.delete_figure(self.top_upperArm)
        self.top_upperArm = self.topDown.DrawLine((elbowX * scale, elbowY * scale), (wristX * scale, wristY * scale))
        self.topDown.delete_figure(self.top_endEffector)
        self.top_endEffector = self.topDown.DrawLine((wristX * scale, wristY * scale),
                                                     (gripperX * scale, gripperY * scale))

    def updateSideView(self, wristDis, wristZ, elbowDis, elbowZ, gripperDis, gripperZ):
        self.sideOn.delete_figure(self.side_wrist)
        self.side_wrist = self.sideOn.DrawCircle((wristDis * scale, wristZ * scale), scale * 1.25, fill_color='red',
                                                 line_color='black')
        self.sideOn.delete_figure(self.side_elbow)
        self.side_elbow = self.sideOn.DrawCircle((elbowDis * scale, elbowZ * scale), scale * 1.25, fill_color='black',
                                                 line_color='black')
        self.sideOn.delete_figure(self.side_gripper)
        self.side_gripper = self.sideOn.DrawCircle((gripperDis * scale, gripperZ * scale), scale * 1.25,
                                                   fill_color='green', line_color='black')
        self.sideOn.delete_figure(self.side_lowerArm)
        self.side_lowerArm = self.sideOn.DrawLine((0, 0), (elbowDis * scale, elbowZ * scale))
        self.sideOn.delete_figure(self.side_upperArm)
        self.side_upperArm = self.sideOn.DrawLine((elbowDis * scale, elbowZ * scale),
                                                  (wristDis * scale, wristZ * scale))
        self.sideOn.delete_figure(self.side_endEffector)
        self.side_endEffector = self.sideOn.DrawLine((wristDis * scale, wristZ * scale),
                                                     (gripperDis * scale, gripperZ * scale))

    def updateMotorInfo(self, gripperX, gripperY, gripperZ, allMInfo):
        coordinates = 'X:{}, Y:{}, Z:{}'.format(self.mx, self.my, self.mz)
        windowFrame.window['__targetCoords__'].update("{}".format(coordinates))
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

    @staticmethod
    def layout():
        top_size = ((120 * scale) + (5 * scale), (120 * scale) + (5 * scale))
        top_bottomLeft = ((-60 * scale) - (5 * scale), (-60 * scale) - (5 * scale))
        top_topRight = ((60 * scale) + (5 * scale), (60 * scale) + (5 * scale))
        side_size = ((60 * scale) + (30 * scale), (60 * scale) + (0 * scale) + (5 * scale))
        side_bottomLeft = ((-30 * scale), (-0 * scale) - (5 * scale))
        side_topRight = ((60 * scale), (60 * scale))
        menu = sg.Menu(
            [["File",
              ["Settings", ["Scale", ["3::3", "4::4", "5::5", "6::6"], ["Mode", ["Mouse", "Controller"]]], "Exit"]]])

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
                      key='__sideOn__')]
        ], element_justification='center')

        layout = [[menu], [leftColumn, middleColumn]]
        return layout


def controllerLoop():
    while True:
        if controller.controllerMode:
            controller.getGamepadValues()
        else:
            time.sleep(0.017)


def mainLoop():
    allMCAngle = [0, 0, 0, 0, 0, 0]
    lastCoords = [0, 0, 0]
    while True:
        # print(windowFrame.targetCurrentCoords)
        if controller.controllerMode:
            windowFrame.targetUpdate(0, 0, scale * controller.gamepadXAccel, scale * controller.gamepadYAccel,
                                     windowFrame.mz)
        elif not controller.controllerMode:
            pass
        # try:
        # Temp fix until you fix
        # if windowFrame.targetCurrentCoords[2] is None:
        #    windowFrame.targetCurrentCoords[2] = 0
        allMInfo, Off = calcLoop(windowFrame.targetCurrentCoords, windowFrame.endEffector, lastCoords)
        offX, offY, armLimitRad  = Off[0], Off[1], Off[2]
        lastCoords[0] = windowFrame.targetCurrentCoords[0]
        lastCoords[1] = windowFrame.targetCurrentCoords[1]
        lastCoords[2] = windowFrame.targetCurrentCoords[2]

        # except TypeError:
        #    print("Motor Calculation Error [0x0003a]")
        #    allMInfo = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        for i in range(6):
            allMCAngle[i] = allMInfo[i][1]

        wristX, wristY, wristZ, wristDis, elbowDis, elbowX, elbowY, elbowZ, gripperX, gripperY, gripperZ, gripperDis = GUIUpdate(
            allMCAngle)

        windowFrame.updateTopView(wristX, wristY, elbowX, elbowY, gripperX, gripperY, armLimitRad, offX, offY)
        windowFrame.updateSideView(wristDis, wristZ, elbowDis, elbowZ, gripperDis, gripperZ)
        windowFrame.updateMotorInfo(gripperX, gripperY, gripperZ, allMInfo)


if __name__ == '__main__':
    controller = controller()
    windowFrame = windowcls()
    window = windowFrame.window
    inputThread = threading.Thread(target=controllerLoop, args=(), daemon=True)
    main = threading.Thread(target=mainLoop, args=(), daemon=True)
    inputThread.start()
    main.start()
    while run:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            run = False
        elif event == '3::3':
            config.set('DEFAULT', 'windowscale', '3')
            with open('settings.ini', 'w') as configfile:
                config.write(configfile)
            scale = int(config['DEFAULT']['windowscale'])
            window.close()
            windowFrame = windowcls()
            window = windowFrame.window
        elif event == '4::4':
            config.set('DEFAULT', 'windowscale', '4')
            with open('settings.ini', 'w') as configfile:
                config.write(configfile)
            scale = int(config['DEFAULT']['windowscale'])
            window.close()
            windowFrame = windowcls()
            window = windowFrame.window
        elif event == '5::5':
            config.set('DEFAULT', 'windowscale', '5')
            with open('settings.ini', 'w') as configfile:
                config.write(configfile)
            scale = int(config['DEFAULT']['windowscale'])
            window.close()
            windowFrame = windowcls()
            window = windowFrame.window
        elif event == '6::6':
            config.set('DEFAULT', 'windowscale', '6')
            with open('settings.ini', 'w') as configfile:
                config.write(configfile)
            scale = int(config['DEFAULT']['windowscale'])
            window.close()
            windowFrame = windowcls()
            window = windowFrame.window
        elif event == 'Mouse':
            config.set('DEFAULT', 'controllermode', 'False')
            with open('settings.ini', 'w') as configfile:
                config.write(configfile)
            controller.controllerMode = config['DEFAULT']['controllermode'] == 'True'
            windowTitle = config['DEFAULT']['windowTitle'] + " [Mouse]"
            windowFrame.window.TKroot.title(windowTitle)
        elif event == 'Controller':
            config.set('DEFAULT', 'controllermode', 'True')
            with open('settings.ini', 'w') as configfile:
                config.write(configfile)
            controller.controllerMode = config['DEFAULT']['controllermode'] == 'True'
            windowTitle = config['DEFAULT']['windowTitle'] + " [Controller]"
            windowFrame.window.TKroot.title(windowTitle)
            try:
                get_gamepad()
            except inputs.UnpluggedError:
                print("Gamepad Unplugged Error [0x0002a]")
                config.set('DEFAULT', 'controllermode', 'False')
                with open('settings.ini', 'w') as configfile:
                    config.write(configfile)
                controller.controllerMode = config['DEFAULT']['controllermode'] == 'True'
                windowTitle = config['DEFAULT']['windowTitle'] + " [Mouse]"
                windowFrame.window.TKroot.title(windowTitle)
        try:
            if not controller.controllerMode:
                windowFrame.mx = values['__topDown__'][0]
                windowFrame.my = values['__topDown__'][1]
                windowFrame.mz = float(values['__coordInput__'])
                windowFrame.targetUpdate(windowFrame.mx, windowFrame.my, 0, 0, windowFrame.mz)
        except AttributeError:
            print("Mouse Coordinate Error [0x0001a]")
        except TypeError:
            print("Mouse Coordinate Error [0x0001b]")

window.close()
