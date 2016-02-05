N = [3.35774, -1.68663, -0.62988, -1.04123;
    -1.68663,  3.15898, -0.90703, -0.56532;
    -0.62988, -0.90703,  4.05644, -2.51953;
    -1.04123, -0.56532, -2.51953, 4.12608]
det(N)   % deteminant is zero
inv1 = pinv(N)  % pseudo inverse
N * pinv(N) * N   % should be N

% SVD
[U, S, V] = svd(N);
S1 = zeros(rows(S), columns(S));
for i=1:rows(S)
    if (abs(S(i,i)) > 1e-6)
        S1(i, i) = 1.0 / S(i, i);
    end
end
inv2 = V * S1 * U'

% eigen values
[E, lambda] = eig(N);
N1 = zeros(rows(N), columns(N));
for i = 1:rows(E)     % sum of diades
    if (abs(lambda(i,i)) < 1e-6)
        N1 += E(:, i) * E(:, i)';
    end
end
inv3 = inv(N + N1) - N1
