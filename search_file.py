import json
from data_structure import *
#Load all modules
with open('module_dict.json') as json_file:
    all_modules = json.load(json_file)

'''
I need functions that do the following
- Extracts taught keywords from a module DONE
- Extracts required keywords from a module DONE
- Extracts taught skills DONE
- Extracts required skills DONE
- Returns which section a keyword/skill is from DONE
- Is the keyword in the other list DONE
- Keeps track and count of what is repeated DONE
- Counting the number of skills DONE
- Write a function that takes all the modules in the csv folder and loads them into the json file
'''
######################### EXTRACTION FUNCTIONS ##############################

def keywords(module_dict, index):
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

###################### HELPER FUNCTIONS ########################

def is_repeated(module_dict, keyword, index):
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
    keyword = whitespace_cleaner(keyword)
    num_of_sections = int(module_dict['module information'][4][0])

    for i in range(1,num_of_sections+1):
        # Specify which of the lists to search in
        where_to_look = module_dict['section_'+str(i)][index]
        for j in range(len(where_to_look)):
            if keyword in where_to_look[j]:
                return 'section_'+str(i)
    return False

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
    skill_list = keywords(module_dict,index)
    for skill in skill_list:
        if skill[0] in skills.keys():
            skills[skill[0]]+=1
        else:
            skills[skill[0]]=1
    return skills

########################## THE BIG FUNCTIONS ###############################

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
    keywords_input = keywords(module_dict1,index1)
    repeat_counter = 0
    repeated_sections = {}
    repeated_keywords = []

    for i in range(len(keywords_input)):
        if len(keywords_input[i]) == 1:
            keyword = keywords_input[i][0]
            section = is_repeated(module_dict2,keyword,index2)
            if type(section) == str:
                if section in repeated_sections.keys():
                    repeated_sections[section]+=1
                else: 
                    repeated_sections[section]=1
                repeat_counter+=1
                repeated_keywords.append(keyword)
        else:
            for j in range(len(keywords_input[i])):
                keyword = keywords_input[i][j]
                section = is_repeated(module_dict2,keyword,index2)
                if type(section) == str:
                    if section in repeated_sections.keys():
                        repeated_sections[section]+=1
                    else: 
                        repeated_sections[section]=1
                    repeat_counter+=1
                    repeated_keywords.append(keyword)
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

        
