class Graph:
    def __init__(self, cells: list=None):
        self.cells = cells if cells != None else []
        self.nodes = []
        self.undirectedEdges = []
        self.directedEdges = []

        for c in cells:
            for e in c.getEdges():
                currentEdge = set([e[0].id, e[1].id])
                currentEdges = [ set([e[0].id, e[1].id]) for e in self.undirectedEdges ]
                if currentEdge not in currentEdges:
                    self.undirectedEdges.append(e)

            for n in c.getNodes():
                if n not in self.nodes:
                    self.nodes.append(n)

    def addDirectedEdge(self, edge: tuple):
        if not self.isEdgeMarked(edge):
            self.directedEdges.append(edge)
        else:
            raise Exception('Tried to mark an edge that is already marked in graph')

        for c in self.cells:
            if [edge[0], edge[1]] in c.getEdges() or [edge[1], edge[0]] in c.getEdges():
                c.addMarkedEdge(edge)
        return

    def isEdgeMarked(self, edge: tuple) -> bool:
        return (edge[0], edge[1]) in self.directedEdges or (edge[1], edge[0]) in self.directedEdges

    def isUnmarkedEdgeInGraph(self, edge) -> bool:
        return [edge[0], edge[1]] in self.undirectedEdges or [edge[1], edge[0]] in self.undirectedEdges

    def doesContainCycle(self):
        for c in self.cells:
            if c.doesContainCycle():
                return True
        return False

    def printGraphData(self):
        for n in self.nodes:
            print("Node:", n.id)
        for e in self.undirectedEdges:
            print("Undirected Edge:", e[0].id, e[1].id)

    def getCytoscapeGraphEdges(self):
        edges = []
        for e in self.directedEdges:
            edges.append({
                'data': {
                    'type': 'directed',
                    'source': int(e[0].id),
                    'target': int(e[1].id)
                }
            })

        for e in self.undirectedEdges:
            if not self.isEdgeMarked(e):
                edges.append({ 'data': { 'type': 'undirected', 'source': int(e[0].id), 'target': int(e[1].id) } })
        
        return edges

    def removeAllMarkedEdges(self):
        self.directedEdges = []
        for c in self.cells:
            c.removeAllMarkedEdges()
        return
