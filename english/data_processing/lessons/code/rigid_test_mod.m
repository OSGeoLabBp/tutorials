B = dlmread('gcp.txt');
A = dlmread('gcp_photo.txt');

[ret_R, ret_t] = rigid_transform_3D(A, B);
ret_R
ret_t
A2 = ((ret_R*A') + ret_t)';

% Find the error
err = A2 - B;
err = err .* err;
err = sum(err(:));
rmse = sqrt(err/rows(B));

disp(sprintf("RMSE: %f", rmse));
