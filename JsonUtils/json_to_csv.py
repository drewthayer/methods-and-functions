import json
import os
import pandas as pd
import argparse

def main():
    parser = argparse.ArgumentParser('convert a .json dictionary to a row-wise csv')
    parser.add_argument('-f', dest='filepath', required=True, help='relative path to file')
    args = parser.parse_args()
    # load json file
    #dir = 'object_counts_total'
    #fname = 'object_counts_exterior_2018-10-10.json'
    with open(args.filepath, 'r') as f:
        d = json.load(f)

    # convert to dataframe
    df = pd.DataFrame.from_dict(d, orient='index')
    df.columns=['count']

    # save as csv
    csv_file = args.filepath.replace('.json','.csv')
    df.to_csv(csv_file, sep=',', header=False)
    print('\n {} written to csv'.format(csv_file))

if __name__=='__main__':
    ''' example: $ python json_to_csv.py --dir object_counts_total
        --fname object_counts_interior_2018-10-17.json '''
    main()
