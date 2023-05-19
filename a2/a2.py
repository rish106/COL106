class minHeap():

    def __init__(self, n):
        self.Heap = []
        self.size = 0
        self.mapping = [None]*n

    def isEmpty(self):
        return self.size == 0

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
        if ((2*i + 1 < self.size) and (self.Heap[self.leftChild(i)] < self.Heap[i] or self.rightChild(i) < self.size and self.Heap[self.rightChild(i)] < self.Heap[i])):
            if (self.rightChild(i) == self.size or self.Heap[self.leftChild(i)] < self.Heap[self.rightChild(i)]):
                self.swap(i, self.leftChild(i))
                self.heapDown(self.leftChild(i))
            else:
                self.swap(i, self.rightChild(i))
                self.heapDown(self.rightChild(i))

    def heapUp(self, i):
        if (self.size != 0 and i != 0 and self.Heap[i] < self.Heap[self.parent(i)]):
            self.swap(i, self.parent(i))
            self.heapUp(self.parent(i))

    def enqueue(self, e): # insert element in O(log(n)) time
        self.Heap.append(e)
        self.size += 1
        j = self.size - 1
        self.mapping[e[1]] = j
        while (j > 0 and self.Heap[j] < self.Heap[self.parent(j)]):
            self.swap(j, self.parent(j))
            j = self.parent(j)

    def remove(self): # remove root node in O(log(n)) time
        self.swap(0, self.size - 1)
        root = self.Heap.pop()
        self.mapping[root[1]] = None
        self.size -= 1
        self.heapDown(0)
        return root

    def buildMinHeap(self, L):
        n = len(L)
        for i in range(n):
            self.Heap.append(L[i])
            self.mapping[L[i][1]] = i
        self.size = n
        for i in range(n//2 - 1, -1, -1):
            self.heapDown(i)

    def getMapping(self, u):
        return self.mapping[u]

    def update(self, i, e):
        self.Heap[i] = e
        self.heapUp(i)
        self.heapDown(i)

    def peek(self):
        if not self.isEmpty():
            return self.Heap[self.size - 1]

    def __str__(self):
        return str(self.Heap[0:self.size])


def listCollisions(M, x, v, m, T):

    n = len(M)
    L = []
    for i in range(n):
        L.append([M[i], x[i], v[i], 0.0])
    L2 = []

    def afterCollision(L1):
        (t, i, x) = L1
        (M1, x1, v1, t1) = L[i]
        (M2, x2, v2, t2) = L[i+1]
        L[i][2] = ((M1 - M2)*v1 + 2*M2*v2)/(M1 + M2)
        L[i+1][2] = ((M2 - M1)*v2 + 2*M1*v1)/(M1 + M2)
        L[i][1], L[i][3] = x, t
        L[i+1][1], L[i+1][3] = x, t

    def collision(i):
        (M1, x1, v1, t1) = L[i]
        (M2, x2, v2, t2) = L[i+1]
        x = (x1*v2 - x2*v1 + v1*v2*(t2 - t1))/(v2 - v1)
        t = t1 + (x1 - x2 + v2*(t2 - t1))/(v2 - v1)
        return (t, i, x)


    for i in range(n-1):
        if (L[i][2] > L[i+1][2] and L[i][1] != L[i+1][1]):
            L2.append(collision(i))
    possibleCollisions = minHeap(n)
    possibleCollisions.buildMinHeap(L2)
    collisions = []
    while (len(collisions) < m and not possibleCollisions.isEmpty()):
        (t, i, x) = possibleCollisions.remove()
        if (t > T):
            break
        afterCollision((t, i, x))
        collisions.append((round(t, 4), i, round(x, 4)))
        if (i > 0 and L[i-1][2] > L[i][2] and possibleCollisions.getMapping(i-1) != None):
            possibleCollisions.update(possibleCollisions.getMapping(i-1), collision(i-1))
        if (i < n-2 and L[i+1][2] > L[i+2][2]) and possibleCollisions.getMapping(i+1) != None:
            possibleCollisions.update(possibleCollisions.getMapping(i+1), collision(i+1))
        if (i > 0 and L[i-1][2] > L[i][2]) and possibleCollisions.getMapping(i-1) == None:
            possibleCollisions.enqueue(collision(i-1))
        if (i < n-2 and L[i+1][2] > L[i+2][2]) and possibleCollisions.getMapping(i+1) == None:
            possibleCollisions.enqueue(collision(i+1))
    return collisions

print(listCollisions([1.0, 5.0], [1.0, 2.0], [3.0, 5.0], 100, 100.0))
print(listCollisions([1.0, 1.0, 1.0, 1.0], [-2.0, -1.0, 1.0, 2.0], [0.0, -1.0, 1.0, 0.0], 5, 5.0))
print(listCollisions([10000.0, 1.0, 100.0], [0.0, 1.0, 2.0], [0.0, 0.0, -1.0], 6, 10.0))
print(listCollisions([10000.0, 1.0, 100.0], [0.0, 1.0, 2.0], [0.0, 0.0, -1.0], 100, 1.5))
