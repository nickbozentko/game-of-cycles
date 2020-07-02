# Game of Cycles

## About the Game of Cycles

### Background

The Game of Cycles, introduced by Su (2020), is played on a simple connected planar graph, and players take turns marking edges with arrows according to certain rules that give the game a distinct topological flavor. The object of the game is to produce a cycle cell—which is a cell surrounded by arrows all cycling in one direction — or to make the last possible move. 

### How to Play

Start with any simple connected planar graph of dots (vertices) and edges. It divides the plane into regions, which we call cells. A graph together with its bounded cells is a game board. Two players take turns marking one unmarked edge with an arrow pointing along the edge in one direction or the other. The arrows must obey a sink-source rule: players are not allowed to create a sink (a dot all of whose edges are all marked pointing toward that dot) or a source (a dot all of whose edges are marked pointing away from that dot). Each edge can admit only one arrow, and arrows serve the same function in the game no matter who marks them.

The object of the game is to produce a cycle cell, a single cell in the board whose boundary edges are all marked by arrows all cycling in the same direction (either clockwise or counterclockwise). The first person to create a cycle cell wins the game, but if play ends without a cycle cell, the person who makes the last possible move is declared the winner.

---

## About this Repository

The game is implemented in Python and utilizes [Dash](https://dash.plotly.com/) and [Cytoscape](https://cytoscape.org/). 

### Prerequisites

- [Python 3](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installing/)

### Install the Dependencies

With pip installed, in the root of the repository, run `pip install -r requirements.txt`. This will install all of the dependencies including Dash, Dash Core Components, and Dash Cytoscape.

### Run the App

In the root of the repository, run `py src/app.py`. A local server will start on port 3000. Open the app in any _modern_ browser.

### Game Boards

Multiple boards/graphs are implemented to be played. Each board has a corresponding initialization file. These files are contained in `/src/boards/`. 

Each board initialization file define a board name, a list of Nodes, a list Cells using those Nodes, and a Graph using that list of cells. In a addition, a list of Cytoscape nodes and a Cytoscape stylesheet are defined.

`getGraph`, `getBoardName`, `getCytoscapeNodes`, and `getCytoscapeStylesheet` getter methods are defined to by used by the app's main code.

The `cytoscapeNodes` list is agreed to be a map of the following "shape".

```
{
    'data': {
        'id': <NODE_ID>
    },
    'position': {
        'x': <X_POSITION>,
        'y': <Y_POSITION>
    }
}
```

Notice that the id of any Cytoscape node corresponds to the id of one of our internal Nodes. **When defining Cells and Cytoscape node positions, it is important that the Cytoscape nodes are positioned such that the Cells can be accurately drawn by Cytoscape.** No errors will occur, but a discrepency between the internally defined Cells and Cytoscape node positions is likely to result in unexpected or unwanted behavior.

To access a newly added board from the main menu, it must also be imported and included in the `boardList` in `AppControl.py`. Then, if properly defined, the board will be accessible through the maim menu and playable.

---
