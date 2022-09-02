import json
import os
from helper_functions import *

## LOAD ALL CSV FILES IN MODULE CSV DIRECTORY INTO A DICTIONARY
def all_modules_dict(json_relative_path, module_csv_directory_full_path, modules_csv_directory_percent_s):
    '''
    Loads all of the csv files in the module_csv_files directory into a dictionary.
    Parameters:
        json_relative_path (str): Relative path to json file. If its in your current directory then './name.json'
        module_csv_directory_full_path (str): Full path to folder containing the csv files.
        modules_csv_directory_percent_s (str): Relative path to folder containing csv files, followed by /%s i.e './module_csv_files/%s'
    Returns: 
        all_modules (dict): Dictionary containing all modules
    '''
    # Load all the modules from json file
    with open(json_relative_path, 'r') as openfile:
        all_modules = json.load(openfile)

    # Get a list of the csv files that are in the folder
    module_csv = os.listdir(module_csv_directory_full_path)
    module_csv.remove('.DS_Store') #If you've got a Mac
   
    # Add all modules into the json file
    for module in module_csv:
        module_csv_path = modules_csv_directory_percent_s%module
        dict_maker(module_csv_path, all_modules)

    return all_modules

#### ADDS AN INDIVIDUAL MODULE TO THE JSON FILE
def dict_maker(module_csv_path, all_modules):
    '''
    Takes module information from a csv file and formats as a python dictionary of the form 
    Module_name = {'module information':['module name', 'code',year,term,number of sections],
    'section_number': ['section_title', taught_keywords, required_keywords, taught_skills, required_skills]}
    Writes to a json file containing all modules.
    
    Parameters:
        module_csv_path (str): Path to the module csv file. Expected syntax 'module_csv_files/Module.csv' 
        all_modules (dict): Dictionary containing all modules
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
                taught_keywords = keyword_list_update(i, j, taught_keywords, dataframe)
            else:
                req_start = i
                break
        module_dict['section_'+str(j)].append(taught_keywords)

        #Identify 'required' keywords
        required_keywords = []
        for i in range(req_start+1, len_of_section):
            if dataframe['Section '+str(j)][i] != 'Skills (Taught)':
                required_keywords = keyword_list_update(i, j, required_keywords, dataframe)
            else:
                taught_skills_start = i
                break
        module_dict['section_'+str(j)].append(required_keywords)

        #Identify taught skills
        taught_skills = []
        for i in range(taught_skills_start +1, len_of_section):
            if dataframe['Section '+str(j)][i] != 'Skills (Prerequisite)':
                taught_skills = keyword_list_update(i, j, taught_skills, dataframe)
            else:
                req_skills_start = i
                break   
        module_dict['section_'+str(j)].append(taught_skills)

        #Identify required skills  
        required_skills = []
        for i in range(req_skills_start+1, len_of_section):
            if type(dataframe['Section '+str(j)][i]) == str:
                required_skills = keyword_list_update(i, j, required_skills, dataframe)
            else:
                break
        module_dict['section_'+str(j)].append(required_skills)

    module_code = module_dict['module information'][1][0]
    all_modules[module_code] = module_dict
    write_to_json('./module_dict.json', all_modules)
