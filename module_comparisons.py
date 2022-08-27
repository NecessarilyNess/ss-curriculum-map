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

def data_to_excel(all_modules,index1, index2, info_index):
    info_array = repeat_similarity(all_modules, index1, index2, info_index)
    module_codes = list(all_modules.keys())
    df1 = pd.DataFrame(info_array,
                    index=module_codes,
                    columns=module_codes)
    df1.to_excel(excel_writer = "/Users/vanessamadu/Documents/StudentShapers/StudentShapers_code/test.xlsx")


