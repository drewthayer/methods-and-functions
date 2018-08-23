import numpy as np

''' homography equations:
    http://www.corrmap.com/features/homography_transformation.php '''

class HomographyTransform(object):
    ''' fit a homeography transform and transform points to projection in new plane '''
    def __init__(self, xx, yy, XX, YY):
        # initial coordinates in x,y
        self.x1, self.x2, self.x3, self.x4 = xx
        self.y1, self.y2, self.y3, self.y4 = yy

        # plane of projection in X, Y
        self.X1, self.X2, self.X3, self.X4 = XX
        self.Y1, self.Y2, self.Y3, self.Y4 = YY

        # initiate empty parameters
        self.H = np.array([])
        self.B = np.array([])

    def define_H(self):
        col1 = np.array([self.x1, self.x2, self.x3, self.x4, 0, 0, 0, 0]).reshape(-1,1)
        col2 = np.array([self.y1, self.y2, self.y3, self.y4, 0, 0, 0, 0]).reshape(-1,1)
        col3 = np.array([1, 1, 1, 1, 0, 0, 0, 0]).reshape(-1,1)
        col4 = np.array([0, 0, 0, 0, self.x1, self.x2, self.x3, self.x4]).reshape(-1,1)
        col5 = np.array([0, 0, 0, 0, self.y1, self.y2, self.y3, self.y4]).reshape(-1,1)
        col6 = np.array([0, 0, 0, 0, 1, 1, 1, 1]).reshape(-1,1)
        col7 = np.array([-self.x1 * self.X1, -self.x2 * self.X2, -self.x3 * self.X3, -self.x4 * self.X4, -self.x1 * self.Y1, -self.x2 * self.Y2, -self.x3 * self.Y3, -self.x4 * self.Y4]).reshape(-1,1)
        col8 = np.array([-self.y1 * self.y1, -self.y2 * self.X2, -self.y3 * self.X3, -self.y4 * self.X4, -self.x1 * self.Y1, -self.x2 * self.Y2, -self.x3 * self.Y3, -self.x4 * self.Y4]).reshape(-1,1)

        self.H = np.concatenate((col1, col2, col3, col4, col5, col6, col7, col8), axis=1)

    def define_B(self):
        self.B = np.array([self.X1, self.X2, self.X3, self.X4, self.Y1, self.Y2, self.Y3, self.Y4]).reshape(-1,1)

    def fit(self):
        self.define_H()
        self.define_B()
        self.x = np.linalg.solve(self.H, self.B)

    def transform(self, P):
        ''' P = point in (x,y) to transform to (X, Y) '''
        # unpack parameters
        a, b, c, d, e, f, g, h = self.x

        # target coordinates
        x = P[0]
        y = P[1]

        # calc X and Y
        X = (a * x + b * y + c)/ (g * x + h * y + 1)
        Y = (d * x + e * y + f)/ (g * x + h * y + 1)

        return float(X), float(Y)

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
