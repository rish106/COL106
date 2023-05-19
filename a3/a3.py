def mergeSortedLists(L1, L2):
    L3 = []
    i, j = 0, 0
    while (i < len(L1) and j < len(L2)):
        if (L1[i] <= L2[j]):
            L3.append(L1[i])
            i += 1
        else:
            L3.append(L2[j])
            j += 1
    while (i < len(L1)):
        L3.append(L1[i])
        i += 1
    while (j < len(L2)):
        L3.append(L2[j])
        j += 1
    return L3

class Node:

    def __init__(self, key1, key2, parent):
        self.key1 = key1
        self.key2 = key2
        self.parent = parent
        self.left = None
        self.right = None
        self.ySortedList = None

class BinarySearchTree:

    def __init__(self):
        self.root = None

    def findNodeMaxForN(self, root, N):
        # find node with max key less than N
        if (root.key1 > N and root.left is None):
            return None
        elif (root.key1 <= N and root.right is None):
            return root
        elif (root.key1 > N and root.left != None):
            return self.findNodeMaxForN(root.left, N)
        elif (root.key1 <= N and root.right != None):
            right = self.findNodeMaxForN(root.right, N)
            if (right is None):
                return root
            else:
                return right

    def findNodeMinForN(self, root, N):
        # find node with minimum key greater than N
        if (root.key1 < N and root.right is None):
            return None
        elif (root.key1 >= N and root.left is None):
            return root
        elif (root.key1 < N and root.right != None):
            return self.findNodeMinForN(root.right, N)
        elif (root.key1 >= N and root.left != None):
            left = self.findNodeMinForN(root.left, N)
            if (left is None):
                return root
            else:
                return left

    def lowestCommonAncestor(self, root, node1, node2):
        rootValue = (root.key1, root.key2)
        node1Value = (node1.key1, node1.key2)
        node2Value = (node2.key1, node2.key2)
        if (rootValue >= node1Value and rootValue <= node2Value):
            return root
        elif (rootValue > node1Value and rootValue > node2Value):
            return self.lowestCommonAncestor(root.left, node1, node2)
        elif (rootValue < node1Value and rootValue < node2Value):
            return self.lowestCommonAncestor(root.right, node1, node2)

    def buildBalancedTree(self, sortedList, i, j, parent=None):
        if (i > j):
            return None
        mid = (i+j)//2
        root = Node(sortedList[mid][0], sortedList[mid][1], parent)
        if (parent is None):
            self.root = root
        root.left = self.buildBalancedTree(sortedList, i, mid-1, root)
        root.right = self.buildBalancedTree(sortedList, mid+1, j, root)
        return root


    def buildYTrees(self, root):
        if (root is None):
            return
        if (root.left is None and root.right is None):
            root.ySortedList = [(root.key2, root.key1)]
        else:
            if (root.left is None):
                L1 = []
            else:
                self.buildYTrees(root.left)
                L1 = root.left.ySortedList
            if (root.right is None):
                L2 = []
            else:
                self.buildYTrees(root.right)
                L2 = root.right.ySortedList
            tmp = mergeSortedLists(L1, L2)
            ySortedList = mergeSortedLists([(root.key2, root.key1)], tmp)
            root.ySortedList = ySortedList


def findMaxForN(L, N):
    n = len(L)
    i, j = 0, n-1
    if (L[i][0] > N):
        return None
    if (L[j][0] <= N):
        return j
    while (i <= j):
        mid = (i+j)//2
        if (mid < n-1 and L[mid][0] <= N and L[mid+1][0] > N):
            return mid
        elif L[mid][0] > N:
            j = mid
        elif L[mid][0] <= N:
            i = mid+1

def findMinForN(L, N):
    n = len(L)
    i, j = 0, n-1
    if (L[j][0] < N):
        return None
    if (L[i][0] >= N):
        return i
    while (i <= j):
        mid = (i+j)//2
        if (mid > 0 and L[mid][0] >= N and L[mid-1][0] < N):
            return mid
        elif L[mid][0] < N:
            i = mid + 1
        elif L[mid][0] >= N:
            j = mid

def nodeListAndSubTreeList(a, b, c):
    nodeList = []
    subTreeList = []
    notLCA = a
    nodeList.append(a)
    if (a != c and a.right != None):
        subTreeList.append(a.right)
    while (notLCA != c and notLCA.parent != c):
        if (notLCA == notLCA.parent.left):
            nodeList.append(notLCA.parent)
            if (notLCA.parent.right != None):
                subTreeList.append(notLCA.parent.right)
        notLCA = notLCA.parent
    if (c != a and c != b):
        nodeList.append(c)
    notLCA = b
    while (notLCA != c and notLCA.parent != c):
        if (notLCA == notLCA.parent.right):
            nodeList.append(notLCA.parent)
            if (notLCA.parent.left != None):
                subTreeList.append(notLCA.parent.left)
        notLCA = notLCA.parent
    if (a != b):
        nodeList.append(b)
    if (b != c and b.left != None):
        subTreeList.append(b.left)
    return (nodeList, subTreeList)

class PointDatabase:

    def __init__(self, pointlist):
        self.treeX = BinarySearchTree()
        pointlist.sort()
        self.treeX.buildBalancedTree(pointlist, 0, len(pointlist)-1)
        self.treeX.buildYTrees(self.treeX.root)

    def searchNearby(self, q, d):
        (qx, qy) = (q[0], q[1])
        if (self.treeX.root == None):
            return []
        a = self.treeX.findNodeMinForN(self.treeX.root, qx - d)
        b = self.treeX.findNodeMaxForN(self.treeX.root, qx + d)
        if ((a is None) or (b is None) or (a.key1 > b.key1)):
            return []
        c = self.treeX.lowestCommonAncestor(self.treeX.root, a, b)
        (nodeList, subTreeList) = nodeListAndSubTreeList(a, b, c)
        points = []
        for node in nodeList:
            if (node.key2 >= qy - d and node.key2 <= qy + d):
                points.append((node.key1, node.key2))
        for node in subTreeList:
            ySortedList = node.ySortedList
            aY = findMinForN(ySortedList, qy - d)
            bY = findMaxForN(ySortedList, qy + d)
            if (aY is None or bY is None):
                continue
            for i in range(aY, bY+1):
                points.append((ySortedList[i][1], ySortedList[i][0]))
        return points
