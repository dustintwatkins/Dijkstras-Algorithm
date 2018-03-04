#!/usr/bin/python3


from CS312Graph import *
import time

class arraypq:
    def __init__(self):
        self.data = []

    def pop(self):
        if len(self.data) == 0:
            print("empty")

        min_key = float("inf")
        min_val = None
        min_index = float("inf")
        indx = 0
        lst = None

        #Time: O(n) iterate through data pts
        for pt in self.data:
            if pt[0] < min_key:
                min_key = pt[0]
                min_val = pt[1]
                min_index = indx
                lst = pt
            indx = indx + 1

        #Remove the index val from
        self.data = list(filter(lambda x:x != self.data[min_index], self.data))

        return lst

    def insert(self, key, val):
        self.data.append([key, val])

    def is_not_empty(self):
        if len(self.data) == 0:
            return False
        return True

def get_else(lst, idx, alt):
    try:
        return lst[idx]
    except:
        return alt

class binHeap:
    def __init__(self):
        self.data = [[float("-inf")]]

    def balance(self, idx):
        parent = get_else(self.data, idx//2, [float("-inf")])
        child_left = get_else(self.data, idx * 2, [float("inf")])
        child_right = get_else(self.data, (idx * 2) + 1, [float("inf")])
        item = get_else(self.data, idx, [float("inf")])
        if item[0] < parent[0]:
            self.data[idx//2] = item
            self.data[idx] = parent
            return self.balance(idx//2)
        if child_left[0] < item[0] and child_left[0] <= child_right[0]:
            self.data[idx] = child_left
            self.data[idx * 2] = item
            return self.balance(idx * 2)
        if child_right[0] < item[0] and child_right[0] < child_left[0]:
            self.data[idx] = child_right
            self.data[(idx * 2) + 1] = item
            return self.balance((idx * 2) + 1)

    def pop(self):
        res = self.data[1]
        self.data[1] = self.data[len(self.data) - 1]
        del self.data[len(self.data) - 1:]
        self.balance(1)
        return res

    def insert(self, cost, item):
        self.data.append([cost, item])
        idx = len(self.data) - 1
        self.balance(idx)

    def is_not_empty(self):
        if len(self.data) == 1:             #index[0] is None
            return False
        return True


def dijkstra(queue, edge, src):
    results = {}                             #create dictionary
    results[src] = [src, 0]
    queue.insert(0, src)
    while queue.is_not_empty():
        u = queue.pop()
        u_edges = edge[u[1]]
        for e in u_edges:
            v = e[0]
            original_dist = get_else(results, v, [None, float("inf")])[1]
            new_dist = get_else(results, u[1], [None, float("inf")])[1] + e[1]
            if original_dist > new_dist:
                results[v] = [u[1], new_dist]
                queue.insert(new_dist, v)
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
        #       INSTEAD OF THE DUMMY SET OF EDGES BELOW
        #       IT'S JUST AN EXAMPLE OF THE FORMAT YOU'LL
        #       NEED TO USE

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
        for node in nodes:
            lst = []
            for edge in node.neighbors:
                lst.append([edge.dest.node_id, edge.length])
            self.edges[node.node_id] = lst

        t1 = time.time()
        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index)

        queue = None
        if use_heap:
            queue = binHeap()
        else:
            queue = arraypq()

        self.results = dijkstra(queue, edges, srcIndex)

        t2 = time.time()

        return (t2-t1)
