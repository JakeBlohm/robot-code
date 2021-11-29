import math
from ArmPositioner import MAX_ARM_LENGTH
global lastCoords
lastCoords = [0 ,40, 0]

def CoordsValidation(coords):
    global lastCoords
    tarDistance = (math.sqrt((coords[0]**2)+(coords[1]**2)+(coords[2]**2))+(0))
    if tarDistance <= MAX_ARM_LENGTH:
        lastCoords = coords
        return coords
    else:
        return lastCoords