class Empty(Exception):
    pass


class Stack:

    def __init__(self):
        self._data = []
        self.size = 0

    def __len__(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def push(self, e):
        if self.is_empty():
            self._data += [0]
        elif (self.size == len(self._data)): # all allocated memory has been used
            self._data += (self.size)*[0]
        self._data[self.size] = e
        self.size += 1

    def top(self):
        if self.is_empty():
            raise Empty("Stack is empty")
        return self._data[self.size - 1]

    def pop(self):
        if self.is_empty():
            raise Empty("Stack is empty")
        top_element = self.top()
        self._data[self.size - 1] = 0
        self.size -= 1
        return top_element

    def clear(self):
        self._data = []
        self.size = 0

    def __str__(self):
        return '<' + ', '.join(str(self._data[i]) for i in range(0, self.size)) + '>'


def findMultiplier(string):
    n = len(string)
    if (string[0] == '+' or string[0] == '-'):
        multiplier = 1
    else:
        i = 0
        multiplier = ""
        while (i < n and string[i] != '('):
            multiplier += string[i]
            i += 1
        multiplier = int(multiplier)
    return multiplier


def evaluate(string):
    n = len(string)
    v = [0, 0, 0, 0]
    multiplier = findMultiplier(string)
    i, j = 0, n-1
    if (string[-1] == '('):
        return [0, 0, 0, 0]
    elif ((string[0] != '+' and string[0] != '-') or string[-1] == ')'):
        while (i < n and (not (string[i] == '+' or string[i] == '-'))):
            i += 1
        while (j >= 0 and string[j] == ')'):
            j -= 1
    for k in range(i, j+1, 2):
        v[3] += 1
        if (string[k] == '+'):
            v[ord(string[k+1])-88] += 1;
        else:
            v[ord(string[k+1])-88] -= 1;
    v = [v[k] * multiplier for k in range(4)]
    return v


def countBrackets(string):
    n = len(string)
    brackets = 0
    for i in range(n):
        if (string[i] == '('):
            brackets += 1
        elif (string[i] == ')'):
            brackets -= 1
    return brackets


def findPositionandDistance(string):

    L = [0, 0, 0, 0]
    s = Stack() # will store the substrings of input string according to brackets
    s1 = Stack() # will store the values of evaluate(substring)
    s2 = Stack() # will store the values of bracket depth
    n = len(string)
    i, j = 0, 0
    brackets = 0

    while (j < n):
        if (ord(string[j]) > 47 and ord(string[j]) < 58):
            brackets += 1
            if (i != j):
                s.push(string[i:j])
            i = j
            while (string[j] != '('):
                j += 1
        elif (string[j] == ')'):
            brackets -= 1
            while (j < n-1 and string[j+1] == ')'):
                brackets -= 1
                j += 1
            s.push(string[i:(j+1)])
            i = j+1
        if (brackets == 0 and (not s.is_empty())):
            s1.clear()
            s2.clear()
            for _ in range(len(s)):
                m = s.pop()
                k = countBrackets(m)
                if (k < 0):
                    # this implies 'm' has more ')' than '('
                    # so multipliers of substrings on the left need to be mulitplied to evaluate(m)
                    # hence, we will store evaluate(m) in s1 and (-k) in s2
                    s1.push(evaluate(m))
                    s2.push(-k)
                elif (k == 0):
                    # this means that evaluate(m) needs to simply be stored in s1 without any multipliers
                    s1.push(evaluate(m))
                    if (len(s1) > 1):
                        # if s1 has multiple elements after storing evaluate(m) in s1
                        # we need to remove evaluate(m) from s1 and add it to the top element of s1
                        q1 = s1.pop()
                        q2 = s1.pop()
                        q2 = [q2[p] + q1[p] for p in range(4)]
                        s1.push(q2)
                elif (len(s2) > 0):
                    # decrement the value of top element of s2 by 1
                    # since a substring(in this algorithm) can only have 1 '(' at max
                    r1 = s2.pop()
                    r1 -= 1
                    s2.push(r1)
                    # multiply the top element of s1 by mulitplier(m) and add evaluate(m) to it
                    q1 = s1.pop()
                    q1 = [(q1[p])*findMultiplier(m) + evaluate(m)[p] for p in range(4)]
                    s1.push(q1)
                    if (s2.top() == 0 and len(s1) > 1):
                        # remove the top element of s2 when it equals zero
                        s2.pop()
                        # add the value of top element of s1 to the value at 2nd from top
                        q1 = s1.pop()
                        q2 = s1.pop()
                        q2 = [q2[p] + q1[p] for p in range(4)]
                        s1.push(q2)
            # for every s1, add the value of its top element(also its only element) to L
            L = [L[p] + s1.top()[p] for p in range(4)]
        if (j == n-1 and i < j):
            # add evaluate(substring) of remaining elements without brackets at the end of string
            L = [L[p] + evaluate(string[i:(j+1)])[p] for p in range(4)]
        j += 1
    return L
