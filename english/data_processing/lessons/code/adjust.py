import math
import numpy as np

mkm = 0.7
psz = np.array([1, 2, 3, 4])  # point numbers
mag = np.array([104.234, 103.487, 102.958, 101.345]) # elevations
n = 3   # number of unknown from the beginning of point numbers
# observations: start  end height_difference length
#               index index  [m]              [km]
dm = np.array([[0,    1,   -0.749,          1.1],
               [0,    2,   -1.274,          1.8],
               [0,    3,   -2.890,          1.4],
               [1,    2,   -0.530,          1.5],
               [1,    3,   -2.141,          1.9],
               [2,    3,   -1.614,          0.9 ]])
# --------- end of editable part -----------------------------------------
if n > mag.size or n <= 0:
    n = mag.size
m = dm.shape[0] # number of equations
A = np.zeros((m, n))
P = np.zeros((m, m))
l = np.zeros((m, ))
for i in range(m):
    if dm[i,0] < n:
        A[i, int(dm[i,0])] = -1
    if dm[i,1] < n:
        A[i, int(dm[i,1])] = 1
    P[i,i] = 1.0 / (dm[i,3] * mkm)**2
    l[i] = -((mag[int(dm[i,1])] - mag[int(dm[i,0])]) - dm[i,2]) * 1000
N = A.transpose().dot(P).dot(A)
r = np.linalg.matrix_rank(N)
if n > r:
    Ninv = np.linalg.pinv(N)
else:
    Ninv = np.linalg.inv(N)
f = m - r   # nunmber of redundant observations
x = Ninv.dot(A.transpose()).dot(P).dot(l)
v = A.dot(x) - l            # corrections [mm]
X = mag[:n] + (x / 1000.0)  # adjusted elevations
m0 = math.sqrt(v.transpose().dot(P).dot(v) / f)
mz = m0 * np.sqrt(np.diag(Ninv))
U = dm[:,2] + (v / 1000.0)  # adjusted observations
Qll = np.zeros((m, m))
for i in range(m):
    Qll[i,i] = 1 / P[i,i]
Quu = A.dot(Ninv).dot(A.transpose())
mu = m0 * np.sqrt(np.diag(Quu))
Qvv = Qll - Quu
s = np.zeros(m)             # statistics for blunder
sn = np.zeros(m)
r = np.zeros(m)
for i in range(m):
    s[i] = abs(v[i]) / (m0 * math.sqrt(Qvv[i,i]))
    sn[i] = abs(v[i]) / math.sqrt(Qvv[i,i])
    r[i] = 1.0 - Quu[i,i] * P[i,i]
# check for calculation
w1 = v.transpose().dot(P).dot(v)
w2 = -l.transpose().dot(P).dot(v)
print('--------------------------------------------');
print('Point Preliminary Elevation Adjusted Std.dev')
print('       elevation   change  elevation')
print('          [m]       [mm]       [m]     [mm]')
print('--------------------------------------------')
for i in range(n):
    print('{:3d}    {:8.4f}  {:8.4f}   {:8.4f} {:6.2f}'.format(psz[i], mag[i], x[i], X[i], mz[i]))
for i in range(n, len(mag)):
    print('{:3d}    {:8.4f}'.format(psz[i], mag[i]))
print('------------------------------------------------------')
print(' Sp  Ep    Obs.  Cor.  Adjust.  StDev. Stat. Stat.  r')
print('           [m]   [mm]    [m]     [mm]    t    U\n')
print('------------------------------------------------------')
for i in range(m):
    print('{:3d} {:3d} {:7.4f} {:5.2f} {:7.4f} {:6.2f} {:5.1f} {:5.1f} {:5.1f}'.format(psz[int(dm[i, 0])], psz[int(dm[i, 1])], dm[i, 2], v[i], U[i], mu[i], s[i], sn[i], r[i]))
print('------------------------------------------------------')
print('m0 = {:5.2f}'.format(m0))
print('Check: {:8.3f} = {:8.3f}'.format(w1, w2))
