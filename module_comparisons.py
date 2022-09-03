import pandas as pd
from search_file import *
from helper_functions import *

########## COMPARISON FUNCTIONS NOT TO BE USED IN ISOLATION ####################

def is_there_overlap(module_dict1, module_dict2, index1, index2):
    '''
    Finds repeated keywords between two modules, given the choice of which types of keywords are compared.
    Module 1 is being compared to module 2.
    Parameters:
        module_dict1 (dict): Module dictionary 1
        module_dict2 (dict): Module dictionary 2
        index1 (int): Chooses which class of keywords/skills to be considered from module 1.
        index2 (int): Chooses which class of keywords/skills to be considered from module 2.
            1: taught keywords
            2: required keywords
            3: taught skills
            4: required skills
    returns:
        similarity_list (list): List of unnormalised similarity scores in the form 
        similarity_list = [number of repeated keywords, repeated keywords/number of chapters repeated across, max number of repeated
        keywords in any section, squared sum of number of repeated keywords in each chapter]
    '''
    keywords_input = module_keywords(module_dict1,index1)
    repeat_counter = 0
    repeated_sections = {}
    repeated_keywords = []

    for i in range(len(keywords_input)):
        if len(keywords_input[i]) == 1:
            keyword = keywords_input[i][0]
            section = in_module(module_dict2,keyword,index2)
            if type(section) == str:
                [repeated_sections,repeated_keywords, repeat_counter] = check_section(section, repeated_sections, repeated_keywords, repeat_counter,keyword)
        else:
            for j in range(len(keywords_input[i])):
                keyword = keywords_input[i][j]
                section = in_module(module_dict2,keyword,index2)
                if type(section) == str:
                    [repeated_sections,repeated_keywords, repeat_counter] = check_section(section, repeated_sections, repeated_keywords, repeat_counter,keyword)
                    break
    squared_sum = 0
    for k in range(len(repeated_sections.values())):
        squared_sum += list(repeated_sections.values())[k]**2

    divided_repeats = 0
    max_repeats = 0
    if len(repeated_sections.keys()) != 0:
        divided_repeats = repeat_counter/len(repeated_sections.keys())
        max_repeats = max(repeated_sections.values())

    return [repeat_counter, divided_repeats , max_repeats, squared_sum, repeated_sections, repeated_keywords]

## GENERATE INFORMATION ARRAYS
def repeat_similarity(all_modules, module_codes, index1, index2, info_index):
    '''
    Compares all modules available in module_dict.json for repeated keywords
    Parameters:
        all_modules (dict): Dictionary containing all modules
        index1 (int): Takes values 1 or 2
        index2 (int): Takes values 1 or 2
            (1,1): Compares taught keywords 
            (2,2): Compares required keywords
            (1,2): Compares taught keywords in module 1 with required keywords in module 2.
            (2,1): Compares required keywords in module 1 with taught keywords in module 2.
        info_index (int): Selects the desired comparison metric from the following options
            0: Number of repeated keywords (normalised wrt largest value)
            1: Number of repeated keywords/number of chapters spread across (normalised wrt largest value)
            2: Maximum number of repeated keywords in any section in module 2 (normalised wrt largest value)
            3: Squared sum of number of repeated keywords in each chapter in modules 2 (normalised wrt largest value)
    Returns:
        info (array): Returns an array where component ij is the the requested comparison information 
        for module i and module j.
    '''
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

def clustering_score(all_modules, module_codes, index1, index2):
    '''
    Provides a table of relative scores of 'clustering' of repeated keywords across all modules. Repeats divided repeats,
    max repeats and squared sum of repeats at 1:3:3.
    Parameters: 
        all_modules (dict): Dictionary containing all modules
        index1 (int): Takes values 1 or 2
        index2 (int): Takes values 1 or 2
            (1,1): Compares taught keywords 
            (2,2): Compares required keywords
            (1,2): Compares taught keywords in module 1 with required keywords in module 2.
            (2,1): Compares required keywords in module 1 with taught keywords in module 2.
    Returns:
        clustering_matrix (array): Array of relative scores of 'clustering'
    '''
    divided_repeated_keywords = repeat_similarity(all_modules, module_codes, index1, index2, 1)
    max_repeats = repeat_similarity(all_modules, module_codes, index1, index2, 2)
    squared_sum = repeat_similarity(all_modules, module_codes, index1, index2, 3)

    clustering_matrix = []
    for i in range(len(squared_sum)):
        new_row = [(j+3*k+3*l)/7 for j,k,l in zip(divided_repeated_keywords[i], max_repeats[i], squared_sum[i])]
        clustering_matrix.append(new_row)
    return(clustering_matrix)

