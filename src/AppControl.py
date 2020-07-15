import dash

# Import our boards
import boards.Triforce as Triforce
import boards.TripleTriangleWithDeathDiamond as TripleTriangleWithDeathDiamond
import boards.Square as Square

page = 'HOME'

# Initialize boardList and boardMap
boardList = [TripleTriangleWithDeathDiamond, Triforce, Square]
boardMap = {}
for board in boardList:
    boardMap[board.getBoardName()] = board
chosenBoardName = ''

# State Control
CHOSEN_GRAPH = boardMap.get(chosenBoardName, Triforce)
graph = CHOSEN_GRAPH.getGraph()


app = dash.Dash()
app.config['suppress_callback_exceptions'] = True