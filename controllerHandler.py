from inputs import get_gamepad
import configparser

config = configparser.ConfigParser()
config.read('settings.ini')
controllerMode = config['DEFAULT']['controllermode']

def move(currX, currY, xDir, yDir):
    if xDir > 0:
        newX = currX + xDir/50000
        print("New: {}, Old: {}".format(newX, currX))
    elif xDir < 0:
        newX = currX + xDir/50000
        print("New: {}, Old: {}".format(newX, currX))
    else:
        newX = currX
        print("New: {}, Old: {}".format(newX, currX))

    if yDir > 0:
        newY = currY + yDir/50000
        print("New: {}, Old: {}".format(newY, currY))
    elif yDir < 0:
        newY = currY + yDir/50000
        print("New: {}, Old: {}".format(newY, currY))
    else:
        newY = currY
        print("New: {}, Old: {}".format(newY, currY))
    return newX, newY


def getControllerInput(x, y):
    print("hi")
    xDir = 0
    yDir = 0
    lastXDir = 0
    lastYDir = 0
    try:
        gamepadEvents = get_gamepad()
        for controllerEvent in gamepadEvents:
            if controllerEvent.ev_type == "Absolute" and controllerEvent.code == "ABS_X":
                xDir = controllerEvent.state
                # print(1, xDir)
            elif controllerEvent.ev_type == "Absolute" and lastXDir == xDir:
                xDir = lastXDir
                # print(2, xDir)
            if controllerEvent.ev_type == "Absolute" and controllerEvent.code == "ABS_Y":
                yDir = controllerEvent.state
                # print(3, yDir)
            elif controllerEvent.ev_type == "Absolute" and lastYDir == yDir:
                yDir = lastYDir
                # print(4, yDir)
        lastXDir = xDir
        lastYDir = yDir

        x, y = move(x, y, xDir, yDir)
        print(x, y)
        return x, y
    except:
        config.set('DEFAULT', 'controllermode', 'Mouse')
        with open('settings.ini', 'w') as configfile:
            config.write(configfile)

