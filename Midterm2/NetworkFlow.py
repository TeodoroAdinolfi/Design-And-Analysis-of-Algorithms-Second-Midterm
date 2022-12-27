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

# This class is used for the costruction of the graph representing the network flow
# Adds a method to the Edge class that allows to set the element of the edge in this 
# way we can change the capacity of the edge
class ExtendedGraph(Graph):

    def __init__(self, directed = False):
        super().__init__(directed)

    class Edge(Graph.Edge):
        def __init__(self, u, v, x):
            super().__init__(u, v, x)

        def setElement(self, x):
            self._element = x

# This class is used to represent the given problem as a network flow 
# is a custom class whose behavior is thinked only for the specific given problem
class NetworkFlow():

    __slots__= '_dominatedSet','_dominatorSet','_graph','_source','_sink'

    def __init__(self):
        """
            Create a networkFlow based on a bipartite graph with two sets of vertices: the dominator set and the dominated set        
        """
        self._graph = ExtendedGraph(True)
        self._source = self._graph.insert_vertex('source')
        self._sink = self._graph.insert_vertex('sink')
        self._dominatedSet = {}
        self._dominatorSet = {}

    # Complexity: O(n^2 X)
    def insertDevices(self, deviceList,data,X):
        """
            Adds the devices to the network flow
            this is made by creating a bipartite graph with two set of vertex dominator and dominated
            each device is added twice, one in the dominator set and one in the dominated set
            a dominator device is connected to the source with a capacity of 1
            a dominated device is connected to the sink with a capacity of 1
            if a dominator device is better than a dominated device, a connection is made between the two devices with a capacity of 1
        """
        for x in deviceList:
            #Adding the dominator and the edge to the source
            dominantVertex = self._graph.insert_vertex(x)
            self._graph.insert_edge(self._source,dominantVertex,1)
            #Adding the dominated and the edge to the sink
            dominatedVertex = self._graph.insert_vertex(x)
            self._graph.insert_edge(dominatedVertex,self._sink,1)
            #Adding the devices to the sets
            self._dominatorSet[x] = dominantVertex
            self._dominatedSet[x] = dominatedVertex
        #Adding the edges between the dominator and the dominated
        for dominator in self._dominatorSet:
            for dominated in self._dominatedSet:
                if dominator != dominated:
                    if self._isBetter(dominator,dominated,data,X):
                        self._graph.insert_edge(self._dominatorSet[dominator],self._dominatedSet[dominated],1)
        
    # Complexity: O(n*m)
    def fordFulkerson(self):
        """
            Compute the maximum flow. In this case at the end of the algorithm
            the graph is changed to be the last residual graph built by the algorithm
        """
        flow = 0
        path = {}
        path[self._source] = None
        while _bfs(self._graph,self._source,self._sink,path):
            bottleNeck = 1 # all the edges have capacity 1 by construction this menas that the bottleNeck is always 1, the variable bottleNeck is used to make the code more general
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
        
    # Complexity: O(?)
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
                self._makePartitionFromHead(device,subpartition)
                partition.append(subpartition)
        return partition

    #------------------------- Private methods -------------------------
    # Complexity: O(X)
    def _isBetter(self, dominator, dominated, data, X):
        """
            Check if the dominator device is better than the dominated one 
            by checking all the device's caratteristic
        """
        for elem in range(X-2):
            if data[dominator][elem]<=data[dominated][elem]:
                return False
        return True

    # Complexity: O(1)
    def _isHead(self,device):
        """
            Check if the device is a head of a partition this means that 
            the device is not dominated by any other device, if this is true
            the only edge to the sink must have a capacity of 1 (and so different from 0)
        """
        return self._graph.get_edge(self._dominatedSet[device.element()],self._sink).element() != 0

    # Complexity: ?
    def _makePartitionFromHead(self,head,partition):
        """
            Build a partition starting from a head device
        """
        partition.append(head.element())
        for outgoingEdge in self._graph.incident_edges(head):
            if outgoingEdge.element() == 0:
                newElement = outgoingEdge.opposite(head).element()
                self._makePartitionFromHead(self._dominatorSet[newElement],partition)        