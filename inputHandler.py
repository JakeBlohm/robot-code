from inputs import get_gamepad
import PySimpleGUI as sg
import configparser


class inputHandler:
    config = configparser.ConfigParser()
    config.read('settings.ini')
    mode = config['DEFAULT']['controllermode']

    def __init__(self):
        try:
            self.events = get_gamepad()
        except:
            self.events = None

    def getGamepad(self):
        retry = True
        while retry:
            try:
                self.events = get_gamepad()
                print("Try get_gamepad.")
                retry = False
            except:
                choice = sg.Window('ERROR', [[sg.T('Gamepad not found, set to mouse mode.')],
                                             [sg.B(button_text="Continue in mouse mode", key='__cont__'),
                                              sg.B(button_text="Retry", key='__retry__')]],
                                   disable_close=True).read(close=True)
                if choice[0] == '__retry__':
                    print("Retry")
                    continue
                else:
                    print("Continue")
                    self.config.set('DEFAULT', 'controllermode', 'Mouse')
                    with open('settings.ini', 'w') as configfile:
                        self.config.write(configfile)
                    self.mode = self.config['DEFAULT']['controllermode']
                    retry = False

    def eventLoop(self):
        if self.mode == "Mouse":
            return 'mouse'
        elif self.mode == "Controller":
            # print("Interpret gamepad inputs.")
            self.getGamepad()
            for event in self.events:
                print(event.ev_type, event.code, event.state)
                return 'controller'


if __name__ == '__main__':
    handler = inputHandler()

    while True:
        result = handler.eventLoop()
        if result == 'mouse':
            print('mouse')
        elif result == 'controller':
            print('controller')
