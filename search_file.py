import json

#Load all modules
with open('module_dict.json') as json_file:
    all_modules = json.load(json_file)

'''
I need functions that do the following
- Extracts taught keywords from a module DONE
- Extracts required keywords from a module DONE
- Extracts taught skills DONE
- Extracts required skills DONE
- Returns which section a keyword/skill is from
- Is the keyword in the other list
- Keeps track and count of what is repeated
- Counting the number of skills
'''
######################### EXTRACTION FUNCTIONS ##############################

def taught_keywords(module_dict):
    '''
    Extracts all of the taught keywords in a module where each 'keyword' is stored as a list.
    Parameters: 
        module_dict (dict): Module dictionary
    Returns:
        taught_keywords (list): List of taught keywords
    '''
    num_of_sections = int(module_dict['module information'][4][0])
    taught_keywords = []
    for i in range(1,num_of_sections+1):
        taught_keywords+=(module_dict['section_'+str(i)][1])
    return(taught_keywords)

def required_keywords(module_dict):
    '''
    Extracts all of the prerequisite keywords in a module where each 'keyword' is stored as a list.
    Parameters: 
        module_dict (dict): Module dictionary
    Returns:
        required_keywords (list): List of prerequisite keywords
    '''
    num_of_sections = int(module_dict['module information'][4][0])
    required_keywords = []
    for i in range(1,num_of_sections+1):
        required_keywords+=(module_dict['section_'+str(i)][2])
    return(required_keywords)

def taught_skills(module_dict):
    '''
    Extracts all of the taught skills in a module where each 'skill' is stored as a list.
    Parameters: 
        module_dict (dict): Module dictionary
    Returns:
        taught_skills (list): List of taught skills
    '''
    num_of_sections = int(module_dict['module information'][4][0])
    taught_skills = []
    for i in range(1,num_of_sections+1):
        taught_skills+=(module_dict['section_'+str(i)][3])
    return(taught_skills)

def required_skills(module_dict):
    '''
    Extracts all of the required skills in a module where each 'skill' is stored as a list.
    Parameters: 
        module_dict (dict): Module dictionary
    Returns:
        required_skills (list): List of required skills
    '''
    num_of_sections = int(module_dict['module information'][4][0])
    required_skills = []
    for i in range(1,num_of_sections+1):
        required_skills+=(module_dict['section_'+str(i)][4])
    return(required_skills)