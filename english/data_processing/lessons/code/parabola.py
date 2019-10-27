import sys
import numpy as np
import numpy.polynomial.polynomial as poly
import matplotlib.pyplot as plt

# read input data
fn = 'parabola.csv'
if len(sys.argv) > 1:
    fn = sys.argv[1]
f = open(fn, 'r')
x = []
y = []
for line in f:
    l = line.strip().split(';')
    x.append(float(l[0]))
    y.append(float(l[1]))
coefs = poly.polyfit(x, y, 2)
x_new = np.linspace(x[0], x[-1], num=len(x)*10)
ffit = poly.polyval(x_new, coefs)
plt.plot(x, y, 'ro')
plt.plot(x_new, ffit)
plt.show()
