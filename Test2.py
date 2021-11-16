import PySimpleGUI as sg

SCALE = 8

tooltipCat = None

maxArmLength = 60
radius = maxArmLength*SCALE
halfRadius = radius/2

menu = [["File", ["Settings","Exit"]]]

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
    [sg.T("Z Input:              "),sg.Input(default_text="0", key='_coordInput_')],
    [sg.T("Horizontal Input: "),sg.Input(default_text='0', key='_endEffHori_')],
    [sg.T("Vertical Input:    "),sg.Input(default_text='0', key='_endEffVert_')],
    [sg.T("Rotational Input: "),sg.Input(default_text='0', key='_gripperRotation_')]
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

while True:
    event, values = window.read() 

    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'Settings':
        pass

    x = values['graph'][0]
    y = values['graph'][1]
    z = int(values['_coordInput_'])

    coordinates = "{},{}".format(int(x/SCALE),int(y/SCALE))

window.close()