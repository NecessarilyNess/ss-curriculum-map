import pandas as pd
from search_file import *
from data_structure import *

############################## HELPER FUNCTIONS ##################################

def normalise(array, factor):
    '''
    Normalises all the values in symmetric array by a given factor 
    Parameters:
        array (array): Array of values
        factor (int): Factor to normalise wrt
    Returns:
        array (array): Normalised array
    '''
    for i in range(len(array)):
                new_row = [val/factor for val in array[i]]
                array[i] = new_row
    return array

def max_val_finder(array):
    '''
    Finds the maximum value in a symmetric array
    Parameters: 
        array (array): Array of values
    Returns:
        max_overall_value (int): Maximum value in the array
    '''
    max_overall_value = 0
    for i in range(len(array)):
        max_value = max(array[i])
        if max_value > max_overall_value:
            max_overall_value = max_value
    return max_overall_value

def remove_diag(array):
    '''
    Sets the components on the diagonal of a symmetric array to zero.
    Parameters:
        array (array): Array of values
    Returns:
        array (array): The same array with the diagonal set to zero.
    '''
    for i in range(len(array)):
        array[i][i] = 0
    return array 

def pair_finder(all_modules,info_array, min_val):
    '''
    Look for all the module pairs that have a similarity metric greater than min_val
    '''
    pairs = []
    module_codes = list(all_modules.keys())
    length = len(info_array)
    for i in range(length):
        for j in range(length):
            if info_array[i][j] > min_val:
                pairs.append([module_codes[i],module_codes[j]])
    return pairs

def results(pairs, index1, index2):
    '''
    This only tells us about repeated keywords and shouldn't be used in isolation as index1 and index2 need to be the same as those
    that were used to generate the info array.
    '''
    if index1 ==1 and index2==1:
        pairs = remove_duplicate(pairs)
        for i in range(len(pairs)):
            module1 = pairs[i][0]
            module2 = pairs[i][1]
            print(' '.join([code_to_name(all_modules, module1)] + ['may be similar to'] + [code_to_name(all_modules, module2)]))
    elif index1 == 1 and index2 == 2:
        for i in range(len(pairs)):
            module1 = pairs[i][0]
            module2 = pairs[i][1]
            print(' '.join([code_to_name(all_modules, module1)] + ['may be a good module to take for'] + [code_to_name(all_modules,module2)]))
    elif index1 == 2 and index2 == 2:
        pairs = remove_duplicate(pairs)
        for i in range(len(pairs)):
            module1 = pairs[i][0]
            module2 = pairs[i][1]
            print(' '.join([code_to_name(all_modules, module1)] + ["may have the same 'prerequisites' as"] + [code_to_name(all_modules, module2)]))

def remove_duplicate(pairs):
    for i in range(len(pairs)):
        pairs[i] = set(pairs[i])
    for i in range(len(pairs)):
        if pairs.count(pairs[i]) != 1:
            pairs[i] = 'dup'
    pairs.remove('dup')
    pairs = [list(pair) for pair in pairs]
    return pairs

def code_to_name(all_modules, code):
    module = all_modules[code]
    module_name = module["module information"][0][0]
    return module_name

###################################################################################


def repeat_similarity(all_modules, index1, index2, info_index):
    '''
    Compares all modules available in module_dict.json for repeated keywords
    Parameters:
        all_modules (dict): Dictionary containing all modules
        index1 (int): Takes values 1 or 2
        index2 (int): Takes values 1 or 2
            (1,1): Compares taught keywords 
            (2,2): Compares required keywords
            (1,2): Compares taught keywords in module 1 with required keywords in module 2.
        info_index (int): Selects the desired comparison metric from the following options
            0: Number of repeated keywords (normalised wrt largest value)
            1: Number of repeated keywords/number of chapters spread across (normalised wrt largest value)
            2: Maximum number of repeated keywords in any section in module 2 (normalised wrt largest value)
            3: Squared sum of number of repeated keywords in each chapter in modules 2 (normalised wrt largest value)
    Returns:
        info (array): Returns an array where component ij is the the requested comparison information 
        for module i and module j.
    '''
    module_codes = list(all_modules.keys())
    #initialising
    info_array = []

    for module1 in module_codes:
        module_dict1 = all_modules[module1]
        repeat_count = []
        for module2 in module_codes:
            module_dict2 = all_modules[module2]
            overlap_list = is_there_overlap(module_dict1, module_dict2, index1, index2)
            repeat_count.append(overlap_list[info_index])
        info_array.append(repeat_count)

    #Remove diagonal components and finding maximum value
    info_array = remove_diag(info_array)
    max_overall_value = max_val_finder(info_array)
    #Normalising with respsect to maximum value
    if max_overall_value != 0:
        info_array = normalise(info_array, max_overall_value)

    return info_array

def data_to_excel(all_modules, info_array):
    '''
    Writes chosen information into an excel spreadsheet
    Parameters:
        all_modules (dict): Dictionary containing all modules
        info_array (array): Numerical metrics for each module
    '''
    module_codes = list(all_modules.keys())
    df1 = pd.DataFrame(info_array,
                    index=module_codes,
                    columns=module_codes)
    df1.to_excel(excel_writer = "/Users/vanessamadu/Documents/StudentShapers/StudentShapers_code/test.xlsx")

def clustering_score(all_modules, index1, index2):
    '''
    Provides a table of relative scores of 'clustering' of repeated keywords across all modules. Weights divided repeats,
    max repeats and squared sum of repeats at 1:3:3.
    Parameters: 
        all_modules (dict): Dictionary containing all modules
        index1 (int): Takes values 1 or 2
        index2 (int): Takes values 1 or 2
            (1,1): Compares taught keywords 
            (2,2): Compares required keywords
            (1,2): Compares taught keywords in module 1 with required keywords in module 2.
    Returns:
        clustering_matrix (array): Array of relative scores of 'clustering'
    '''
    divided_repeated_keywords = repeat_similarity(all_modules, index1, index2, 1)
    max_repeats = repeat_similarity(all_modules, index1, index2, 2)
    squared_sum = repeat_similarity(all_modules, index1, index2, 3)

    clustering_matrix = []
    for i in range(len(squared_sum)):
        new_row = [(j+3*k+3*l)/7 for j,k,l in zip(divided_repeated_keywords[i], max_repeats[i], squared_sum[i])]
        clustering_matrix.append(new_row)
    return(clustering_matrix)


