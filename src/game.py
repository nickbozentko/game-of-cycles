import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
from dash.dependencies import Input, Output, State
from dash import callback_context, no_update

import GameStateControl
import AppControl
from AppControl import app

# Use this as default board
import boards.Triforce as Triforce


# Returns the game board layout of the currently selected board
def renderCurrentBoard():
    AppControl.CHOSEN_GRAPH = AppControl.boardMap.get(AppControl.chosenBoardName, Triforce)
    AppControl.graph = AppControl.CHOSEN_GRAPH.getGraph()
    cytoscapeEdges = AppControl.graph.getCytoscapeGraphEdges()

    return html.Div([
        html.H1(
            'Player ' + str(GameStateControl.playerMove) + ' Move',
            style={'textAlign': 'center'},
            id='playerMove'
        ),
        html.H1(
            '',
            style={'display': 'none'},
            id='winnerText'
        ),
        cyto.Cytoscape(
            id='myGraph',
            layout={'name': 'preset'},
            style={
                'width': '100%', 
                'height': '500px',
            },
            stylesheet=AppControl.CHOSEN_GRAPH.getCytoscapeStylesheet(),
            elements=AppControl.CHOSEN_GRAPH.getCytoscapeNodes() + cytoscapeEdges,
            userZoomingEnabled=False,
            userPanningEnabled=False,
        ),
        html.Div(
            [
                html.Button(
                    'Reset',
                    id='resetBtn',
                    n_clicks=0,
                    style={
                        'backgroundColor': 'red',
                        'color': 'white',
                        'border': 'none',
                        'height': '50px',
                        'width': '150px',
                        'margin': '20px'
                    }
                ),
                dcc.Link(
                    html.Button(
                        'Main Menu',
                        id='mainMenuBtn',
                        n_clicks=0,
                        style={
                            'backgroundColor': 'blue',
                            'color': 'white',
                            'border': 'none',
                            'height': '50px',
                            'width': '150px',
                            'margin': '20px'
                        }
                    ),
                    href='/'
                ),
                html.H3(
                    '',
                    style={
                        'color': 'red',
                        'textAlign': 'center',
                        'margin': 'auto'
                    },
                    id='errorText'
                )
            ],
            style={
                'display': 'flex',
                'flexDirection': 'row',
                'alignContent': 'center'
            }
        )
    ])


# Triggered when a node is clicked or the reset button is clicked
# Returns Cytoscape graph elements (both nodes and edges) and error text if invalid move is made
@app.callback(
    [Output('myGraph', 'elements'), Output('errorText', 'children')],
    [Input('myGraph', 'tapNodeData'), Input('resetBtn', 'n_clicks')],
    [State('myGraph', 'elements'), State('playerMove', 'children')])
def handleNodeClick(node, nClicks, elements, currPlayerMove):
    """ 
    I do not like that the "reset graph" and "handle node click"
    functionality share the same function but it must be this way
    due to a limitation with Dash. Both of these functionalities
    output the "myGraph->elements" item. Dash only allows you to have one 
    callback to output the same item.
    """

    # Handle reset click, as described above
    if nClicks != GameStateControl.resetClicks and nClicks != 0:
        GameStateControl.resetClicks = nClicks
        GameStateControl.selectedNode = None
        GameStateControl.playerMove = 1
        AppControl.graph.removeAllMarkedEdges()

        nodes = AppControl.CHOSEN_GRAPH.getCytoscapeNodes()
        edges = AppControl.graph.getCytoscapeGraphEdges()

        GameStateControl.gameIsOver = False

        return [nodes+edges, '']

    # Handle random trigger when board loads
    if node is None:
        return [elements, '']

    # Handle node click if game is over
    if GameStateControl.gameIsOver:
        return [elements, '']

    # Handle first node selected
    if GameStateControl.selectedNode is None or GameStateControl.selectedNode == node:
        GameStateControl.selectedNode = node

        # Highlight selected node
        found = list(filter(lambda x: str(
            x['data']['id']) == str(node['id']), elements))[0]
        found['classes'] = 'selected'

        return [elements, '']

    # If we get here, an edge was selected to be marked
    cytoEdge = (GameStateControl.selectedNode, node)
    sourceNode = list(filter(lambda x: str(x.id) == str(
        cytoEdge[0]['id']), AppControl.graph.nodes))[0]
    targetNode = list(filter(lambda x: str(x.id) == str(
        cytoEdge[1]['id']), AppControl.graph.nodes))[0]
    edge = (sourceNode, targetNode)

    nodes = AppControl.CHOSEN_GRAPH.getCytoscapeNodes()

    # Unhighlight all nodes
    for n in nodes:
        n['classes'] = ''
    edges = AppControl.graph.getCytoscapeGraphEdges()

    GameStateControl.selectedNode = None

    # Return without adding a new edge if it is not an actual edge in our graph
    if not AppControl.graph.isUnmarkedEdgeInGraph(edge):
        return [nodes+edges, 'Tried to mark a non-existent edge']

    # Return without adding a new edge if the edge is already marked
    if AppControl.graph.isEdgeMarked(edge):
        return [nodes+edges, 'Tried to mark an edge that was already marked']

    # Return without adding a new edge if the edge would create a sink or source
    if sourceNode.wouldOutboundNodeCreateSource(targetNode):
        return [nodes+edges, 'Tried to create a source']

    if targetNode.wouldInboundNodeCreateSink(sourceNode):
        return [nodes+edges, 'Tried to create a sink']

    # If we get here, a valid edge was marked
    AppControl.graph.addDirectedEdge(edge)
    edges = AppControl.graph.getCytoscapeGraphEdges()

    return [nodes+edges, '']


# Update player turn when node is clicked, after graph is updated
@app.callback(
    Output('playerMove', 'children'),
    [Input('myGraph', 'elements')]
)
def updatePlayerMove(graphEls):
    return 'Player 1 Turn' if sum(1 for el in graphEls if el['data'].get('type', '') == 'directed') % 2 == 0 else 'Player 2 Turn'


# Update the winner text if there is a winner
@app.callback(
    [
        Output('winnerText', 'children'),
        Output('winnerText', 'style'),
        Output('playerMove', 'style')
    ],
    [
        Input('myGraph', 'elements'),
        Input('playerMove', 'children')
    ]
)
def updateWinnerText(graphEls, playerMove):

    gameOver = AppControl.graph.doesContainCycle() or not AppControl.graph.doesHaveMarkableEdge()
    if(not gameOver):
        return [
            '', 
            {'display': 'none'}, 
            {'textAlign': 'center'}
        ]

    GameStateControl.gameIsOver = True
    winnerNum = '2' if playerMove.split(' ')[1] == '1' else '1'
    return [
        'Player ' + winnerNum + ' Wins', 
        {
            'display': 'block', 
            'textAlign': 'center', 
            'color': 'red'
        }, 
        {'display': 'none'}
    ]
