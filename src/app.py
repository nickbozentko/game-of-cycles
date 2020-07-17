import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
from dash.dependencies import Input, Output, State
from dash import callback_context, no_update
import re

import AppControl
from AppControl import app, boardList
import game


def getMainMenuLayout():
    htmlEls = [
        html.H1(
            [
                'Select a Board',
                html.Button(
                    '+',
                    style={
                        'backgroundColor': 'blue',
                        'color': 'white',
                        'border': 'none',
                        'height': '30px',
                        'width': '30px',
                        'margin-left': '80px'
                    }
                )
            ],
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
            dcc.Link(
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
                ),
                href="/game/"+board.boardName
            ),
        )

    return htmlEls

# Root layout
app.layout = html.Div([
        dcc.Location(id="url", refresh=False),
        html.Div(
            id="page-content"
        )
    ],
    id='root',
    style={'fontFamily': 'Courier New'}
)

# Page Navigation
@app.callback(
    [Output('page-content', 'children')],
    [Input('url', 'pathname')]
)
def displayPage(url):
    gamePattern = re.compile("/game/\w+")

    if url == '/':
        return [html.Div(
            getMainMenuLayout(),
            id='main-page',
        )]
    elif gamePattern.match(url):
        boardName = url.split('/')[2]
        AppControl.chosenBoardName = boardName

        return [html.Div(
            game.renderCurrentBoard(),
            id='game-page',
        )]

    return [html.Div(
        getMainMenuLayout(),
        id='main-page',
    )]



# Start dev server
if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port=3000, debug=True)
