import json
import sys

def main():
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        d = json.load(f)

    # check for type
    if type(d) == dict:
        print('dict: {} items'.format(len(d)))
        # check for nested dicts
        for val in d.values():
            if type(val) == dict:
                print('nested dict')
                break
    else:
        print('not a dictionary')

if __name__=='__main__':
    main()
