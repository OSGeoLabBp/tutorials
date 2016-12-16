def area(coords):
    w = 0.0
    for i in range(len(coords)):
        j = (i + 1) % len(coords)
        #print("(%.1f + %.1f) * (%.1f - %.1f)" % (coords[j][0], coords[i][0], coords[j][1], coords[i][1]))
        w += (coords[j][0] + coords[i][0]) * (coords[j][1] - coords[i][1])
    return abs(w) /2.0

coords0 = [[1, 1], [3, 1], [2, 2]]
coords = [[634110.62 , 232422.09 ],
    [634108.23, 232365.96],
    [634066.13, 232378.12],
    [634062.95, 232457.58],
    [634111.68, 232454.93],
    [634110.62, 232422.09]]
print(area(coords0))
print(area(coords))
