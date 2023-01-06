from TdP_collections.graphs.bfs import *
from TdP_collections.graphs.graph import Graph

# This method perfomrs a BFS that is interrubted when a path to destination is founded.
# When the edges are labeled with a capacity that is 0, the edge cannot be traversed.
# Complexity: O( N + M ) with N the number of vertices and M the number of edges
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
# Adds a method to the Edge class that allows to set the label of the edge in this 
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

    # Complexity: O(N^2 * X)
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
        #Adding the edges between the dominators and the dominateds
        for dominator in self._dominatorSet:
            for dominated in self._dominatedSet:
                if dominator != dominated:
                    if self._isBetter(dominator,dominated,data,X):
                        self._graph.insert_edge(self._dominatorSet[dominator],self._dominatedSet[dominated],1)
        
    # Complexity: O(N*M) with N the number of devices and M the number edges
    def fordFulkerson(self):
        """
            Compute the maximum flow. In this case at the end of the algorithm
            the graph is changed to be the last residual graph built by the algorithm
        """
        flow = 0
        path = {}                                                          # path is a dictionary that maps each vertex to the edge that is traversed to reach it
        path[self._source] = None                                          # the source cannot be reached by any path for construction                         
        while _bfs(self._graph,self._source,self._sink,path):              # we are searching all the possible paths from the source to the sink
            bottleNeck = 1                                                 # all the edges have capacity 1 by construction this menas that the bottleNeck is always 1, the variable bottleNeck is used to make the code more general
            flow+=bottleNeck                                               # the total flow can be augmented by the bottleNeck
            edge = path[self._sink]                                        # edge is the edge that is traversed to reach the sink, we start analyzing the bath from the sink to the source
            while edge != None:                                            # Edge will be none only when we reach the source
                v1,v2 = edge.endpoints()                                   # v1 is the source of the edge and v2 is the destination of the edge
                edge.setElement(edge.element()-bottleNeck)                 # Reduce the remaining capacity of the forward edge by the bottleNeck (this means saturate the edge because the maximum capacity is 1)
                backwardEdge = self._graph.get_edge(v2,v1)                 # We must change (and augment) the backward edge into the residual graph (that as said in this case is the same as the original graph) 
                if  backwardEdge == None:                                  # If the backward edge does not exist, we create it because now we can send back the flow that is going from v1 to v2
                    backwardEdge = self._graph.insert_edge(v2,v1,0)        # Only for convenience the backward edge is added with a remaining capacity of 0 but it will be increased immediately
                backwardEdge.setElement(backwardEdge.element()+bottleNeck) # Increase the remaining capacity of the backward edge by the bottleNeck, this means thath we can send back more flow now
                edge = path.get(v1)                                        # go to the next edge in the path
            path = {}                                                      # reset the path because we are going to search a new path for the sink if it exists
            path[self._source] = None                                     
        return flow


    # Complexity: O( N + M ) where N is the number of vertex of the bipartyte graph and M the number of edges
    def makePartition(self):
        """
            Return a group of partition: in each partition there are a ranked group of devices built as follows:
            - the first device is the best one and dominates all the other devices
            - the second device is the second best one and dominates all the other devices except the first one
            - so on...
        """
        partition = []
        for device in self._dominatorSet.values():                  # We check all the dominator devices
            if self._isHead(device):                                # If the device is a head of a partition we build the partition starting from him (a device is a head if it is not dominated by any other device)     
                subpartition = []                                   # Checking if a device is a head is done by checking if the only edge to the sink of that device in the dominated set has a remaining capacity of 1 
                self._makePartitionFromHead(device,subpartition)    # (there isn't a matching with that device and so it must be a head)
                partition.append(subpartition)                      # We add the partition to the list of partitions and keep searching for other heads
        return partition



    # Complexity: O( N + M ) where N is the number of vertex of the bipartyte graph and M the number of edges
    # Note that we can be sure tath if the head dominates a device let's call it B this menas that all the devices dominated by B 
    # are dominated by the head for the transitivity of the dominance relation
    def _makePartitionFromHead(self,head,partition):
        """
            Build a partition starting from a head device
        """
        partition.append(head.element())                                                # Add the head to the partition
        for outgoingEdge in self._graph.incident_edges(head):                           # Start searching for the edges choosen by the ford fulkerson algorithm (the edges that have a remaining capacity of 0)
            if outgoingEdge.element() == 0:
                newElement = outgoingEdge.opposite(head).element()                      # We get the device that is connected to the head by that edge and we repeat the process by searching the dominated
                self._makePartitionFromHead(self._dominatorSet[newElement],partition)   # device in the dominator set till the end of the partition (a device that is only dominated but not dominates any other device))
        
    
    
    #------------------------- Private methods -------------------------
    
    # Complexity: O(X) whith X the number X-terms tested
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

    


    
