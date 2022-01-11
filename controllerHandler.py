import inputs
from inputs import get_gamepad
import configparser

config = configparser.ConfigParser()
config.read('settings.ini')


class controllerHandler:
    def __init__(self):
        self.events = None
        self.errorWindow = ()

    def getController(self):
        try:
            self.events = get_gamepad()
            print("Try get_gamepad.")
            return True
        except inputs.UnpluggedError:
            print("setting mode")
            config.set('DEFAULT', 'controllermode', 'False')
            with open('settings.ini', 'w') as configfile:
                config.write(configfile)
            print("set mode")
            return False

    def interpretEvent(self):
        for event in self.events:
            evType = event.ev_type
            evCode = event.code
            evState = event.state


test = controllerHandler()
test.getController()
