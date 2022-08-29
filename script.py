from search_file import *
from module_comparisons import * 
from data_structure import *
import os

# Get a list of the csv files that are in the folder
module_csv = os.listdir('/Users/vanessamadu/Documents/StudentShapers/StudentShapers_code/module_csv_files')
arr.remove('.DS_Store')

# Add all modules into the json file

for module in module_csv:
    module_csv_path = 'module_csv_files/%s'%module
    dict_maker(module_csv_path, all_modules)

# Generate the Information Array

def which_info(all_modules, index1, index2, repeat_or_cluster, min_val):
    '''
    1 for repeats
    2 for clustering
    '''
    if repeat_or_cluster == 1:
        info_array = repeat_similarity(all_modules, index1, index2, 0)
    elif repeat_or_cluster == 2:
        info_array = clustering_score(all_modules, index1, index2)
    
    data_to_excel(all_modules, info_array)
    pairs = pair_finder(all_modules,info_array, min_val)
    results(pairs, index1, index2)