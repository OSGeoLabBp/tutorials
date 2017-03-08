#! /usr/bin/env python

# search for loop using connected points of a levelling network
# input file format: startp endp height_diff distance

import sys

def addp(obs, loop, indx):
    for i in range(indx[-1], len(obs)):
        ob1 = obs[i]
        if ob1[0] == loop[-1] and ob1[1] != loop[-2] and not ob1[1] in loop[1:]:
            # connection to end point
            loop.append(ob1[1])
            indx[-1] = i + 1
            indx.append(0)
            return loop, indx
        if ob1[1] == loop[-1] and ob1[0] != loop[-2] and not ob1[0] in loop[1:]:
            # connection to end point
            loop.append(ob1[0])
            indx[-1] = i + 1
            indx.append(0)
            return loop, indx
    return loop, indx

if len(sys.argv) < 2:
    print ("Usage loops input_file")
    #sys.exit()
    fname = "loops.txt"
else:
    fname = sys.argv[1]
f = open(fname, "r")
obs = []
for line in f:
    obs.append(line.split())
loops = []
for ob in obs:
    loop = [ob[0], ob[1]]
    indx = [0, 0]
    while True:
        n = len(loop)
        loop, indx = addp(obs, loop, indx)
        if loop[0] == loop[-1]:
            loops.append(loop[:])   # make a copy of list
            n = len(loop)   # force back step
        if len(loop) == n:
            # no new point or loop found step back
            loop.pop()
            indx.pop()
            indx[-1] += 1
            if len(loop) < 3:
                break
n = 0
m = 0
for i in range(len(loops)):
    # remove duplicates
    loop1 = loops[i]
    n1 = len(loop1)
    s1 = set(loop1)
    for j in range(i+1, len(loops)):
        loop2 = loops[j]
        if n1 == len(loop2) and s1 == set(loop2):
            break   # same route found
    else:
        n += 1
        if m < len(loop1):
            m = len(loop1)
        print (loop1)
print (n, m)
