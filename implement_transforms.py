import numpy as np
import matplotlib.pyplot as plt

from CoordinateTransforms.Quadrilateral import HomographyTransform

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

if __name__=='__main__':
    # define points of original plane
    arr = np.array([[500, 1700, 2000, 550], [500, 430, 2100, 2200]])
    
    # point in original plane
    P = np.array([1400, 800])

    # define points of transform plane
    XX = [0, 750, 750, 0]
    YY = [0, 0, 1000, 1000]

    # Homography transform
    xx = arr[0,:]
    yy = arr[1,:]
    HT = HomographyTransform(xx, yy, XX, YY)
    HT.fit()
    x, y = HT.transform(P)

    # plot
    plot_2_planes_2_points(xx, yy, XX, YY, P, (x,y))
