import pandas as pd
from search_file import *
from data_structure import *

############################## HELPER FUNCTIONS ##################################

def normalise(array, factor):
    for i in range(len(array)):
                new_row = [val/factor for val in array[i]]
                array[i] = new_row
    return array

def max_val_finder(array):
    max_overall_value = 0
    for i in range(len(array)):
        max_value = max(array[i])
        if max_value > max_overall_value:
            max_overall_value = max_value
    return max_overall_value

def remove_diag(array):
    for i in range(len(array)):
        array[i][i] = 0
    return array 

###################################################################################


def repeat_similarity(all_modules, index1, index2):
    '''
    Compares all modules available in module_dict.json for repeated keywords
    Parameters:
        all_modules (dict): Dictionary containing all modules
        index1 (int): Takes values 1 or 2
        index2 (int): Takes values 1 or 2
            (1,1): Compares taught keywords 
            (2,2): Compares required keywords
            (1,2): Compares taught keywords in module 1 with required keywords in module 2.
    Returns:
        num_repeated_keywords (array): Returns an array where component ij is the 
        the number of keywords that are repeated across module i and module j.
    '''
    module_codes = list(all_modules.keys())
    #initialising
    repeated_keywords_array = []

    for module1 in module_codes:
        module_dict1 = all_modules[module1]
        repeat_count = []
        for module2 in module_codes:
            module_dict2 = all_modules[module2]
            overlap_list = is_there_overlap(module_dict1, module_dict2, index1, index2)
            repeat_count.append(overlap_list[0])
        repeated_keywords_array.append(repeat_count)

    #Remove diagonal components and finding maximum value
    max_overall_value = max_val_finder(repeated_keywords_array)
    repeated_keywords_array = remove_diag(repeated_keywords_array)

    #Normalising with respsect to maximum value
    if max_overall_value != 0:
        repeated_keywords_array = normalise(repeated_keywords_array, max_overall_value)

    return repeated_keywords_array

def data_to_excel(all_modules):
    taught_keywords_array = keyword_similarity(all_modules)
    module_codes = list(all_modules.keys())
    df1 = pd.DataFrame(taught_keywords_array,
                    index=module_codes,
                    columns=module_codes)
    df1.to_excel(excel_writer = "/Users/vanessamadu/Documents/StudentShapers/StudentShapers_code/test.xlsx")






'''for i in range(len(module_codes)):
    taught_keywords_array[i] = [module_codes[i]] + taught_keywords_array[i]
repeat_count_matrix = [[0]+module_codes]
repeat_count_matrix.append(taught_keywords_array)
#df = pd.DataFrame(repeat_count_matrix).T///