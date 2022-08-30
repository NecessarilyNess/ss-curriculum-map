from module_dict_updates import *
from helper_functions import *
from module_dict_updates import *

## SEARCH FOR KEYWORDS IN A MODULE
def module_keywords(module_dict, index):
    '''
    Extracts all of the desired keywords/skills in a module where each 'keyword' is stored as a list.
    Parameters: 
        module_dict (dict): Module dictionary
        index (int): Takes the values 1,2,3, or 4 to determine which list to 
            extract
            1: taught keywords
            2: required keywords
            3: taught skills
            4: required skills
    Returns:
        keywords (list): List of desired keywords/skills
    '''
    num_of_sections = int(module_dict['module information'][4][0])
    keywords = []
    for i in range(1,num_of_sections+1):
        keywords+=(module_dict['section_'+str(i)][index])
    return(keywords)

def in_module(module_dict, keyword, index):
    '''
    Determines if a keyword/skill is in a module and if it is, returns where
    Parameters:
        module_dict (dict): Module dictionary
        keyword (str): Keyword/skill to be search for
        index (int): Takes the values 1,2,3, or 4 to determine which list to 
            search for the keyword/skill in:
            1: taught keywords
            2: required keywords
            3: taught skills
            4: required skills
    Returns: 
        Either: section_number (str): Section the keyword/skill is in
        False (bool): False (the term is not in the list)
    '''
    keyword = whitespace_cleaner(close_quote_cleaner(keyword))
    num_of_sections = int(module_dict['module information'][4][0])

    for i in range(1,num_of_sections+1):
        # Specify which of the lists to search in
        where_to_look = module_dict['section_'+str(i)][index]
        for j in range(len(where_to_look)):
            if keyword in close_quote_cleaner(where_to_look[j]):
                return 'section_'+str(i)
    return False

## SKILL INFORMATION

def skill_importance(module_dict, index):
    '''
    Identifies the frequency with which skills appear in a module.
    Paramters: 
        module_dict (dict): Module dictionary
        index (int): Takes the value 3 or 4 to determine which skills to consider
            3: taught skills
            4: required skills
    Returns:
        skills (dict): Dictionary containing skills and the number of chapters it
        appears in
    '''
    skills = {}
    skill_list = module_keywords(module_dict,index)
    for skill in skill_list:
        if skill[0] in skills.keys():
            skills[skill[0]]+=1
        else:
            skills[skill[0]]=1
    return skills

        
