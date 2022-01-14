from inputs import get_gamepad
import PySimpleGUI as sg
import threading
import time

scale = 4


class controller:
    def __init__(self):
        self.nx = 0
        self.ny = 0
        self.cx = 0
        self.cy = 0
        self.gamepadXAccel = 0
        self.gamepadYAccel = 0
        self.events = None

    def getGamepadValues(self):
        self.events = get_gamepad()
        # print(self.nx, ' | ', self.ny)

        for event in self.events:
            if event.ev_type == 'Absolute':
                # print(event.code)
                if event.code == 'ABS_X':
                    self.gamepadXAccel = (event.state / 32768) ** 3
                elif event.code == 'ABS_Y':
                    self.gamepadYAccel = (event.state / 32768) ** 3
                # print(self.gamepadXAccel, ' | ', self.gamepadYAccel)


class frame:
    def __init__(self):
        self.layout = [[sg.Graph(canvas_size=top_size,
                                 graph_bottom_left=top_bottomLeft,
                                 graph_top_right=top_topRight,
                                 background_color='white',
                                 enable_events=True,
                                 key='__topDown__')]]
        self.window = sg.Window("Gamepad Test", self.layout, finalize=True)
        self.graph = self.window['__topDown__']
        self.target = self.graph.DrawCircle((0, 0), 1.5 * scale, fill_color='blue')

    def update(self, xinc, yinc):
        self.graph.move_figure(self.target, xinc, yinc)
        # self.graph.delete_figure(self.target)
        # self.target = self.graph.DrawCircle((nx, ny), 1.5 * scale, fill_color='blue')


def gamepad():
    while True:
        handler.getGamepadValues()


def mainLoop():
    while True:
        newFrame.update(scale * handler.gamepadXAccel / 1.5, scale * handler.gamepadYAccel / 1.5)
        time.sleep(0.01)


top_size = ((120 * scale) + (5 * scale), (120 * scale) + (5 * scale))
top_bottomLeft = ((-60 * scale) - (5 * scale), (-60 * scale) - (5 * scale))
top_topRight = ((60 * scale) + (5 * scale), (60 * scale) + (5 * scale))

handler = controller()
newFrame = frame()
window = newFrame.window
graph = newFrame.graph
gpThread = threading.Thread(target=gamepad, args=(), daemon=False)
updateLoop = threading.Thread(target=mainLoop, args=(), daemon=False)
gpThread.start()
updateLoop.start()

while True:
    winevent, values = window.read()
    if winevent == sg.WIN_CLOSED:
        break

window.close()
