from classes.Node import Node
from classes.Cell import Cell
from classes.Graph import Graph

boardName = 'Square'

nodes = [Node() for i in range(4)]
cells = [
    Cell([nodes[0], nodes[1], nodes[2], nodes[3]]),
]
graph = Graph(cells)

cytoscapeNodes = [
    {
        'data': {
            'id': nodes[0].id,
        },
        'position': {
            'x': 0,
            'y': 0
        },
        'grabbable': False
    },
    {
    'data': {
            'id': nodes[1].id,
        },
        'position': {
            'x': 100,
            'y': 0
        },
        'grabbable': False
    },
        {
        'data': {
            'id': nodes[2].id,
        },
        'position': {
            'x': 100,
            'y': 100
        },
        'grabbable': False
    },
    {
        'data': {
            'id': nodes[3].id,
        },
        'position': {
            'x': 0,
            'y': 100
        },
        'grabbable': False
    },
]

cytoscapeStylesheet = [
    {
        'selector': 'edge',
        'style': {
            'line-color': 'grey'
        }
    },
    {
        'selector': '[type ^= "directed"]',
        'style': {
            'mid-target-arrow-color': 'blue',
            'mid-target-arrow-shape': 'triangle',
            'arrow-scale': 2
        }
    },
    {
        'selector': 'node',
        'style': {
            'background-color': 'black',
            'width': '15%',
            'height': '15%'
        }
    },
    {
        'selector': '.selected',
        'style': {
            'background-color': 'red'
        }
    },
    {
        'selector': '[type ^= "unmarkable"]',
        'style': {
            'mid-target-arrow-color': 'red',
            'mid-target-arrow-shape': 'tee',
            'arrow-scale': 2
        }
    },
]

def getGraph():
    return graph

def getBoardName():
    return boardName

def getCytoscapeNodes():
    return cytoscapeNodes

def getCytoscapeStylesheet():
    return cytoscapeStylesheet