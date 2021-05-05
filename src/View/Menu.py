import PySimpleGUI as sg


def makeMenu():
    layout = [[sg.Button('Indexing'), sg.Button('query')]]
    menu = sg.Window('App', layout)
    while True:  # Event Loop
        event, values = menu.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Indexing':
            # menu.close()
            folder_path = selectIndexingFolder()
        elif event == 'query':
            print('query')


def selectIndexingFolder():
    # see https://holypython.com/gui-with-python-file-browser-and-input-form-pysimplegui-part-iii/
    layout = [[sg.T("")], [sg.Text("Choose a folder: "), sg.Input(
        key="-IN2-", change_submits=True), sg.FolderBrowse(key="-IN-")], [sg.Button("Submit")]]

    # Building Window
    window = sg.Window('My File Browser', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "Submit":
            print("Collection folder: "+values["-IN-"])
            break
    window.close()
    if values["-IN-"] == None:
        return ''
    return values["-IN-"]
