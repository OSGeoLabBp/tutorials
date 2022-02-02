#! /usr/bin/env python

"""
    Search for all loops in an undirected graph using deep first search
    and sum up distances and a values of edges in each loop.

    Usage: loops.py input_file

    ascii input file format for a line/edge (space separated):
    startp endp distance value
"""

import sys

def addp(edges, loop, indx):
    """ find and add a point to the loop
        :param edges: edges of graph
        :param loop: actual loop
        :param indx: edge indices

        :returns: extended loop and new indx as a tuple
    """
    for i in range(indx[-1], len(edges)):
        edge = edges[i]
        if edge[0] == loop[-1] and edge[1] != loop[-2] and edge[1] not in loop[1:]:
            # connection to start point
            loop.append(edge[1])
            indx[-1] = i
            indx.append(0)
            return loop, indx
        if edge[1] == loop[-1] and edge[0] != loop[-2] and edge[0] not in loop[1:]:
            # connection to end point
            loop.append(edge[0])
            indx[-1] = i
            indx.append(0)
            return loop, indx
    return loop, indx

if len(sys.argv) < 2:
    print (f"Usage: {sys.argv[0]} input_file")
    sys.exit()
else:
    fname = sys.argv[1]
edges = []
edges_dic = {}
i = 0
with open(fname, "r") as f:
    for line in f:
        l = line.split()
        i += 1
        ll = tuple(l[:2])
        edges.append(ll)
        try:
            edges_dic[ll] = (float(l[2]), float(l[3]))
        except:
            print("Error in input file line: ", i)
            exit(-1)
loops = []
for edge in edges:
    loop = [edge[0], edge[1]]
    indx = [0, 0]
    while True:
        n = len(loop)
        loop, indx = addp(edges, loop, indx)
        if loop[0] == loop[-1]:     # closed loop found
            n1 = len(loop)
            s1 = set(loop)
            for loop2 in loops:     # check same loop found?
                if n1 == len(loop2) and s1 == set(loop2):
                    break
            else:
                loops.append(loop[:])   # make a copy of list
            n = len(loop)           # force back step
        if len(loop) == n:
            # no new point or loop found step back
            loop.pop()
            indx.pop()
            indx[-1] += 1
            if len(loop) < 2:       # no more step back
                break
loops.sort(key=len)                 # sort loop by length
n = 0
m = len(loops[-1])                  # length of longest loop
for i, loop1 in enumerate(loops):
    n += 1
    # calculate sum distance and value
    sdist = 0
    sdm = 0
    last = loop1[0]                 # start point
    for node in loop1[1:]:
        indx = last,node
        if indx in edges_dic:       # forward direction
            sdist += edges_dic[indx][0]
            sdm += edges_dic[indx][1]
        else:                       # reverse direction
            indx = node,last
            sdist += edges_dic[indx][0]
            sdm -= edges_dic[indx][1]
        last = node
    print (f"{sdm:.5f};{sdist:.1f};{loop1}")
print(f"Number of loops: {n}, Max loop length: {m}")
