import numpy as np
import matplotlib.pyplot as plt

from CoordinateTransforms.Quadrilateral import HomographyTransform
from CoordinateTransforms.Triangle import BarycentricTransform

def plot_plane_and_point_labeled(xx, yy, P):
    corner_labels = ['p0', 'p1', 'p2', 'p3']
    target = 'P'
    fig = plt.subplots()
    corners = [p0, p1, p2, p3]
    for pt, label in zip(corners, corner_labels):
        plt.scatter(pt[0], pt[1], c='k', marker = r"$ {} $".format(label), s=300)
    plt.scatter(P[0], P[1], marker = r"$ {} $".format(target), c='r', s=300)
    plt.savefig('foot_coords_raw.png', format='png', dpi=200)
    plt.close()

def plot_plane_and_point(xx, yy, P):
    corner_labels = ['p0', 'p1', 'p2', 'p3']
    target = 'P'
    fig = plt.subplots()
    plt.scatter(xx, yy, c='k')
    plt.scatter(P[0], P[1], marker = r"$ {} $".format(target), c='r', s=300)
    plt.show()
    #plt.savefig('foot_coords_raw.png', format='png', dpi=200)
    #plt.close()


def remove_furthest_point(array):
    ''' input: array, (m x n) array, with n dimensions

        output: array, (m-1 x n) missing furthest point
                array, (1 x n) furthest point

        requires package: scipy.spatial.distance'''
    from scipy.spatial import distance

    Y = distance.pdist(array, 'euclidean')
    dist = distance.squareform(Y)
    i = np.argmax(np.sum(dist, axis=0)) # index of point furthest from others
    ii = [0,1,2,3]

    P = array[i,:]
    ii.remove(i)
    close3 = array[ii,:]
    return close3, P

def triangle_array_from_quad_array(arr, idx):
    ''' arr: 2x4 array defining quadrilateral
        idx: list of 3 indices between 0 and 3 (e.g. [0,2,3])'''
    return arr[:, idx]

def get_foot_length_barycentric_mean_3best(array):
    ''' input:  5x2 numpy array
                order = [UL, Toe, UR, LR, LL]

        output: length in cm

        requires    class: BarycentricTransform
                    function: scale_rectangle
                    function: remove_furthest_point
                                '''
    # define existing quadrilateral
    P = array[1,:]
    quad_1 = array[[0,2,3,4],:] # 4 corners of quadrilateral

    # define target quadrilateral
    xx_true = np.array([0, 850, 850, 0]).reshape(-1,1)
    yy_true = np.array([0, 0, 1100, 1100]).reshape(-1,1)
    quad_2 = np.concatenate((xx_true, yy_true), axis=1)

    # barycentric transform for 4 possible triangles of quadrilateral
    idx_combos = [[0,1,2], [1,2,3], [0,2,3], [1,0,3]]
    transformed_points = []
    for idx in idx_combos:
        # define similar triangles from both quadrilaterals
        tri_1 = triangle_array_from_quad_array(quad_1, idx)
        tri_2 = triangle_array_from_quad_array(quad_2, idx)

        # perform barycentric transform
        BT = BarycentricTransform(tri_1[:,0], tri_1[:,1], tri_2[:,0], tri_2[:,1])
        BT.fit()
        x, y = BT.transform(P)
        transformed_points.append([x,y])

    # mean of 3 best points
    #pdb.set_trace()
    transformed = np.array(transformed_points)
    closest_3, point = remove_furthest_point(transformed)
    mean3_xy = np.mean(closest_3, axis=0)
    XX = [0, 850, 850, 0]
    YY = [0, 0, 1100, 1100]
    mean3_foot_cm = scale_rectangle(XX, YY, mean3_xy, conv=2.54)

    return mean3_foot_cm

def plot_2_planes_2_points(xx, yy, XX, YY, P, P1):
    corner_labels = ['p0', 'p1', 'p2', 'p3']
    target = 'P'
    transformed = "P'"
    fig = plt.subplots()
    plt.scatter(xx, yy, c='b')
    plt.scatter(XX, YY, c='k')
    plt.scatter(P[0], P[1], marker = r"$ {} $".format(target), c='b', s=300)
    plt.scatter(P1[0], P1[1], marker = r"$ {} $".format(transformed), c='k', s=300)
    plt.title(r'Homography Transform: P in original plane (blue) to ${}$ in target plane (black)'.format(transformed))
    plt.show()

def plot_barycentric(triangle_1, triangle_2, P, P1, fname):
    fig = plt.subplots()
    plt.scatter(triangle_1[0,:], triangle_1[1,:], c='b')
    plt.scatter(P[0], P[1], c='b', marker = r"$ P $", s=300)
    plt.scatter(triangle_2[0,:], triangle_2[1,:], c='k')
    plt.scatter(P1[0], P1[1], c='k', marker = r"$ P' $", s=300)
    plt.title(r"Barycentric Transform: P in original plane (blue) to $ P'$ in target plane (black)")
    plt.show()
    #plt.savefig('Transform_Figs/' + fname, dpi=250)
    #plt.close()

if __name__=='__main__':
    # define points of original plane
    xx = [900, 1450, 2200, 1000]
    yy = [1300, 900, 1350, 2000]

    # point in original plane
    P = [1400, 1600]

    # define points of transform plane
    XX = [0, 750, 750, 0]
    YY = [0, 0, 1000, 1000]

    # 1. Homography transform
    HT = HomographyTransform(xx, yy, XX, YY)
    HT.fit()
    x, y = HT.transform(P)

    plot_2_planes_2_points(xx, yy, XX, YY, P, (x,y))

    # 2. Barycentric Transform for 4 possible triangles of quadrilateral
    quad1 = np.array([xx,yy])
    quad2 = np.array([XX,YY])

    idx_combos = [[0,1,2], [1,2,3], [0,2,3], [1,0,3]]
    transformed_points = []
    for idx in idx_combos:
        # define similar triangles from both quadrilaterals
        tri_1 = triangle_array_from_quad_array(quad1, idx)
        tri_2 = triangle_array_from_quad_array(quad2, idx)

        # perform barycentric transform
        BT = BarycentricTransform(tri_1[0,:], tri_1[1,:], tri_2[0,:], tri_2[1,:])
        BT.fit()
        x, y = BT.transform(P)
        transformed_points.append([x,y])
    transformed = np.array(transformed_points)

    # mean of 4 points
    mean4_xy = np.mean(transformed, axis=0)

    # mean of closest 3 points
    closest_3, otherpoint = remove_furthest_point(transformed)
    mean3_xy = np.mean(closest_3, axis=0)

    plot_barycentric(tri_1, tri_2, P, mean4_xy, 'barycentric')
