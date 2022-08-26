import json
import pandas as pd
######### HELPER FUNCTIONS ##############
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

############################################

def dict_maker(module_csv_path):
    '''
    Takes module information from a csv file and formats as a python dictionary of the form 
    Module_name = {'module information':['module name', 'code',year,term,number of sections],
    'section_number': ['section_title', taught_keywords_dict, required_keywords_dict, taught_skills_dict, required_skills_dict]}
    Writes to a json file containing all modules.
    
    Parameters:
        module_csv_path (str): Path to the module csv file. Expected syntax 'module_csv_files/Module.csv' 
    '''
    # Import module from csv file
    df = pd.read_csv (r'%s'%module_csv_path)
    dataframe = {}
    for (columnName, columnData) in df.iteritems():
        dataframe[columnName] = list(columnData.values)

    num_of_sections = int(dataframe['Module Information'][4])

    #Initialising
    module_dict = {}

    #Get module information
    info_length = len(dataframe['Module Information'])
    module_dict['module information'] = []
    for i in range(0,info_length):
        if type(dataframe['Module Information'][i]) == str:
            module_dict['module information'].append([whitespace_cleaner(dataframe['Module Information'][i])])
        else:
            break

    #Add sections and their corresponding keywords
    for j in range(1, num_of_sections+1):
        module_dict['section_'+str(j)] = []
        #Add section name
        module_dict['section_'+str(j)].append(whitespace_cleaner(dataframe['Section '+str(j)][0]))
        #Identify taught keywords
        taught_keywords = []
        len_of_section = len(dataframe['Section '+str(j)])
        for i in range(1,len_of_section):
            if dataframe['Section '+str(j)][i] != 'Keywords (Prerequisite)':
                #Deal with potential for mutliple names for the same term
                if '// ' in dataframe['Section '+str(j)][i]:
                    taught_keywords.append(multiple_names(whitespace_cleaner(dataframe['Section '+str(j)][i])))
                else:
                    taught_keywords.append([whitespace_cleaner(dataframe['Section '+str(j)][i])])
            else:
                req_start = i
                break
        module_dict['section_'+str(j)].append(taught_keywords)
        #Identify 'required' keywords
        required_keywords = []
        for i in range(req_start+1, len_of_section):
            if dataframe['Section '+str(j)][i] != 'Skills (Taught)':
                #Deal with potential for mutliple names for the same term
                if '// ' in dataframe['Section '+str(j)][i]:
                    required_keywords.append(multiple_names(whitespace_cleaner(dataframe['Section '+str(j)][i])))
                else:
                    required_keywords.append([whitespace_cleaner(dataframe['Section '+str(j)][i])])
            else:
                taught_skills_start = i
                break
        module_dict['section_'+str(j)].append(required_keywords)
        #Identify taught skills
        taught_skills = []
        for i in range(taught_skills_start +1, len_of_section):
            if dataframe['Section '+str(j)][i] != 'Skills (Prerequisite)':
                #Deal with potential for mutliple names for the same term
                if '// ' in dataframe['Section '+str(j)][i]:
                    taught_skills.append(multiple_names(whitespace_cleaner(dataframe['Section '+str(j)][i])))
                else:
                    taught_skills.append([whitespace_cleaner(dataframe['Section '+str(j)][i])])
            else:
                req_skills_start = i
                break   
        module_dict['section_'+str(j)].append(taught_skills)
        #Identify required skills  
        required_skills = []
        for i in range(req_skills_start+1, len_of_section):
            if dataframe['Section '+str(j)][i] == str:
                #Deal with potential for mutliple names for the same term
                if '// ' in dataframe['Section '+str(j)][i]:
                    required_skills.append(multiple_names(whitespace_cleaner(dataframe['Section '+str(j)][i])))
                else:
                    required_skills.append([whitespace_cleaner(dataframe['Section '+str(j)][i])])
            else:
                break
        module_dict['section_'+str(j)].append(required_skills)

    module_code = module_dict['module information'][1][0]


    write_to_json('./module_dict.json', {module_code : module_dict})
