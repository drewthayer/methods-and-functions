### methods-and-functions
Mathematical methods and functions I've written

### Plane Coordinate Transforms

Say you have a point in an arbitrary quadrilateral, and you want to know where that point would lie, precisely, in a plane of your choice, like a rectangle. These transforms allow mathematical transformation of a point's location from one coordinate system to another. They come from the disciplines of image rectification and geographic projection.

#### 1. Homography transform

The Homography Transform requires 4 points to define an original plane and another 4 points to define a target plane. In linear algebra, this transform is defined as:

          Hx = b

 where H is the homography matrix (a function of input plane coordinates), x is the transform vector, and b is the coordinates of the target.

 Since we usually know the coordinates of the input and target planes (H and b), we fit the transform by solving the inverse problem to find x.

Example:

<img alt="homography" src="/figures/homography_example.png" width="800">
