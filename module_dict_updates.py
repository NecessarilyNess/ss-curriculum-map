import json
import os
from helper_functions import *


# Load all the modules from json file
with open('./module_dict.json', 'r') as openfile:
    all_modules = json.load(openfile)

# Get a list of the csv files that are in the folder
module_csv = os.listdir('/Users/vanessamadu/Documents/StudentShapers/StudentShapers_code/module_csv_files')
module_csv.remove('.DS_Store')

# Function to add module to json_file
def dict_maker(module_csv_path, all_modules):
    '''
    Takes module information from a csv file and formats as a python dictionary of the form 
    Module_name = {'module information':['module name', 'code',year,term,number of sections],
    'section_number': ['section_title', taught_keywords, required_keywords, taught_skills, required_skills]}
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
            if type(dataframe['Section '+str(j)][i]) == str:
                #Deal with potential for mutliple names for the same term
                if '// ' in dataframe['Section '+str(j)][i]:
                    required_skills.append(multiple_names(whitespace_cleaner(dataframe['Section '+str(j)][i])))
                else:
                    required_skills.append([whitespace_cleaner(dataframe['Section '+str(j)][i])])
            else:
                break
        module_dict['section_'+str(j)].append(required_skills)

    module_code = module_dict['module information'][1][0]
    all_modules[module_code] = module_dict
    write_to_json('./module_dict.json', all_modules)

# Add all modules into the json file
for module in module_csv:
    module_csv_path = 'module_csv_files/%s'%module
    dict_maker(module_csv_path, all_modules)

