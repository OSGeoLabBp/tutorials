import pandas as pd
from point import Point

# orientation
# read coordinates
df = pd.read_csv('coo.csv')
pnts = {}                   # new dictionary for points
# convert data to dictionary of Point objects
for i in range(df.shape[0]):
    pnts[df['id'][i]] = Point(df['x'][i], df['y'][i])
# read station target and mean direction from csv file
df = pd.read_csv('ori.csv')
# calculate orientation angles
o = []
for i in range(df.shape[0]):
    o.append((pnts[df['target'][i]] - pnts[df['station'][i]]).bearing() -
             df['direction'][i])
print sum(o) / len(o)



