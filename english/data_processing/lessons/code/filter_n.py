""" filter ascii point cloud save every nth line
    usage: python filter_n.py n [input}
        n - lines to written, default: 10
        input - name of ascii point cloud or standard input
"""
import sys

i = j = 0
n = 10
fp = sys.stdin
if len(sys.argv) > 1:
    try:
        n = int(sys.argv[1])
    except:
        sys.exit(-1)
if len(sys.argv) > 2:
    try:
        fp = open(sys.argv[2])
    except:
        sys.exit(-2)
for line in fp:
    i += 1
    if i % n == 0:
        print(line.strip())
