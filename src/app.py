import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
from dash.dependencies import Input, Output, State
from dash import callback_context, no_update

import AppControl
from AppControl import app, boardList
import game


def getMainMenuLayout():
    htmlEls = [
        html.H1(
            'Select a Board',
            id='mainMenu',
            style={
                'textAlign': 'center',
                'display': 'block' if AppControl.page == 'HOME' else 'hidden'
            }
        ),
    ]

    # Add board as option on main menu
    for board in boardList:
        graph = board.getGraph()
        cytoscapeEdges = graph.getCytoscapeGraphEdges()
        htmlEls.append(
            html.Div(
                [
                    html.H2(
                        board.boardName,
                        id=board.boardName+'Name',
                        style={'textAlign': 'center'}
                    ),
                    cyto.Cytoscape(
                        id=board.boardName+'Preview',
                        layout={'name': 'preset'},
                        style={'width': '100%', 'height': '200px'},
                        stylesheet=board.getCytoscapeStylesheet(),
                        elements=board.getCytoscapeNodes() + cytoscapeEdges,
                        userZoomingEnabled=False,
                        userPanningEnabled=False
                    ),
                ],
                id=board.boardName,
                style={'border': '2px solid gray', 'margin': '5px'}
            )
        )

    return htmlEls

def getPages():
    return [
        html.Div(
            getMainMenuLayout(),
            id='main-page',
            style={ 'display': 'block' if AppControl.page == 'HOME' else 'none' }
        ),
        html.Div(
            game.renderCurrentBoard(),
            id='game-page',
            style={ 'display': 'block' if AppControl.page == 'GAME' else 'none' }
        )
    ]

# Set layout to main menu
app.layout = html.Div(
    getPages(),
    id='root',
    style={'fontFamily': 'Courier New'}
)

# Triggered when a main menu option is clicked
# Sets page-content to selected game board
@app.callback(
    Output('root', 'children'),
    [Input(board.boardName, 'n_clicks') for board in boardList] + [Input('mainMenuBtn', 'n_clicks')]
)
def handleChangePage(*args):
    trigger = callback_context.triggered[0]['prop_id']
    if trigger == '.':
        return no_update

    if(trigger == 'mainMenuBtn.n_clicks'):
        AppControl.page = 'HOME'
        return getPages()

    boardName = trigger.split('.')[0]
    AppControl.chosenBoardName = boardName
    AppControl.page = 'GAME'
    return getPages()



# Start dev server
if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port=3000, debug=True)
