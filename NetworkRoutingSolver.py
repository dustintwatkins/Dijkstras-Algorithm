#!/usr/bin/python3


from CS312Graph import *
import time

class arraypq:
    def __init__(self):
        self.data = []

    #Time: O(n)
    #Space: O(n)
    def pop(self):
        if len(self.data) == 0:                #shouldn't ever pop an empty list
            print("empty")

        min_key = float("inf")                 #set to highest val so everything is less than this
        min_val = None
        min_index = float("inf")               #set to highest val so everything is less than this
        indx = 0
        lst = None

        #Time: O(n)
        for pt in self.data:                   #iterate through array
            if pt[0] < min_key:
                min_key = pt[0]
                min_val = pt[1]
                min_index = indx
                lst = pt
            indx = indx + 1

        #Remove the index val from
        self.data = list(filter(lambda x:x != self.data[min_index], self.data))

        return lst

    #Time:O(1)
    #Space: O(n)
    def insert(self, key, val):
        self.data.append([key, val])          #add to array, unsorted

    #Time:O(1)
    #Space:O(n)
    def is_not_empty(self):
        if len(self.data) == 0:
            return False
        return True

#Time:O(1)
def get_else(lst, idx, alt):
    try:
        return lst[idx]
    except:
        return alt


class binHeap:
    def __init__(self):
        self.data = [[float("-inf")]]

    #Time:O(log(n))
    #Space:O(n)
    def balance(self, idx):
        parent = get_else(self.data, idx//2, [float("-inf")])                   #O(1)
        child_left = get_else(self.data, idx * 2, [float("inf")])               #O(1)
        child_right = get_else(self.data, (idx * 2) + 1, [float("inf")])        #O(1)
        item = get_else(self.data, idx, [float("inf")])                         #O(1)
        if item[0] < parent[0]:                     #swap parent and child node
            self.data[idx//2] = item
            self.data[idx] = parent
            return self.balance(idx//2)             #balance again              #Olog(n)
        if child_left[0] < item[0] and child_left[0] <= child_right[0]:
            self.data[idx] = child_left
            self.data[idx * 2] = item
            return self.balance(idx * 2)                                        #Olog(n)
        if child_right[0] < item[0] and child_right[0] < child_left[0]:
            self.data[idx] = child_right
            self.data[(idx * 2) + 1] = item
            return self.balance((idx * 2) + 1)                                  #Olog(n)

    #Time:Olog(n)
    #Space:O(n)
    def pop(self):
        res = self.data[1]                                                      #O(1)
        self.data[1] = self.data[len(self.data) - 1] #btm of heap becomes root  #O(1)
        del self.data[len(self.data) - 1:]           #remove from heap          #O(n)
        self.balance(1)                              #rebalance heap            #Olog(n)
        return res

    #Time:Olog(n)
    #Space:O(n)
    def insert(self, cost, item):
        self.data.append([cost, item])               #add to end of heap        #O(1)
        idx = len(self.data) - 1
        self.balance(idx)                            #balance inserted item     #Olog(n)

    #Time:O(1)
    #Space:O(n)
    def is_not_empty(self):
        if len(self.data) == 1:                      #index[0] is -infinity
            return False
        return True

#Time - binHeap: O(nlogn)
#Time - arraypq: O(n^2)
def dijkstra(queue, edge, src):
    results = {}                                              #create dictionary
    results[src] = [src, 0]                                   #start w/ the src node and set cost to 0
    queue.insert(0, src)                                      #add src node to front of queue
    while queue.is_not_empty():                                                 #O(1)
        u = queue.pop()                                                         #Olog(n) for binHeap /O(n) for arraypq
        u_edges = edge[u[1]]
        for e in u_edges:                 #iterate through the edges            #O(num of edges)
            v = e[0]
            original_dist = get_else(results, v, [None, float("inf")])[1]       #O(1)
            new_dist = get_else(results, u[1], [None, float("inf")])[1] + e[1]  #O(1)
            if original_dist > new_dist:                     #check distances between nodes and compare
                results[v] = [u[1], new_dist]
                queue.insert(new_dist, v)                                       #Olog(n) for binHeap /O(1) for arraypq
    return results;

class NetworkRoutingSolver:
    def __init__( self, display ):
        pass

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network


    def getShortestPath( self, destIndex ):
        self.dest = destIndex

        # TODO: RETURN THE SHORTEST PATH FOR destIndex

        path_edges = []
        total_length = 0

        node = self.network.nodes[self.source]
        curr_node = self.dest

        while curr_node != self.source:
            next_node = self.results[curr_node][0]
            curr_length = 0
            for e in self.edges[next_node]:
                if e[0] == curr_node:
                    curr_length = e[1]
                    break

            total_length += curr_length
            path_edges.append((self.network.nodes[curr_node].loc, self.network.nodes[next_node].loc,
                             '{:.0f}'.format(curr_length)))
            curr_node = next_node

        return {'cost':total_length, 'path':path_edges}


    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
        self.results = {}
        self.edges = {}

        graph = self.network
        nodes = graph.nodes

        #edges = {}
        #Time:O(n)
        for node in nodes:                                    #set nodes up for how they are used in DIJKSTRA
            lst = []
            for edge in node.neighbors:                       #max of 3 edges so actually O(3n) => O(n)
                lst.append([edge.dest.node_id, edge.length])
            self.edges[node.node_id] = lst

        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        t1 = time.time()

        queue = None
        if use_heap:
            queue = binHeap()
        else:
            queue = arraypq()

        self.results = dijkstra(queue, self.edges, srcIndex)

        t2 = time.time()

        return (t2-t1)
