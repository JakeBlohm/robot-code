import PySimpleGUI as sg

def main_window(theme, background_color, window=None):

    sg.theme(theme)

    menu_def = [['Customize GUI', ['Background', ['White::white', 'Purple::purple']]]]
    layout = [[sg.Menu(menu_def, key='-MENU-', text_color='black', background_color=background_color)]]
    new_window = sg.Window('Fast reader by Hary', layout, finalize=True)
    if window is not None:
        window.close()
    return new_window

theme, background_color = 'DarkGrey9', 'green'
window = main_window(theme, background_color)

while True:

    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Purple::purple':
        theme, background_color = 'LightPurple', 'purple'
        window = main_window(theme, background_color, window)
    elif event == 'White::white':
        theme, background_color = 'DarkGrey6', 'white'
        window = main_window(theme, background_color, window)

window.close()