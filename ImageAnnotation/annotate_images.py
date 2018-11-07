import matplotlib
matplotlib.use('TkAgg') # this cannot follow 'import matplotlib.pyplot as plt'

import os
import glob
import argparse
import json
import numpy as np
from skimage.io import imread
import random

import pdb

from ImageAnnotation.annotators import ImageAnnotator_TP_TN as Annotator

def load_jsonfile(filename):
    with open(filename) as f:
        file = json.load(f)
    return file

def last_dir_from_path(path):
    ''' returns last directory from path, with or w/o trailing slash'''
    # case for trailing slash
    if path[-1] == '/':
        tmp = path[:-1]
        return tmp.split('/')[-1]
    # case for no trailing slash
    else:
        return path.split('/')[-1]

#def main():


if __name__ == "__main__":
    #main()
    parser = argparse.ArgumentParser(description='Tool for labeling duplicate pairs that might be wrong.')
    parser.add_argument('--img_dir', dest='img_dir', required=True)
    parser.add_argument('--savepath', dest='savepath', default=None)
    parser.add_argument('--img_type', dest='img_type', default='png')
    parser.add_argument('--map_names', dest='map_names', action='store_true')
    parser.add_argument('--show_annotated', dest='show_annotated', action='store_true')
    parser.add_argument('--indiv_mode', dest='indiv_mode', action='store_true')
    parser.add_argument('--index', dest='idx', default=0)
    parser.add_argument('--randomize', dest='randomize', action='store_true')
    args = parser.parse_args()

    # vars from cmd line args
    filepaths = sorted(glob.glob(os.path.join(args.img_dir, '*.{}'.format(args.img_type))))[::-1]
    savepath = args.savepath
    map_names = args.map_names
    skip_annotated = not args.show_annotated
    indiv_mode = args.indiv_mode
    idx = args.idx

    # randomize images if select from cmd line
    # randomize with seed so order does not re-shuffle each time you run
    if args.randomize:
        random.Random(4).shuffle(filepaths)

    ''' optional args (default None unless flags turned to True)
        label           print in plot title
        name_mapper     json file with dict '''
    label = None
    name_mapper = None

    # category from path name if using TP_TN
    use_label = True
    if use_label:
        label = filepaths[0].split('/')[-2]

    # name_mapper dictionary, if using
    use_mapper = True
    if use_mapper:
        name_mapper = load_jsonfile('name_index_maps.json')

    # implement annotator class
    annotator = Annotator(filepaths, savepath, label, name_mapper,
                        map_names, skip_annotated, indiv_mode, idx=0)
    annotator.load_json_files()
    annotator.label_pairs()


    '''
    this script runs outside the module, but comes with the module for convenience

    custom setup for each dataset:
        label (lines 66-75)     label as parsed from filepath string

    example to run:
    $ python annotate_images.py
        --img_dir data/for_annotation_20181101/by_score/cold\ storage\ room/
        --savepath annotations/cold_storage_room.json
        --img_type png

        optional
        --map_names           must set use_mapper=True in this script
        --indiv_mode          flag for individual image mode
        --index 60            '60'(int) is index of desired image
        --randomize           default is sequential from bottom of directory
    '''
