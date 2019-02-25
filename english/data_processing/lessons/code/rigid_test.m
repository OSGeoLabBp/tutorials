R = orth(rand(3,3)); % random rotation matrix

if det(R) < 0
	R (:,3) *= -1;
end
scale = 1;
R(1,1) *= scale;
R(2,2) *= scale;
R(3,3) *= scale;

t = rand(3,1) * 111; % random translation

n = 10; % number of points
A = rand(n,3);
A(:,1) *= 34;
A(:,2) *= 56;
A(:,3) *= 29;
B = R*A' + t;
B = B';

[ret_R, ret_t] = rigid_transform_3D(A, B);

A2 = (ret_R*A') + ret_t;
A2 = A2';

% Find the error
err = A2 - B;
err = err .* err;
err = sum(err(:));
rmse = sqrt(err/n);

disp(sprintf("RMSE: %f", rmse));
disp("If RMSE is near zero, the function is correct!");

