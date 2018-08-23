import numpy as np

class BarycentricTransform(object):
    '''
    finds barycentric coordinates for a triangle and
    transforms point in first triangle to new triangle

    inputs:
        xx, yy: x,y vectors for initial triangle (1x3)
        XX, YY: x,y vectors for target triangle (1x3)

    output:
        x, y '''
    def __init__(self, xx, yy, XX, YY):
        self.xx = xx
        self.yy = yy
        self.XX = XX
        self.YY = YY
        self.x = 0 # initiate as 0
        self.y = 0

    def fit(self):
        # find A_inv for Ax = b
        A = np.array([self.xx, self.yy, [1,1,1]])
        self.barytransform = np.linalg.inv(A)

    def solve_barycentric_coords(self):
        # solve Ax = b
        b = np.array([self.P[0], self.P[1], 1])
        self.barycoords = np.dot(self.barytransform, b)

    def convert_bary_to_cartesian(self):
        b = self.barycoords
        self.x = b[0] * self.XX[0] + b[1] * self.XX[1] + b[2] * self.XX[2]
        self.y = b[1] * self.YY[0] + b[1] * self.YY[1] + b[2] * self.YY[2]

    def transform(self, P):
        self.P = P
        self.solve_barycentric_coords()
        self.convert_bary_to_cartesian()
        return self.x, self.y

    # code for barycentric grid interpolation:
    # # bounding box
    # xleft = min(xx)
    # xright = max(xx)
    # ytop = min(yy)
    # ybottom = max(yy)
    #
    # # define grid
    # grid = np.mgrid[xleft:xright, ytop:ybottom].reshape(2,-1)
    # grid = np.vstack((grid, np.ones((1, grid.shape[1]))))
    #
    # for gridding
    #barycoords = np.dot(barytransform, grid)
    #barycoords = barycoords[:,np.all(barycoords>=0, axis=0)]
