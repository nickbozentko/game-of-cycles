class Node:
    _nextId = 0

    @staticmethod
    def __getId__():
        ret = Node._nextId
        Node._nextId += 1
        return ret

    def __init__(self):
        self.id = Node.__getId__()
        self.outboundNodes = set()
        self.inboundNodes = set()
        self.adjacentNodes = set()

    def addAdjacentNode(self, node: 'Node'):
        self.adjacentNodes.add(node)
        return

    def addOutboundNode(self, node: 'Node'):
        self.outboundNodes.add(node)
        return

    def addInboundNode(self, node: 'Node'):
        self.inboundNodes.add(node)
        return

    def printNodeData(self):
        print('Node', self.id, 'Adjacent IDs:', list(map(lambda x: x.id, self.adjacentNodes)))
        print(self.id, '->', list(map(lambda x: x.id, self.outboundNodes)))
        print(self.id, '<-', list(map(lambda x: x.id, self.inboundNodes)))
        return

    def removeAllDirectedNodes(self):
        self.inboundNodes = set()
        self.outboundNodes = set()
        return

    def wouldOutboundNodeCreateSource(self, node: 'Node') -> bool:
        potentialOutboundNodes = self.outboundNodes.copy()
        potentialOutboundNodes.add(node)
        return len(self.adjacentNodes.difference(potentialOutboundNodes)) == 0

    def wouldInboundNodeCreateSink(self, node: 'Node') -> bool:
        potentialInboundNodes = self.inboundNodes.copy()
        potentialInboundNodes.add(node)
        return len(self.adjacentNodes.difference(potentialInboundNodes)) == 0
