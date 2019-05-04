import numpy as np

elev = np.genfromtxt('elev.txt', delimiter=' ')
obs = np.genfromtxt('obs.txt', delimiter=' ')

mkm = 0.7                       # 0.7 mm/km
n = elev.size                   # ismeretlenek száma
m = obs.shape[0]                # egyenletek száma
A = np.zeros((m, n))            # alakmátrix
P = np.zeros((m, m))            # súlymátrix
P[[np.arange(m), np.arange(m)]] = 1 / (obs[:, -1] * mkm)**2
A[[np.arange(m), obs[:,0].astype(int)]] = -1
A[[np.arange(m), obs[:,1].astype(int)]] = 1
l = obs[:,-2] - A.dot(elev)     # tisztatagok
Ninv = np.linalg.pinv(A.T.dot(P).dot(A))
x = Ninv.dot(A.T).dot(P).dot(l) # magasság változások
v = A.dot(x) - l                # javítások
X = elev + x                    # kiegyenlített magasságok
