s = [195]
sigma = [s[0] % 2]
n = 11*43
m = 4

for i in range(1, m+2):
    s.append((s[i-1]**2) % n)
    sigma.append(s[i] % 2)
    #print("i", i, "s_i", s[i])

print(s)
print(sigma)

"""q = 2
d = 1749
n = 6997
xs = [2101, 3035, 6101, 30]

for x in xs:
    print("x", x)
    notprime = ((x ** d) % n) != 1
    print("((x ** d) % n) != 1", ((x ** d) % n))
    for r in range(1,q):
        notprime &= ((x ** ((2 ** r) * d)) % n) != n - 1
        print("---r", r)
        print("---x^(d*2^r)", ((x ** ((2 ** r) * d)) % n))

    if notprime:
        print(x)
"""


"""
n = len(text)
l = 0

for c in ascii_uppercase:
    n_i = 0
    for char in text:
        if char == c:
            n_i += 1
    l += (n_i)*(n_i-1) / ((n-1)*n)

L = 0.027*n/((n-1)*l -0.038*n + 0.065)
print(L)

"""
"""

ass= [i for i in range(1,26) if math.gcd(i,26) == 1]

print(ass)

bss = [i for i in range(26)]

xss = [i for i in range(26)]

notfound = 0
numfound = 0

for a in ass:
    for b in bss:
        found = False
        for x in xss:
            if ((a*x + b) % 26) == x:
                print("Found a b x", a, b, x)
                numfound += 1
                found = True
        if not found:
            print("Not found ", a, b)
            notfound += 1

print(notfound)
print(numfound)
"""

"""
msgprob = [1/6, 1/6, 1/3, 1/3]
keyprob = [1/4, 1/4, 1/4, 1/4]

table = [[3,1,2,1],
        [2,0,3,3],
        [1,3,0,2],
        [0,2,1,0]]

def getprob(number):
    sum = 0
    for row in range(4):
        for cell in range(4):
            if table[row][cell] == number:
                sum += msgprob[row] * keyprob[cell]
    return sum


cryptprob = [getprob(i) for i in range(4)]

print(cryptprob)


def bayes(plain, crypto):
    cp = 0
    for i in range(4):
        if table[plain][i] == crypto:
            cp += 1
    cp /= 4

    return msgprob[plain] * cp / cryptprob[crypto]

bayestable = []
for i in range(4):
    bayestable.append([bayes(i,j) for j in range(4)])


print()

for row in bayestable:
    print(row)
"""