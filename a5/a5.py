class GraphNode:

    def __init__(self, vertex):
        self.vertex = vertex
        self.adjAndCapacityList = []

    def addAdjVertex(self, c, e):
        self.adjAndCapacityList.append((c, e))


class MaxHeap:

    def __init__(self, n):
        self.Heap = []
        self.size = 0
        self.mapping = [None]*n

    def isEmpty(self):
        return self.size == 0

    def getMapping(self, u):
        return self.mapping[u]

    def parent(self, i):
        return (i-1)//2

    def leftChild(self, i):
        return 2*i + 1

    def rightChild(self, i):
        return 2*i + 2

    def swap(self, i, j):
        self.mapping[self.Heap[i][1]], self.mapping[self.Heap[j][1]] = self.mapping[self.Heap[j][1]], self.mapping[self.Heap[i][1]]
        self.Heap[i], self.Heap[j] = self.Heap[j], self.Heap[i]

    def heapDown(self, i):
        if ((2*i + 1 < self.size) and (self.Heap[self.leftChild(i)] > self.Heap[i] or self.rightChild(i) < self.size and self.Heap[self.rightChild(i)] > self.Heap[i])):
            if (self.rightChild(i) == self.size or self.Heap[self.leftChild(i)] > self.Heap[self.rightChild(i)]):
                self.swap(i, self.leftChild(i))
                self.heapDown(self.leftChild(i))
            else:
                self.swap(i, self.rightChild(i))
                self.heapDown(self.rightChild(i))

    def heapUp(self, i):
        if (i > 0 and self.Heap[i] > self.Heap[self.parent(i)]):
            self.swap(i, self.parent(i))
            self.heapUp(self.parent(i))

    def enqueue(self, e): # insert element in O(log(n)) time
        self.Heap.append(e)
        self.size += 1
        j = self.size - 1
        self.mapping[e[1]] = j
        while (j > 0 and self.Heap[j] > self.Heap[self.parent(j)]):
            self.swap(j, self.parent(j))
            j = self.parent(j)

    def remove(self): # remove root node in O(log(n)) time
        root = self.Heap[0]
        self.mapping[root[1]] = None
        self.size -= 1
        self.Heap[0] = self.Heap[self.size]
        self.mapping[self.Heap[0][1]] = 0
        self.Heap.pop()
        self.heapDown(0)
        return root
    
    def update(self, i, e):
        self.Heap[i] = e
        self.heapUp(i)


def findMaxCapacity(n, links, s, t):
    graphNodes = []
    for i in range(n):
        graphNodes.append(GraphNode(i))
    for link in links:
        (u, v, c) = link
        graphNodes[u].addAdjVertex(c, v)
        graphNodes[v].addAdjVertex(c, u)

    # Modified Dijkstra's algorithm
    capacity = [0]*n
    prev = [None]*n
    maxHeap = MaxHeap(n)
    maxHeap.enqueue((0, s))
    while (not maxHeap.isEmpty()):
        (cap, u) = maxHeap.remove()
        if (u == t):
            break
        for link in graphNodes[u].adjAndCapacityList:
            (c, v) = link
            if (u != s):
                c = min(cap, c)
            if (v != s and c > capacity[v]):
                if (maxHeap.getMapping(v) == None):
                    maxHeap.enqueue((c, v))
                else:
                    maxHeap.update(maxHeap.getMapping(v), (c, v))
                capacity[v] = c
                prev[v] = u
            else:
                continue

    route = []
    route.append(t)
    vert = t
    while (vert != s):
        route.append(prev[vert])
        vert = prev[vert]
    route.reverse()
    maxCapacity = capacity[t]
    return (maxCapacity, route)
