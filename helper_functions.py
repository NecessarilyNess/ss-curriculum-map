import json
import pandas as pd

def write_to_json(file_path, module_dict):
    '''
    Updates the json dictionary.
    Parameters:
        file_path (str): The filepath for the json file.
        module_dict (dict): Module dictionary
    '''
    with open(file_path, "w") as outfile:
        json.dump(module_dict, outfile)

def multiple_names(string_list):
    '''
    Separates different names for the same idea. Expected syntax 'term// term'
    Parameters:
        string_list (str): Names separated by //
    Returns:
        new_list (list): Names for the same idea as a list.
    '''
    num_of_splits = string_list.count('// ') 
    new_list = string_list.split('// ', num_of_splits)
    return new_list

def whitespace_cleaner(term):
    '''
    Removes all duplicate, trailing and leading whitespaces. Also makes all text lower case.
    Parameters:
        term (str): A term as a string.
    Returns:
        term (str): Term with duplicate, trailing and leading whitespaces removed.
    '''
    return(" ".join((term.lower()).split()))

def close_quote_cleaner(term):
    '''
    Replaces the unicode character "\u2019" with "'" for terms in a list.
    Parameters: 
        term (str): term
    Returns:
        term (str): Same term with "\u2019" replaced by "'"
    '''
    if "\u2019" in term:
        term = term.replace("\u2019", "'")
        return term
    return term

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

def remove_duplicate(pairs):
    '''
    Given a list of unordered module pairs, removes pairs containing the same two modules.
    Parameters:
        pairs (list): List of unordered module pairs 
    Returns:
        pairs (list): List of module pairs with duplicates removed
    '''
    for i in range(len(pairs)):
        pairs[i] = set(pairs[i])
    for i in range(len(pairs)):
        if pairs.count(pairs[i]) != 1:
            pairs[i] = 'dup'
    pairs = [list(pair) for pair in pairs if pair != 'dup']
    return pairs 

def code_to_name(all_modules, code):
    '''
    Given a module code, returns the name of the module
    Paramters:
        code (str): Module code
    Returns:
        module_name (str): Module name
    '''
    module = all_modules[code]
    module_name = module["module information"][0][0]
    return module_name

def data_to_excel(all_modules, info_array, write_destination):
    '''
    Writes chosen information into an excel spreadsheet
    Parameters:
        all_modules (dict): Dictionary containing all modules
        info_array (array): Numerical metrics for each module
        write_destination (str): Path to xslx file to write to
    '''
    module_codes = list(all_modules.keys())
    df1 = pd.DataFrame(info_array,
                    index=module_codes,
                    columns=module_codes)
    df1.to_excel(excel_writer = write_destination)

def check_section(section, repeated_sections, repeated_keywords, repeat_counter,keyword):
    '''
    Given that a keyword is in a section, returns appropriate changes to counting variables
    Parameters:
        section (str): The section a keyword is found in
        repeated_sections (dict): Dictionary counting the number of times each repeated section contains a repeat.
        repeated_keywords (list): List containing the keywords that have been repeated
        repeat_counter (int): Number of repeated keywords
        keyword (str): Keyword from a module
    Returns:
        repeated_sections (dict): same as input but with the dictionary counter value of section the keyword is from +1
        repeated_keywords (list): same as input with keyword appended
        repeat_counter (int): previous value +1
    '''
    if section in repeated_sections.keys():
        repeated_sections[section]+=1
    else: 
        repeated_sections[section]=1
    repeat_counter+=1
    repeated_keywords.append(keyword)
    return [repeated_sections,repeated_keywords, repeat_counter]