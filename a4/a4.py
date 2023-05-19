import random
import math

# evaluates (a^b) % c
# O(log(q)) time taken for constant number of arithmetic operations on log(q)-bit numbers
# function is recursively called log(m) times
# O(log(m)*log(q)) time
def modPow(a, b, c):
    if (b == 0):
        return 1
    elif (b % 2 == 0):
        return (modPow(a, b//2, c) * modPow(a, b//2, c)) % c
    else:
        return ((a % c) * modPow(a, b//2, c) * modPow(a, b//2, c)) % c


#To generate random prime less than N
def randPrime(N):
	primes = []
	for q in range(2,N+1):
		if(isPrime(q)):
			primes.append(q)
	return primes[random.randint(0,len(primes)-1)]


# To check if a number is prime
def isPrime(q):
	if(q > 1):
		for i in range(2, int(math.sqrt(q)) + 1):
			if (q % i == 0):
				return False
		return True
	else:
		return False


# pattern matching
def randPatternMatch(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatch(q,p,x)


# pattern matching with wildcard
def randPatternMatchWildcard(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatchWildcard(q,p,x)


# return appropriate N that satisfies the error bounds
def findN(eps,m):
    # The number of prime factors of a positive integer d is at most log2(d)
    # (Number of primes that are less than or equal to N) <= N/(2*log2(N))
    # f(p) mod q = f(x) mod q)
    # f(p) - f(x) is a multiple of q and it has at most log2(f(p) - f(x)) prime factors
    # max value of f(p) - f(x) is 26^(m) - 1
    # log2(26^(m)-1)/(N/(2*log2(N))) <= eps
    # 2*m*log2(26)/eps <= N/log2(N)
	return int(((4*math.log2(26)*m)/eps)*(math.log2((2*m*math.log2(26))/eps)))


# return sorted list of starting indices where p matches x
def modPatternMatch(q,p,x):
    # m = len(p)
    n = len(x)
    L = [] # sorted list of indices where p matches x
    pValue = 0 # stores f(p) mod q
    i = 0
    # store value of (26^(m-1)) mod q
    # O(log(q)) space
    expValue = modPow(26, len(p)-1, q) # O(log(m)*log(q)) time
    iValue = 0 # stores f(x[i...(i+m-1)]) mod q
    # initialize iValue to f(x[0...(m-1)]) mod q
    # m iterations take place in the loop
    # constant number of arithmetic operations on log(q) bit numbers take place in each iteration
    # O(m*log(q)) time
    for j in range(len(p)):
        pValue = (((26 % q) * pValue) % q + (((ord(p[j]) % q) - (65 % q)) % q)) % q
        iValue = (((26 % q) * iValue) % q + (((ord(x[j]) % q) - (65 % q)) % q)) % q
    if (iValue == pValue):
        L.append(0)
    # (n-m) iterations take place in the loop
    # constant number of arithmetic operations on log(q) bit numbers take place in each iteration
    # O((n-m)*log(q))
    for i in range(1, n-len(p)+1):
        iValue = (iValue - ((expValue*((ord(x[i-1]) % q) - (65 % q))) % q)) % q
        iValue = (iValue * (26 % q)) % q
        iValue = (iValue + (((ord(x[i+len(p)-1]) % q) - (65 % q)) % q)) % q
        if (iValue == pValue):
            L.append(i)
    return L
# Space Complexity Analysis
# values of variables iValue, pValue, expValue can be upto q -- O(log(q)) space
# value of (i+m-1) can go upto n-1 -- O(log(n)) space
# output list L -- O(k) space
# Space complexity of modPatternMatch is O(k + log(n) + log(q))
# Time complexity is O((m+n)*log(q))


# return sorted list of starting indices where p matches x
def modPatternMatchWildcard(q,p,x):
    # we change the function f() in the wildcard case by treating the substring and pattern as
    # split at the index of the '?'
    # so the pattern 'AA?CD' and substring 'AHDUI' is checked as
    # f('AA') == f('AH') and f('CD') == f('UI')
    # 
    # m = len(p)
    n = len(x)
    L = [] # sorted list of indices where p matches x
    wildIndex = p.index('?') # O(m) time
    # wildExpValue stores the (exponent of 26 at the wildIndex in pattern) mod q
    if (wildIndex != len(p)-1):
        wildExpValue = modPow(26, len(p)-wildIndex-2, q)
    else:
        wildExpValue = 1
    # store value of (26^(m-1)) mod q
    expValue = modPow(26, len(p)-1, q)
    pValue = 0 # stores f(p) mod q
    iValue = 0 # stores f(x[i...(i+m-1)]) mod q
    # initialize iValue to f(x[0...(m-1)]) mod q
    # m iterations take place in the loop
    # constant number of arithmetic operations on log(q) bit numbers take place in each iteration
    # O(m*log(q)) time
    for j in range(len(p)):
        if (j == wildIndex):
            pValue = (pValue * (26 % q)) % q
            iValue = (iValue * (26 % q)) % q
        else:
            pValue = (((26 % q) * pValue) % q + (((ord(p[j]) % q) - (65 % q)) % q)) % q
            iValue = (((26 % q) * iValue) % q + (((ord(x[j]) % q) - (65 % q)) % q)) % q
    if (iValue == pValue):
        L.append(0)
    i = 0
    # (n-m) iterations take place in the loop
    # constant number of arithmetic operations on log(q) bit numbers take place in each iteration
    # O((n-m)*log(q)) time
    for i in range(1, n-len(p)+1):
        iValue = (iValue - ((expValue*(((ord(x[i-1]) % q) - (65 % q)) % q)) % q)) % q # remove the most significant value from iValue
        if (wildIndex == len(p)-1):
            iValue = (iValue + (((ord(x[i+wildIndex-1]) % q) - (65 % q)) % q)) % q # add the value at old wildIndex
        else:
            iValue = (iValue - ((wildExpValue*(((ord(x[i+wildIndex]) % q) - (65 % q)) % q)) % q) + ((26 % q)*wildExpValue*(((ord(x[i+wildIndex-1]) % q) - (65 % q)) % q) % q)) % q
        iValue = (iValue * (26 % q)) % q
        if (wildIndex != len(p)-1):
            iValue = (iValue + (((ord(x[i+len(p)-1]) % q) - (65 % q)) % q)) % q
        if (iValue == pValue):
            L.append(i)
    return L
# Space Complexity Analysis
# values of variables iValue, pValue, expValue, wildExpValue can be upto q -- O(log(q)) space
# whenever these values are added to, subtracted from, multiplied to another value, mod q operation is done
# value of (i + wildIndex) can go upto n-1 -- O(log(n)) space
# output list L -- O(k) space
# Space complexity of modPatternMatchWildcard is O(k + log(n) + log(q))
# Time complexity is O((m+n)*log(q))
