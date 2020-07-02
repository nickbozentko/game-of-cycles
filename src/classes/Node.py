class Node:
    _nextId = 0

    @staticmethod
    def __getId__():
        ret = Node._nextId
        Node._nextId += 1
        return ret

    def __init__(self):
        self.id = Node.__getId__()