## IDENTIFY MODULES WITH SIMILARITY ABOVE THRESHOLD

def pair_finder(all_modules, module_codes, info_array, min_val, max_val=1):
    '''
    Look for all the module pairs that have a similarity score greater than min_val but less than max_val
    Parameters: 
        all_modules (dict): Dictionary containing all modules
        info_array (array): Either array containing normalised number of keywords or array containing
                            the normalised clustering score.
        min_val (float): Threshold lower value for two modules to be considered similar. Values between 0 and 1 (inclusive)
        max_val (float) (optional): Threshold upper value for two modules to be considered weakly similar. Value between 0 and 1 (inclusive)
        Default value is 1. 
        **max_val is only worth using if looking for small amounts over overlap between modules**
    Returns: 
        pairs (list): List of module pairs with similarity score above threshold.
    '''
    pairs = []
    length = len(info_array)
    for i in range(length):
        for j in range(length):
            if info_array[i][j] > min_val and info_array[i][j] <= max_val:
                pairs.append([module_codes[i],module_codes[j]])
    return pairs

## PRINT USEFUL INFORMATION
def keyword_repeat_results(all_modules, pairs, index1, index2):
    '''
    Prints the results for pairs of modules that exceed the similarity score threshold, stating exactly how
    **This only tells us about repeated keywords and shouldn't be used in isolation as index1 and index2 need to be the same as those
    that were used to generate the info array.**
    **THIS FUNCTION IS MEANT TO BE USED ONLY WHEN MAX_VAL == 1 IS AN ARGUMENT FOR THE PAIR_FINDER FUNCTION**
    Parameters:
        all_modules (dict): Dictionary containing all modules
        pairs (list): List of module pairs that exceed similarity score threshold
        index1 (int): Takes the values 1 or 2
        index2 (int): Takes the values 1 or 2
            (1,1): Compares taught keywords 
            (2,2): Compares required keywords
            (1,2): Compares taught keywords in module 1 with required keywords in module 2.
            (2,1): Compares required keywords in module 1 with taught keywords in module 2.
    '''
    if index1 == index2:
        pairs = remove_duplicate(pairs)
    for i in range(len(pairs)):
        module1 = pairs[i][0]
        module2 = pairs[i][1]

        if index1 ==1 and index2==1:
            print(' '.join([code_to_name(all_modules, module1)] + ['may be similar to'] + [code_to_name(all_modules, module2)]))
        elif index1 == 1 and index2 == 2:
            print(' '.join([code_to_name(all_modules, module1)] + ['may be a good module to take for'] + [code_to_name(all_modules,module2)]))
        elif index1 == 2 and index2 == 2:
            print(' '.join([code_to_name(all_modules, module1)] + ["may have the same 'prerequisites' as"] + [code_to_name(all_modules, module2)]))
        elif index1 == 2 and index2 == 1:
            print(' '.join([code_to_name(all_modules, module2)] + ['may be a good module to take for'] + [code_to_name(all_modules,module1)]))

