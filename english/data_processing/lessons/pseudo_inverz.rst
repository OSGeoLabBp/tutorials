Generalized inverse
===================

*Keywords*: inverse, eigen value, eigen vector, SVD

*Data file*: -

*Program file*: inverse.m, inverse.py

In case of free network adjusment the determinant of normal equation will be
zero. The regular inverse can't be calculated, the generalized inverse must be 
used.

Three recipes will be shown in this example to make generalized inverse using
Octave. In case of least squares estimation of geodetic networks we work with
positive semi definit matrices.

1. Moore-Penrose pseudo inverse
-------------------------------

Octave solution
~~~~~~~~~~~~~~~

The pinv function of octave can be used to calculate pseudo iverse.

.. code:: octave

    N = [3.35774, -1.68663, -0.62988, -1.04123;
        -1.68663,  3.15898, -0.90703, -0.56532;
        -0.62988, -0.90703,  4.05644, -2.51953;
        -1.04123, -0.56532, -2.51953, 4.12608]
    det(N)   % deteminant is zero
    inv1 = pinv(N)  % pseudo inverse
    N * pinv(N) * N   % should be N

Python/numpy solution
~~~~~~~~~~~~~~~~~~~~~

The pinv function is available in numpy.linalg package.

.. code:: python

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

2. Singular Value Decomposition (SVD)
-------------------------------------

Let's decomposit the coefficient matrix into the product of three matrices.

N = V * S * U'

where:

* S is a diagonal matrix
* U * U' = I (identity matrix)
* V * V' = I

The generalized inverse:

V' * S1 * U

where the elements of S1 are the reciprocal value of element from S if it is not zero

Octave solution
~~~~~~~~~~~~~~~

.. code:: octave

    % SVD
    [U, S, V] = svd(N);
    S1 = zeros(rows(S), columns(S));
    for i=1:rows(S)
        if (abs(S(i,i)) > 1e-6)
            S1(i, i) = 1.0 / S(i, i);
        end
    end
    inv2 = V * S1 * U'

Python/numpy solution
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

	U, S, VT = np.linalg.svd(N)     # attention V transpose is returned!
	S1 = np.array([ 1.0/s if abs(s) > 1e-6 else 0 for s in S])
	inv2 = VT.T.dot(np.diag(S1)).dot(U.T)
	print('SVD general inverse')
	print(inv2)
	print('inv1 == inv2 ? {}'.format(np.allclose(inv1, inv2)))

3. Let's transform the matrix to have regular inverse
-----------------------------------------------------

   Create diad from the eingen vectors belonging to the zero eigenvalues and
   add them to the matrix. This matrix has regular inverse. Finally
   substract the diads from the regular inverse.

Octave solution
~~~~~~~~~~~~~~~

.. code:: octave

    % eigen values
    [E, lambda] = eig(N);
    N1 = zeros(rows(N), columns(N));
    for i = 1:rows(E)     % sum of diades
        if (abs(lambda(i,i)) < 1e-6)
            N1 += E(:, i) * E(:, i)';
        end
    end
    inv3 = inv(N + N1) - N1

Python/numpy solution
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

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

.. note:: 

	+= does not work for numpy arrays, see the answer `here <https://stackoverflow.com/questions/35910577/why-does-python-numpys-mutate-the-original-array>`_.

.. note:: *Develeopment tipps*:

    Use vectorization to avoid loops.
