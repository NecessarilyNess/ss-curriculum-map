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

def data_to_excel(all_modules, module_codes, info_array, write_destination):
    '''
    Writes chosen information into an excel spreadsheet
    Parameters:
        all_modules (dict): Dictionary containing all modules
        info_array (array): Numerical metrics for each module
        write_destination (str): Path to xslx file to write to
    '''
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

def keyword_list_update(i, j, keyword_list, dataframe):
    '''
    Given indices that specify a component in a module dataframe, appends they keyword(s)/skill(s)
    contained in that component.
    Parameters:
        i (int): Index for position within the section (column)
        j (int): Index belonging to the section number
        keyword_list (list): List of desired keywords 
        dataframe (dataframe): pandas dataframe built from csv file
    Returns:
        keyword_list (list): Input list with index keyword(s) appended.
    '''
    if '// ' in dataframe['Section '+str(j)][i]:
        keyword_list.append(multiple_names(whitespace_cleaner(dataframe['Section '+str(j)][i])))
    else:
        keyword_list.append([whitespace_cleaner(dataframe['Section '+str(j)][i])])
    return keyword_list

############ FILTER FUNCTIONS ##################

def which_year(code):
    '''
    Returns the year a module is taught in from the module code.
    Parameters:
        code (str): Module code
    Returns: 
        year (int): Year the module is taught in (1,2,3 or 4)
    '''
    year = int(list(code)[4]) - 3
    return year

def year_filter(all_modules, list_of_years = [1,2,3,4]):
    '''
    Given a list of years, returns the list of modules taught in those years
    Parameters: 
        all_modules (dict): Dictionary containing all modules
        list_of_years (list): List of year groups to include. Default value is [1,2,3,4]
    Returns:
        filtered_modules (list): Modules taught in the years specified
    '''
    module_codes = list(all_modules.keys())
    filtered_modules = [module for module in module_codes if which_year(module) in list_of_years]
    return filtered_modules

def which_section(all_modules, code):
    '''
    Returns the mathematical section that a module belongs to (pure, applied, statistics)
    Parameters:
        all_modules (dict): Dictionary containing all modules
        code (str): Module code
    Returns:
        section (str): Mathematical section the module belongs to
    '''
    section = all_modules[code]['module information'][5][0]
    return section

def section_filter(all_modules, list_of_sections = ['pure', 'applied', 'statistics']):
    '''
    Given a list of (mathematical) sections, returns the list of modules taught from those sections
    Parameters: 
        all_modules (dict): Dictionary containing all modules
        list_of_sections (list): List of sections to include. Default value is ['pure', 'applied', 'statistics']
    Returns:
        filtered_modules (list): Modules taught in the sections specified
    '''
    module_codes = list(all_modules.keys())
    filtered_modules = [module for module in module_codes if which_section(all_modules, module) in list_of_sections]
    return filtered_modules

def year_and_section_filter(all_modules, list_of_years = [1,2,3,4], list_of_sections = ['pure', 'applied', 'statistics']):
    '''
    Given lists of years and (mathematical) sections, returns the list of modules taught from those years and sections
    Parameters: 
        all_modules (dict): Dictionary containing all modules
        list_of_years (list): List of year groups to include. Default value is [1,2,3,4]
        list_of_sections (list): List of sections to include. Default value is ['pure', 'applied', 'statistics']
    Returns:
        filtered_modules (list): Modules taught in the years and sections specified
    '''
    year_filtered_modules = year_filter(all_modules, list_of_years)
    section_filtered_modules = section_filter(all_modules, list_of_sections)
    filtered_modules = [module for module in year_filtered_modules if module in section_filtered_modules]
    return filtered_modules