def weak_keyword_repeat_results(all_modules, pairs, index1, index2):
    '''
    Prints the results for pairs of modules that exceed the similarity score threshold, stating exactly how
    **This only tells us about repeated keywords and shouldn't be used in isolation as index1 and index2 need to be the same as those
    that were used to generate the info array.**
    **THIS FUNCTION IS MEANT TO BE USED ONLY WHEN MAX_VAL != 1 IS AN ARGUMENT FOR THE PAIR_FINDER FUNCTION**
    Parameters:
        all_modules (dict): Dictionary containing all modules
        pairs (list): List of module pairs that exceed similarity score threshold
        index1 (int): Takes the values 1 or 2
        index2 (int): Takes the values 1 or 2
            (1,1): Compares taught keywords 
            (2,2): Compares required keywords
            (1,2): Compares taught keywords in module 1 with required keywords in module 2.
            (2,1): Compares required keywords in module 1 with taught keywords in module 2.
    '''
    if index1 == index2:
        pairs = remove_duplicate(pairs)
    for i in range(len(pairs)):
        module1 = pairs[i][0]
        module2 = pairs[i][1]
        
        if index1 ==1 and index2==1:
            print(' '.join([code_to_name(all_modules, module1)] + ['may have a small amount of similarity to'] + [code_to_name(all_modules, module2)]))
        elif index1 == 1 and index2 == 2:
            print(' '.join([code_to_name(all_modules, module1)] + ['may be have a small number of useful concepts for'] + [code_to_name(all_modules,module2)]))
        elif index1 == 2 and index2 == 2:
                print(' '.join([code_to_name(all_modules, module1)] + ["may have a small number of the same 'prerequisites' as"] + [code_to_name(all_modules, module2)]))
        elif index1 == 2 and index2 == 1:
                print(' '.join([code_to_name(all_modules, module2)] + ['may be have a small number of useful concepts for'] + [code_to_name(all_modules,module1)]))

def clustering_results(all_modules, pairs, index1, index2):
    '''
    Prints the results for pairs of modules that exceed the clustering similarity score threshold, stating exactly how
    **This only tells us about clustering of keywords and shouldn't be used in isolation as index1 and index2 need to be the same as those
    that were used to generate the info array.**
    **THIS FUNCTION IS MEANT TO BE USED ONLY WHEN MAX_VAL == 1 IS AN ARGUMENT FOR THE PAIR_FINDER FUNCTION**
    Parameters:
        all_modules (dict): Dictionary containing all modules
        pairs (list): List of module pairs that exceed similarity score threshold
        index1 (int): Takes the values 1 or 2
        index2 (int): Takes the values 1 or 2
            (1,1): Compares taught keywords 
            (2,2): Compares required keywords
            (1,2): Compares taught keywords in module 1 with required keywords in module 2.
            (2,1): Compares required keywords in module 1 with taught keywords in module 2.
    '''
    if index1 == index2:
        pairs = remove_duplicate(pairs)
    for i in range(len(pairs)):
        module1 = pairs[i][0]
        module2 = pairs[i][1]

        if index1 ==1 and index2==1:
            print(' '.join(['The similarity in'] + [code_to_name(all_modules, module1)] + ['and'] + [code_to_name(all_modules, module2)] + ['is highly clustered in'] + [code_to_name(all_modules, module2)] ))
        elif index1 == 1 and index2 == 2:
            print(' '.join(['The prerequisites for'] + [code_to_name(all_modules, module2)] + ['found in'] + [code_to_name(all_modules, module1)] + ['are highly clustered in'] + [code_to_name(all_modules, module2)] ))
        elif index1 == 2 and index2 == 2:
            print(' '.join(['The required keyword similarity in'] +[code_to_name(all_modules, module1)] + ['and'] + [code_to_name(all_modules, module2)] + ['is highly clustered in'] + [code_to_name(all_modules, module2)] ))
        elif index1 == 2 and index2 == 1:
            print(' '.join(['The prerequisites for'] + [code_to_name(all_modules, module1)] + ['found in'] + [code_to_name(all_modules, module2)] + ['are highly clustered in'] + [code_to_name(all_modules, module2)] ))

