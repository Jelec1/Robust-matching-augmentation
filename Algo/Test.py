import os

from multiprocessing import Process
import time
import networkx as nx


D = nx.balanced_tree(2, 13, nx.Graph())
start_time = time.time()
a = set(nx.algorithms.traversal.dfs_preorder_nodes(D, 0))
print("---first part %s seconds ---" % (time.time() - start_time))


print({1,2,3} > {1,2})
########################################################################

# First let's get the process id for just running this script

#current = os.getpid()
#print
#"\nCurrent process:", current


########################################################################

# Now let's launch another process and get the id.

def get_id():
    # This function gets the parent process id (pp) and the current
    # process id (p).

    pp = os.getppid()
    p = os.getpid()

    print("parent process:", pp)
    print("current process:", p)


# Let's call the function get_id twice. The parent process should
# have the same id in both cases but the current processes will have
# different ids.

#print("\nFirst call:")
#p1 = Process(target=get_id)
#p1.start()
#p1.join()

#print("\nSecond call:")
#p2 = Process(target=get_id)
#p2.start()
#p2.join()

########################################################################
# Now let's demonstrate what happens if we call a process and start it
# but forget to join it to the parent process before starting a new one.
"""
print("\nThis is what happens if we join() at the end:")

print("\nFirst call:")
p3 = Process(target=get_id)
p3.start()

print("\nSecond call:")
p4 = Process(target=get_id)
p4.start()
p4.join()
"""


def hamming_distance(chaine1, chaine2):
    return sum(c1 != c2 for c1, c2 in zip(chaine1, chaine2))

mindist = 8
pole = ['10010101', '01101101', '11000010', '00111010']

poss = []
def generate_pos(num, pos):
    if num > 0:
        if len(pos) == 0:
            pos = ['0', '1']
            return generate_pos(num-1, pos)

        pos1 = [str + '0' for str in pos]
        pos2 = [str + '1' for str in pos]
        pos = pos1.extend(pos2)
        return generate_pos(num-1, pos1)
    return pos

def minDist(arr, el, le):
    mindist = le
    for e in arr:
            if e != el:
                dist = hamming_distance(e, el)
                mindist = min(mindist, dist)
    return mindist


poss = generate_pos(8, poss)
ass = ['00000000', '11111100', '11100011', '00011111']
"""while len(poss) > 0:
    ass.append({e for e in poss if minDist(ass, e, 8) == 5}.pop())
    poss1 = []

    poss = poss1
"""
poss1 = []
for el in poss:
    if minDist(ass, el, 8) >= 5 and el not in ass:
        poss1.append(el)
print(poss1)

for i in range(len(ass)):
    for j in range(len(ass)):
        if i != j:
            dist = hamming_distance(pole[i], pole[j])
            mindist = min(mindist, dist)

print(mindist)