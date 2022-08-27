import pandas as pd
from search_file import *
from data_structure import *

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
    num_repeated_keywords = []

    for module1 in module_codes:
        module_dict1 = all_modules[module1]
        repeat_count = []
        for module2 in module_codes:
            module_dict2 = all_modules[module2]
            overlap_list = is_there_overlap(module_dict1, module_dict2, index1, index2)
            repeat_count.append(overlap_list[0])
        num_repeated_keywords.append(repeat_count)

    #Remove diagonal components and finding maximum value
    max_overall_value = 0
    for i in range(len(num_repeated_keywords)):
        num_repeated_keywords[i][i] = 0
        max_value = max(num_repeated_keywords[i])
        if max_value > max_overall_value:
            max_overall_value = max_value
    #Normalising
    
    if max_overall_value != 0:
        for i in range(len(num_repeated_keywords)):
                new_row = [val/max_overall_value for val in num_repeated_keywords[i]]
                num_repeated_keywords[i] = new_row
    return num_repeated_keywords

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