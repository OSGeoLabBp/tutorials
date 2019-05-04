% This function finds the optimal Rigid/Euclidean transform in 3D space
% It expects as input a Nx3 matrix of 3D points.
% It returns R, t
% original work of Nghia Ho (http://nghiaho.com/?page_id=671)
% corrected by Zoltan Siki

% You can verify the correctness of the function by copying and pasting these commands:
%{

R = orth(rand(3,3)); % random rotation matrix

if det(R) < 0
	R (:,3) *= -1;
end

t = rand(3,1); % random translation

n = 10; % number of points
A = rand(n,3);
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

%}

% expects row data
function [R,t,sc] = rigid_transform_3D_mod(A, B)
    if nargin != 2
	    error("Missing parameters");
    end
    assert(size(A) == size(B))

    centroid_A = mean(A);
    centroid_B = mean(B);
    N = rows(A);
    H = (A - centroid_A)' * (B - centroid_B);
    [U,S,V] = svd(H);
    % rotation matrix
    R = V*U';
    if det(R) < 0
        R(:,3) *= -1;
    end
    % translation
    t = -R * centroid_A' + centroid_B';
    % scale
    sc = norm(B - centroid_B, 2) / norm(A - centroid_A, 2);
end
