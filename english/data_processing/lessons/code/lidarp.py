import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata
from mpl_toolkits.mplot3d import Axes3D

step = 10   # grid step
# read scattered points
a = np.loadtxt('lidar.txt', delimiter=',')
x = a[:,0]
y = a[:,1]
z = a[:,2]
# bounding box
xmin = 548040.0
ymin = 5129010.0
zmin = round(z.min() + 5.0, -1)
xmax = 548300.0
ymax = 5129270.0
zmax = round(z.max() - 5.0, -1)
# grid interpolation
xi = np.arange(xmin, xmax+step, step)
yi = np.arange(ymin, ymax+step, step)
xi, yi = np.meshgrid(xi, yi)
zi = griddata((x, y), z, (xi, yi), method='linear')
# 2D plot
fig = plt.figure()
plt.contour(xi,yi,zi,np.arange(zmin,zmax+step, step))
#plt.plot(x,y,'k.')
plt.xlabel('xi',fontsize=16)
plt.ylabel('yi',fontsize=16)
plt.savefig('lidar_contour.png',dpi=100)
plt.close(fig)
# 3D plot
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_wireframe(xi, yi, zi)
ax.contour3D(xi, yi, zi, 10)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
plt.savefig('lidar_3dcontour.png',dpi=100)
plt.close(fig)
# volume calculation
vol = sum(zi[zi > 1000] - 1000.0) * step**2
print('Volume above 1000m: {:.0f} m3'.format(vol))
