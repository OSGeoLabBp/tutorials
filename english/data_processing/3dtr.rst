3D ortogonal transformation
===========================

*Keywords*: transformation, 3D, point cloud

*Data files*: gcp.txt, gcp_photo.txt

*Program files*: rigid_transform_3D_mod.m, rigid_test_mod.m

This solution is based on http://nghiaho.com/?page_id=671

Let's find the rotation and translation of a point cloud to fit to some GCPs.
To solve the problem we need the coordinates for the GCPs in both reference 
systems. Let's store these values in two text files (Easting, Northing, Elevation).

GCPs in the source reference system

.. code:: 

    30.5557   48.3188    3.5465
    23.9325   21.5202    1.7207
    25.9909   21.6259   27.6905
    13.3294   27.0915   16.2552
    19.9702   40.3968   23.8941
    16.3791    5.4036   17.2654
     6.4734   46.0633    9.8115
    13.6336   28.1767    2.2597
    26.7044   40.0221   16.5392
    27.9647   38.2493   13.2022

GCPs in the target reference system

.. code::

    133.101   140.589    83.295
    119.427   121.613    98.070
    104.153   141.505   105.158
    105.286   131.409    90.394
    109.961   147.038    86.747
     98.155   121.064   108.372
    112.310   134.787    70.718
    114.882   121.867    86.678
    118.986   143.970    89.747
    121.269   141.009    91.106

The trick in the solution is to move the origin of the reference systems to 
the weight points to eliminate translation. Then the elements of the rotational matrix
are unknowns.

During the solution first the weight point of GCPs are generated in both 
reference systems and the points are translated. Then the rotational parameters 
are calculated by SVD.
Finally the translations are calculated by the weight points and the known
rotational matrix..
If more than 3 GCPs are given a least square approximation will be calculated.

Octave function:

.. code:: octave

	function [R,t] = rigid_transform_3D_mod(A, B)
		if nargin != 2
			error("Missing parameters");
		end
		assert(size(A) == size(B))

		centroid_A = mean(A);
		centroid_B = mean(B);
		N = rows(A);
		H = (A - centroid_A)' * (B - centroid_B);
		[U,S,V] = svd(H);
		R = V*U';
		if det(R) < 0
			R(:,3) \*= -1;
		end
		t = -R * centroid_A' + centroid_B';
	end

Test program for the function:

.. code:: octave

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

Result:

.. code::

	ret_R =

	   0.65980   0.39121  -0.64158
	   0.37871   0.56432   0.73357
	   0.64903  -0.72698   0.22418

	ret_t =

	   96.316
	   99.146
	   97.800

	RMSE: 0.007440

.. note:: *Development tipps*:

    Add scale difference calculation (the average ratio of the point distances from the 
    weight points in the two reference systems).
