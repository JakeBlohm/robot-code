import inputs
from inputs import get_gamepad
import PySimpleGUI as sg
import configparser

config = configparser.ConfigParser()
config.read('settings.ini')


class controllerHandler:
    def __init__(self):
        self.events = None

    def getController(self):
        retry = True
        while retry:
            try:
                self.events = get_gamepad()
                print("Try get_gamepad.")
            except inputs.UnpluggedError:
                choice = sg.Window('ERROR', [[sg.T('Gamepad not found, set to mouse mode.')],
                                             [sg.B(button_text="Continue in mouse mode", key='__cont__'),
                                              sg.B(button_text="Retry", key='__retry__')]],
                                   disable_close=True, keep_on_top=True).read(close=True)
                if choice[0] == '__retry__':
                    print("Retry")
                    continue
                else:
                    print("Continue")
                    config.set('DEFAULT', 'controllermode', 'False')
                    with open('settings.ini', 'w') as configfile:
                        config.write(configfile)
                    retry = False

    def interpretEvent(self):
        for event in self.events:
            evType = event.ev_type
            evCode = event.code
            evState = event.state


test = controllerHandler()
test.getController()
