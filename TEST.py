import PySimpleGUI as sg

layout = [[sg.Graph(canvas_size=(65536/100, 65536/200),
                    graph_bottom_left=(-32768, -1),
                    graph_top_right=(32767, 1),
                    background_color='white',
                    key='__graph__',
                    enable_events=True)]]

window = sg.Window("Controller Curve", layout, finalize=True)
graph = window['__graph__']

graph.DrawLine((-32768, 0), (32768, 0))
graph.DrawLine((0, 1), (0, -1))

for i in range(-32768, 32769, 1024):
    if i == 0:
        pass
    else:
        graph.DrawCircle((i, (i/32768)**3), radius=256, fill_color='red')
        print((i/32768)**3)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    print(values['__graph__'][0], values['__graph__'][1])

window.close()
