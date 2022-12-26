from TdP_collections.graphs.bfs import *
from TdP_collections.graphs.graph import Graph

# This method perfomrs a BFS that is interrubted when a path to destination is founded.
# When the edges are labeled with a capacity that is 0, the edge cannot be traversed.
def _bfs( g, source, destination, discovered):
    """Perform a BFS on the graph g, return true if there is a path from source to destination, false otherwise."""
    founded = False
    level = [source]                        
    while ( (len(level) > 0) and ( not founded) ):
        next_level = []                 
        for u in level:
            for e in g.incident_edges(u):  
                if (e.element() == 1):
                    v = e.opposite(u)
                    if v is destination:
                        founded = True
                    if v not in discovered:     
                        discovered[v] = e          
                        next_level.append(v)       
        level = next_level   
    return founded

class ExtendedGraph(Graph):

    def __init__(self, directed = False):
        super().__init__(directed)

    class Edge(Graph.Edge):
        def __init__(self, u, v, x):
            super().__init__(u, v, x)

        def setElement(self, x):
            self._element = x

class NetworkFlow():

    __slots__= '_dominatedSet','_dominatorSet','_graph','_source','_sink'


    
    def __init__(self):
        """
            Create a bipartite graph with two sets of vertices: the dominator set and the dominated set        
        """
        self._graph = ExtendedGraph(True)
        self._source = self._graph.insert_vertex('source')
        self._sink = self._graph.insert_vertex('sink')
        self._dominatedSet = {}
        self._dominatorSet = {}

    def insertDevices(self, deviceList,data,X):
        for x in deviceList:
            dominantVertex = self._graph.insert_vertex(x)
            self._graph.insert_edge(self._source,dominantVertex,1)
            dominatedVertex = self._graph.insert_vertex(x)
            self._graph.insert_edge(dominatedVertex,self._sink,1)
            self._dominatorSet[x] = dominantVertex
            self._dominatedSet[x] = dominatedVertex
        for dominator in self._dominatorSet:
            for dominated in self._dominatedSet:
                if dominator != dominated:
                    if self._isBetter(dominator,dominated,data,X):
                        self._graph.insert_edge(self._dominatorSet[dominator],self._dominatedSet[dominated],1)
        

    def fordFulkerson(self):
        """
            Compute the maximum flow in the network flow built from the vertex set, in this specific case at the end of the algorithm
            the graph is changed to be the last residual graph built by the algorithm
        """
        flow = 0
        path = {}
        path[self._source] = None
        while _bfs(self._graph,self._source,self._sink,path):
            bottleNeck = 1 # all the edges have capacity 1 by construction this menas that the bottleNeck is always 1
            flow+=bottleNeck
            edge = path[self._sink]
            while edge != None:
                v1,v2 = edge.endpoints()
                edge.setElement(edge.element()-bottleNeck)
                backwardEdge = self._graph.get_edge(v2,v1)
                if  backwardEdge == None:
                    backwardEdge = self._graph.insert_edge(v2,v1,0) #backward edge
                backwardEdge.setElement(backwardEdge.element()+bottleNeck)
                edge = path.get(v1)
            path = {}
            path[self._source] = None
        return flow

    def makePartition(self):
        """
            Return a group of partition: in each partition there are a ranked group of devices built as follows:
            - the first device is the best one and dominates all the other devices
            - the second device is the second best one and dominates all the other devices except the first one
            - so on...
        """
        partition = []
        for device in self._dominatorSet.values():
            if self._isHead(device):
                subpartition = []
                partition.append(self._makePartitionFromHead(device,subpartition))
        return partition

    #------------------------- Private methods -------------------------
    def _isBetter(self, dominator, dominated, data, X):
        """
            Check if the dominator device is better than the dominated one 
            by checking all the device's caratteristic
        """
        for elem in range(X-2):
            if data[dominator][elem]<=data[dominated][elem]:
                return False
        return True
    
    def _isHead(self,device):
        """
            Check if the device is a head of a partition this means that 
            the device is not dominated by any other device, if this is true
            even one edge to the sink is enough to prove it
        """
        return self._graph.get_edge(self._dominatedSet[device.element()],self._sink).element() != 0

    def _makePartitionFromHead(self,head,partition):
        """
            Build a partition starting from a head device
        """
        partition.append(head.element())
        for outgoingEdge in self._graph.incident_edges(head):
            if outgoingEdge.element() == 0:
                newElement = outgoingEdge.opposite(head).element()
                self._makePartitionFromHead(self._dominatorSet[newElement],partition)        
        return partition