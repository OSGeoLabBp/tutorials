Generalized inverse
===================

*Keywords*: inverse, eigen value, eigen vector, SVD

*Data file*: -

*Program file*: inverse.m

In case of free network adjusment the determinant of normal equation will be
zero. The regular inverse can't be calculated, the generalized inverse must be 
used.

Three recipes will be shown in this example to make generalized inverse using
Octave. In case of least squares estimation of geodetic networks we work with
positive semi definit matrices.

#. Moore-Penrose pseudo inverse

The pinv function of octave can be used to calculate pseudo iverse.

.. code:: octave

    N = [3.35774, -1.68663, -0.62988, -1.04123;
        -1.68663,  3.15898, -0.90703, -0.56532;
        -0.62988, -0.90703,  4.05644, -2.51953;
        -1.04123, -0.56532, -2.51953, 4.12608]
    det(N)   % deteminant is zero
    inv1 = pinv(N)  % pseudo inverse
    N * pinv(N) * N   % should be N

#. Singular Value Decomposition (SVD)

Let's decomposit the coefficient matrix into the product of three matrices.

N = V * S * U'

where:

* S is a diagonal matrix
* U * U' = I (unit matrix)
* V * V' = I

The generalized inverse:

V' * S1 * U

where the elements of S1 are the reciprocal value of element from S if it is not zero

.. code:: octave

    [U, S, V] = svd(N);
    S1 = zeros(rows(S), columns(S));
    for i=1:rows(S)
        if (abs(S(i,i)) > 1e-6)
            S1(i, i) = 1.0 / S(i, i);
        end
    end
    inv2 = V * S1 * U'

#. Let's transform the matrix to have regular inverse. 
   Create diad from the eingen vectors belonging to the zero eigenvalues and
   add them to the matrix. This matrix has regular inverse. Finally
   substract the diads from the regular inverse.

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

.. note:: *Develeopment tipps*:

    Use vectorization to avoid loop.
