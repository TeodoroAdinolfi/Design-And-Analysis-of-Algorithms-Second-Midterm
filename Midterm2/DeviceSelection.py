from NetworkFlow import NetworkFlow

class DeviceSelection:

    _slots_ = "_networkFlow","_N","_X","_maxFlow","_partition","_generator"


    #The object is created as follows:
    #    - a bipartite graph is created with two sets of vertices: the dominator set and the dominated set
    #    - the dominator set and the dominated set are the same and are the set of devices
    #    - the dominator set is connected to the source with capacity 1
    #    - the dominated set is connected to the sink with capacity 1
    #    - between a dominator and a dominated vertex there is an edge with capacity 1 only if all the caratteristic of the dominator device are striclty better than the dominated one
    #    - the maximum flow is calculated using the Ford-Fulkerson algorithm, on a network flow created as described above this algorithm can be used fot obtaining the maximum cardinality matching
    #    - the maximum cardinality matching is used to create the partitions of the devices by remembering that the non-interliving propertyes must always be vaild,
    #      this means that if there is a matching between a device A and a device B and if there is also a matching between the device B and a device C we can assume that A dominates C
    #    - in the end after the creation of the partition, a list of generaor is created, each generator iterate over one of the partitions
    def __init__(self,N, X, data):
        """
            Create a device selection object
            N: a tuple containing the devices names
            X: the number of X-term frases on witch the devices are tested (from 3 to X)
            data: a dictionary with the values of the X-term frases correctly interpreted by the device
        """
        self._networkFlow = NetworkFlow()
        self._N = N
        self._X = X
        self._networkFlow.insertDevices(N,data,X)
        self._maxFlow = self._networkFlow.fordFulkerson()
        self._partition = self._networkFlow.makePartition()
        self._generator = [None] * self.countDevices()
        for i in range(self.countDevices()):
            self._generator[i] = self._makeGenerator(i)

    # The max flow can be interpreted as the number of devices that are dominated by a another device
    # If we want to know the number of devices that are not dominated by any other device we can subtract the max flow from the number of devices
    # in this way we now how many classes of devices we have because each class must have exactly one device that is not dominated by any other device
    # Complexity: O(1)
    def countDevices(self):
        """
            Return the number of sub-partition of the set of devices
        """
        return len(self._N) - self._maxFlow

    # Complexity: O(1)
    def nextDevice(self,i):
        """
            Return the next device in the partition "i" or none if the iteration is ended
            throws an exception if the "i" partition doesn't exist
        """
        if (i >= self.countDevices() or i<0):
            raise("You can access into the range [0-",self.countDevices()-1,"]")
        try:
            #Call the next method on the correct generator and return the result
            return next(self._generator[i])
        except StopIteration:
            #if  the iteration is ended I create a new generator so taht the next time I call nextDevice(i) I can iterate again
            self._generator[i] = self._makeGenerator(i)
            return None
    
    #------------------------- Private methods -------------------------
    
    # Complexity: O(1)
    def _makeGenerator(self,count):
        """
            Return a generator that iterate over the partition "count"
        """
        yield from self._partition[count]
        
            



        
        
