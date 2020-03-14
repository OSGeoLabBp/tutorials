import math
import numpy as np

def rigid_transform_3D(A, B):
    """ given the coordinates of GCPs in source system in array A
        and the coordinates in the destination system in array B
    """
    centroid_A = np.mean(A, 0)
    centroid_B = np.mean(B, 0)
    N = A.shape[0]
    H = (A - centroid_A).T.dot(B - centroid_B)
    U, S, V = np.linalg.svd(H)
    # rotation matrix
    R = V.T.dot(U.T)
    if np.linalg.det(R) < 0:
        R[:,3] *= -1
    # translation
    t = -R.dot(centroid_A.T) + centroid_B.T
    # scale
    sc = np.linalg.norm(B - centroid_B, 2) / np.linalg.norm(A - centroid_A, 2)
    return R, t, sc

if __name__ == "__main__":

    A = np.loadtxt('gcp.txt', delimiter=' ')
    B = np.loadtxt('gcp_photo.txt', delimiter=' ')
    R, t, sc = rigid_transform_3D(A, B)
    print(R)
    print(t)
    print(sc)
    # check
    A2 = (R.dot(A.T)).T
    for i in range(A2.shape[0]):
        A2[i,:] = A2[i,:] + t
    err = A2 - B
    err = err * err
    err = np.sum(err)
    rmse = math.sqrt(err / A.shape[0])
    print("RMSE: {:.3f}".format(err))
    print("If RMSE is near zero, the function is correct!")
