import numpy as np

N = np.array([[ 3.35774, -1.68663, -0.62988, -1.04123],
              [-1.68663,  3.15898, -0.90703, -0.56532],
              [-0.62988, -0.90703,  4.05644, -2.51953],
              [-1.04123, -0.56532, -2.51953, 4.12608]])
# Moore-Penrose pseudo inverse
print('Determinant: {:.3f}'.format(np.linalg.det(N)))
inv1 = np.linalg.pinv(N)
print('Moore-Penrose pseudo inverse')
print(inv1)
print('N == N * inv1 * N ? {}'.format(np.allclose(N, N.dot(inv1).dot(N))))
# Singular value decomposition (SVD)
U, S, VT = np.linalg.svd(N)     # attention V transpose is returned!
S1 = np.array([ 1.0/s if abs(s) > 1e-6 else 0 for s in S])
inv2 = VT.T.dot(np.diag(S1)).dot(U.T)
print('SVD general inverse')
print(inv2)
print('inv1 == inv2 ? {}'.format(np.allclose(inv1, inv2)))
# regularize matrix with eigenvalues
lamb, E = np.linalg.eig(N)
N1 = np.zeros(N.shape)
for i in range(lamb.size):
    if abs(lamb[i]) < 1e-6:
        N1 = N1 + np.outer(E[:,i], E[:,i])  # diad product
inv3 = np.linalg.inv(N + N1) - N1
print('General inverse from regularization')
print(inv3)
print('inv1 == inv3 ? {}'.format(np.allclose(inv1, inv3)))
