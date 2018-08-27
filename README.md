## methods-and-functions
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

#### 2. Barycentric transform

This transform is built around geometric properties of triangles, therefore it only requires 3 points to define an original plane. This transform is also defined in classic linear algebra formulation:

        Ax = b

But here, A represents the input plane coordinates and b represents the coordinates of the point in the input plane. The vector x defines the _barycentric coordinates_ which map b to A. These coordinates are specific to the input triangle's geometry.

Barycentric coordinates (x) are found by inverting A and taking the dot product of (A_inv, b).

These coordinates are precise, but not useful for most applications because they are defined relative to the triangle's vertices. For most applications they will need to be transformed to cartesian coordinates.

In the _convert_to_cartesian_ method, the barycentric coordinates (x) are multiplied by the target plane coordinates to find the target point in x,y coordinates.

<img alt="barycentric" src="/figures/barycentric_example.png" width="800">


### Signal Processing Tools

These tools aid in processing time-series signals. They were designed for processing digital audio files, but could be useful for many periodic time-series applications.

Description in progress...

### Audio Processing Tools

Tools to help with reading audio files

 - _convert_audio_file_:  uses ffmpeg (can install with homebrew) to convert audio files, e.g. from .m4a to .wav
 - _read_wavefile_:       uses python's wave library to read a .wav file and return the signal and framerate


### JSON Utils

utilities for working with JSON files

__write_or_update_to_json__

  - writes a new dictionary to a JSON file
  - if the JSON file doesn't exist, it creates a new file
  - if the JSON file already exists, it appends to the file
