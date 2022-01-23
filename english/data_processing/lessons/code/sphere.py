import numpy as np
from math import sqrt
from sys import argv

def sphere(x_, y_, z_):
    """
        calculate best fitting sphere (LSM) on points
        :param returns: x0, y0, z0, R
    """
    n_ = x_.shape[0]
    a = np.c_[x_, y_, z_, np.full(n_, 1, 'float64')]
    b = -np.square(x_) - np.square(y_) - np.square(z_)
    res = np.linalg.lstsq(a, b, rcond=None)[0]
    return -0.5 * res[0], -0.5 * res[1], -0.5 * res[2], \
          sqrt((res[0]**2 + res[1]**2 + res[2]**2) / 4 - res[3])

if __name__ == "__main__":
    if len(argv) > 1:
        file_names = argv[1:]
    else:
        file_names = ['sphere1.txt']
    for file_name in file_names:
        pnts = np.genfromtxt(file_name, 'float64', delimiter=',')
        if pnts.shape[1] > 3:
            pnts = pnts[:,1:4]  # skip first column (point id)
        sph = sphere(pnts[:,0], pnts[:,1], pnts[:,2])
        print("x0: {:.3f} y0: {:.3f} z0: {:.3f} R: {:.3f}".format(sph[0], sph[1], sph[2], sph[3]))
        dr = np.sqrt(np.sum(np.square(pnts - sph[:3]), 1)) - sph[3] # difference in radius direction
        RMS = sqrt(np.sum(np.square(dr)) / pnts.shape[0])
        print("RMS: {:.3f}".format(RMS))
