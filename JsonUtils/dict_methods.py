import json

def sort_annotations_dict_to_lists(annots, categories):
    ''' sorts keys in a dict into separate lists based on their values
        input: annots (dict)
        output: 3 lists of keys

        set for 3 categories '''
    cat_0 = []
    cat_1 = []
    cat_2 = []
    for k in annots.keys():
        if annots[k] == categories[0]:
            cat_0.append(k)
        elif annots[k] == categories[1]:
            cat_1.append(k)
        elif annots[k] == categories[2]:
            cat_2.append(k)
    return cat_0, cat_1, cat_2