def weak_clustering_results(all_modules, pairs, index1, index2):
    '''
    Prints the results for pairs of modules that exceed the clustering similarity score threshold, stating exactly how
    **This only tells us about clustering of keywords and shouldn't be used in isolation as index1 and index2 need to be the same as those
    that were used to generate the info array.**
    **THIS FUNCTION IS MEANT TO BE USED ONLY WHEN MAX_VAL != 1 IS AN ARGUMENT FOR THE PAIR_FINDER FUNCTION**
    Parameters:
        all_modules (dict): Dictionary containing all modules
        pairs (list): List of module pairs that exceed similarity score threshold
        index1 (int): Takes the values 1 or 2
        index2 (int): Takes the values 1 or 2
            (1,1): Compares taught keywords 
            (2,2): Compares required keywords
            (1,2): Compares taught keywords in module 1 with required keywords in module 2.
            (2,1): Compares required keywords in module 1 with taught keywords in module 2.
    '''
    if index1 == index2:
        pairs = remove_duplicate(pairs)
    for i in range(len(pairs)):
        module1 = pairs[i][0]
        module2 = pairs[i][1]

        if index1 ==1 and index2==1:
            print(' '.join(['The similarity in'] + [code_to_name(all_modules, module1)] + ['and'] + [code_to_name(all_modules, module2)] + ['is weakly clustered in'] + [code_to_name(all_modules, module2)] ))
        elif index1 == 1 and index2 == 2:
            print(' '.join(['The prerequisites for'] + [code_to_name(all_modules, module2)] + ['found in'] + [code_to_name(all_modules, module1)] + ['are weakly clustered in'] + [code_to_name(all_modules, module2)] ))
        elif index1 == 2 and index2 == 2:
            print(' '.join(['The required keyword similarity in'] +[code_to_name(all_modules, module1)] + ['and'] + [code_to_name(all_modules, module2)] + ['is weakly clustered in'] + [code_to_name(all_modules, module2)] ))
        elif index1 == 2 and index2 == 1:
            print(' '.join(['The prerequisites for'] + [code_to_name(all_modules, module1)] + ['found in'] + [code_to_name(all_modules, module2)] + ['are weakly clustered in'] + [code_to_name(all_modules, module2)] ))

############################### COMPARE ALL MODULES TO EACH OTHER #########################################

def similarity_all_modules(all_modules, module_codes,index1, index2, repeat_or_cluster, min_val, write_destination, max_val=1):
    '''
    Compares desired keywords across all modules for similarity, prints the modules that have a score above
    the threshold and exports all the scores into a excel file.
    Parameters:
        all_modules (dict): Dictionary containing all the modules
        index1 (int): Takes the values 1 or 2
        index2 (int): Takes the values 1 or 2
            (1,1): Compares taught keywords 
            (2,2): Compares required keywords
            (1,2): Compares taught keywords in module 1 with required keywords in module 2.
            (2,1): Compares required keywords in module 1 with taught keywords in module 2.
        repeat_or_cluster (int): Takes the values 1 or 2
            1: Return results for repeated keywords
            2: Return results for clustering of repeated keywords
        min_val (float): Threshold value for two modules to be considered similar. Value between 0 and 1 (inclusive)
        write_destination (str): Path to xslx file to write to
        max_val (float) (optional): Threshold upper value for two modules to be considered weakly similar. Value between 0 and 1 (inclusive)
        Default value is 1. 
        **max_val is only worth using if looking for small amounts over overlap between modules**
        
    '''
    if repeat_or_cluster == 1:
        info_array = repeat_similarity(all_modules, module_codes, index1, index2, 0)
    elif repeat_or_cluster == 2:
        info_array = clustering_score(all_modules, module_codes, index1, index2)
    
    data_to_excel(all_modules, module_codes, info_array, write_destination)
    if max_val != 1:
        pairs = pair_finder(all_modules, module_codes, info_array, min_val, max_val)
    else:
        pairs = pair_finder(all_modules, module_codes, info_array, min_val)

    if repeat_or_cluster == 1:
        if max_val == 1:
            keyword_repeat_results(all_modules, pairs, index1, index2)
        else:
            weak_keyword_repeat_results(all_modules, pairs, index1, index2)

    elif repeat_or_cluster == 2: 
        if max_val ==1:
            clustering_results(all_modules, pairs, index1, index2)
        else:
            weak_clustering_results(all_modules, pairs, index1, index2)
