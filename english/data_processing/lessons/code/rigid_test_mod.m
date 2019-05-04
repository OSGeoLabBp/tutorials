B = dlmread('gcp.txt');
A = dlmread('gcp_photo.txt');

[ret_R, ret_t, ret_s] = rigid_transform_3D_mod(A, B);
ret_R
ret_t
ret_s
A2 = ((ret_R*((A-mean(A))*1.0 + mean(A))') + ret_t)'

% Find the error
err = A2 - B;
err2 = err .* err;
serr2 = sum(err(:));
rmse = sqrt(serr2/rows(B));

disp(sprintf("RMSE: %f", rmse));
