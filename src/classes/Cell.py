class Cell:

    def __init__(self, nodes: list=None, markedEdges: list=None):
        self.nodes = nodes if nodes != None else []
        self.markedEdges = markedEdges if markedEdges != None else []

        for idx, n in enumerate(self.nodes):
            n.addAdjacentNode(self.nodes[idx-1])
            n.addAdjacentNode(self.nodes[(idx+1) % len(self.nodes)])

        return

    def getEdges(self) -> list:
        return [ [self.nodes[i], self.nodes[i+1]] for i in range(-1, len(self.nodes)-1) ]

    def getNodes(self) -> list:
        return self.nodes

    def printCellData(self):
        myEdges = self.getEdges()

        print('Undirected Edges')
        print('----------------')
        for n1, n2 in myEdges:
            print('(', n1.id, ',', n2.id, ')')
        print()

        print('Directed Edges')
        print('----------------')
        for n1, n2 in self.markedEdges:
            print(n1.id, '->', n2.id)
        return

    def addMarkedEdge(self, edge: tuple):
        if self.isUndirectedEdgeInCell(edge):
            if self.isEdgeMarked(edge):
                raise Exception('Tried to mark an edge that is already marked in cell')
            else:
                self.markedEdges.append(edge)
        else:
            raise Exception('Tried to add marked edge using nodes not in this cell')
        return

    def isEdgeMarked(self, edge: tuple) -> bool:
        return (edge[0], edge[1]) in self.markedEdges or (edge[1], edge[0]) in self.markedEdges

    def isUndirectedEdgeInCell(self, edge) -> bool:
        return\
        edge[0] in self.nodes\
        and edge[1] in self.nodes \
        and (\
            abs(self.nodes.index(edge[0]) - self.nodes.index(edge[1])) == 1\
            or (self.nodes.index(edge[0]) == 0 and self.nodes.index(edge[1]) == len(self.nodes) - 1)\
            or (self.nodes.index(edge[1]) == 0 and self.nodes.index(edge[0]) == len(self.nodes) - 1)\
        )

    def doesContainCycle(self) -> bool:
        return self.doesContainForwardCycle() or self.doesContainBackwardCycle()

    def doesContainForwardCycle(self) -> bool:
        for i in range(len(self.nodes)):
            if (self.nodes[i-1], self.nodes[i]) not in self.markedEdges:
                return False
        return True

    def doesContainBackwardCycle(self) -> bool:
        for i in range(len(self.nodes)):
            if (self.nodes[i], self.nodes[i-1]) not in self.markedEdges:
                return False
        return True

    def removeAllMarkedEdges(self):
        self.markedEdges = []
        return