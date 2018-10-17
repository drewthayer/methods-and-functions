# methods-and-functions
Mathematical methods and utility functions I've written in python to help with work and side projects.

## Table of Contents:

  - DataTools
  - CoordinateTransforms
  - SignalProcessing
  - AudioProcessing
  - JsonUtils
  - FileUtils
  - WebScraping

## Module Descriptions:

### DataTools
tools for working with data

__imputation.py__: tools for imputing missing values in a data set
  - df_impute_previous_index
        - imputes missing values based on prior index in pandas dataframe, uses np array for speed. Preserves column names and indices.

### CoordinateTransforms
mathematical methods for transforming points between coordinate systems

__plane_transforms.py__

Say you have a point in an arbitrary quadrilateral, and you want to know where that point would lie, precisely, in a plane of your choice, like a rectangle. These transforms allow mathematical transformation of a point's location from one coordinate system to another. They come from the disciplines of image rectification and geographic projection.

#### 1. HomographyTransform()

The Homography Transform requires 4 points to define an original plane and another 4 points to define a target plane. In linear algebra, this transform is defined as:

          Hx = b

 where H is the homography matrix (a function of input plane coordinates), x is the transform vector, and b is the coordinates of the target.

 Since we usually know the coordinates of the input and target planes (H and b), we fit the transform by solving the inverse problem to find x.

Example:

<img alt="homography" src="/figures/homography_example.png" width="800">

#### 2. BarycentricTransform()

This transform is built around geometric properties of triangles, therefore it only requires 3 points to define an original plane. This transform is also defined in classic linear algebra formulation:

        Ax = b

But here, A represents the input plane coordinates and b represents the coordinates of the point in the input plane. The vector x defines the _barycentric coordinates_ which map b to A. These coordinates are specific to the input triangle's geometry.

Barycentric coordinates (x) are found by inverting A and taking the dot product of (A_inv, b).

These coordinates are precise, but not useful for most applications because they are defined relative to the triangle's vertices. For most applications they will need to be transformed to cartesian coordinates.

In the _convert_to_cartesian_ method, the barycentric coordinates (x) are multiplied by the target plane coordinates to find the target point in x,y coordinates.

<img alt="barycentric" src="/figures/barycentric_example.png" width="800">

Note that 'P' can lie outside of the triangle.


### SignalProcessing

These tools aid in processing time-series signals. They were designed for processing digital audio files, but could be useful for many periodic time-series applications.

__audioparsers.py__: tools that parse an audio file by finding peaks
  - _LowpassFilterAudioParser()_:
      - smooths signal with a lowpass butterworth filter (scipy.signal.butter)
      - finds peaks using scipy.signal.argrelextrema
      - functionality for removing double peaks that are close together

  - _IterativeThresholdAudioParser()_:
      - steps through audio file window by window, searching for peaks and troughs
      - threshold dependent, will only work if peak/trough amplitudes are relatively consistent through file

__preprocessing.py__: tools for pre-processing digital signals
  - _clip_signal_start_
  - _clip_signal_both_ends_
  - _cutoff_threshold_from_signal_max_
      - defines a cutoff amplitude for a signal based on the percent of the average max value within n number of bins
  - _clip_signal_start_by_threshold_
  - _clip_signal_end_by_threshold_

### AudioProcessing

__audio_tools.py__: Tools to help with reading audio files
  - _convert_audio_file_:  uses ffmpeg (can install with homebrew) to convert audio files, e.g. from .m4a to .wav
  - _read_wavefile_: uses python's wave library to read a .wav file and return the signal and framerate

### JsonUtils
utilities for working with JSON files
__write_tools.py__
  - _write_or_update_to_json_
      - writes a new dictionary to a JSON file
      - if the JSON file doesn't exist, it creates a new file
      - if the JSON file already exists, it appends to the file

__check_json_length.py__: checks the length of a dictionary in a .json file
      - if file contains a nested dict, prints ('nested dict')
      - if file does not contain a dict, prints ('not a dict')
  ~~~
  $ python check_json_length.py some_file.json
  ~~~

__dict_methods.py__: methods for working with dictionaries
  - _sort_annotations_dict_to_list_
  
__json_to_csv.py__
  - converts a one-level dictionary in a .json file to a row-wise .csv

### FileUtils
utilities for working with file io

__move_copy.py__: functions to move/copy files between directories
  - _move_files.py_
  - _copy_files.py_

__count_files.py__: count number of files in a directory, prints integer (n_files) to terminal
  ~~~
  $ python count_files.py some_directory
  ~~~

### WebScraping

__selenium_scrapers.py__: tools for using Selenium for scraping webpages with asynchronous javascript
  - _AirbnbSpider()_: crawls Airbnb webpages based on city, state, min_price, max_price in increments (default $10), enters each individual listing and returns listing data and photos from listing
      - see script for cmd line args
  - _scrape_airbnb_get_images.py_: function for implementing AirbnbSpider() class
  - _soup_example.py_: example of scraping images with BeautifulSoup

## Resources

### Web Scraping

image scraping tutorials:

https://www.pyimagesearch.com/2015/10/12/scraping-images-with-python-and-scrapy/

https://realpython.com/web-scraping-with-scrapy-and-mongodb/

http://www.thecodeknight.com/post_categories/search/posts/scrapy_python

scrape tools for airbnb:

 - js tool : https://github.com/nonlinearnarrative/scrape-airbnb

 - scrapy blog: https://www.verginer.eu/blog/web-scraping-airbnb/#setting-up-the-system

 - robust, with scrapy-splash, but doesn't quite work: https://github.com/bashedev/airbnb_scraper

 - simpler, works: https://github.com/adodd202/Airbnb_Scraping

 - another project: https://github.com/drewthayer/airbnb-data-collection/blob/master/airbnb.py

 ### using scrapy

 tutorial: https://realpython.com/web-scraping-with-scrapy-and-mongodb/

 ~~~
 scrapy crawl spider -o results.json
 ~~~

### simple scraping: requests.get()

 it appears that airbnb city pages might not be  scrapable for listing numbers? This file has no listing numbers in it:

 ~~~
r = requests.get(url)
text = r.text
with open('out2.txt','w') as f:
    f.write(text)
 ~~~

### scraping basics

1. check source code to see if what you want is in the page's source. Two options:
    - mac, chrome: alt+cmd+u, or view-> developer-> view source
    - save to file: requests.get().text

2. scraping w/ javascript engine
    - selenium:
        - install chromedriver (brew), export to PATH
            https://stackoverflow.com/questions/38081021/using-selenium-on-mac-chrome

        - tutorial: https://medium.com/@hoppy/how-to-test-or-scrape-javascript-rendered-websites-with-python-selenium-a-beginner-step-by-c137892216aa

        - examples:
            - https://testdriven.io/building-a-concurrent-web-scraper-with-python-and-selenium
            - https://realpython.com/web-scraping-with-scrapy-and-mongodb/

3. finding elements by xpath
        - evaluate in console $x('//*[contains(@src, https)]')
