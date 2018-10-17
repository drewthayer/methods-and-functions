import json
import os
import pandas as pd
import argparse

def main():
    parser = argparse.ArgumentParser('convert a .json dictionary to a row-wise csv')
    parser.add_argument('--dir', dest='dir', required=True, help='relative path to dir')
    parser.add_argument('--fname', dest='fname', required=True, help='filename with .json extension')
    args = parser.parse_args()
    # load json file
    #dir = 'object_counts_total'
    #fname = 'object_counts_exterior_2018-10-10.json'
    with open(os.path.join(args.dir, args.fname), 'r') as f:
        d = json.load(f)

    # convert to dataframe
    df = pd.DataFrame.from_dict(d, orient='index')
    df.columns=['count']

    # save as csv
    csv_name = args.fname.replace('.json','.csv')
    df.to_csv(os.path.join(args.dir, csv_name), sep=',', header=False)
    print('{} written'.format(csv_name))

if __name__=='__main__':
    ''' example: $ python json_to_csv.py --dir object_counts_total
        --fname object_counts_interior_2018-10-17.json '''
    main()
