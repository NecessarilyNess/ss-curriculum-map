#After reading the csv file
#everything needs to be made lower case and the white spaces need to be cleaned up
#For different versions of the same term, separate with //
#Split the list into each of it's key elements

#Applied_Complex_Analysis = {"module information":["MATH60006",2,1], "section_1":["Review of Complex Numbers",taught_keywords,required_keywords,taught_skills,required_skills]}

#taught_keywords = {"conformality":[,0], "linear mapping":[,0], "circle property":[,0], "critical points":[,0], "inverse mappings":[,0], "power function mapping":[,0], "linear fractional transformation":[[Mobius transformation, Bilinear transformation],0], "complex infinity":[,0], "Joukovskii transformation":[,0], "Schwarz-Christoffel transformation":[,0], "Laplace's equation":[,0], "Dirichlet boundary condition":[,0], "Neumann boundary condition":[,0], "ideal flow past a flat plate":[,0]}
#required_keywords = {}
#taught_skills = {}
#required_skills = {}
#Repeated terms will just have the number written next to the term.
#Deal with cases
'''
Mark 1 of data structure:
Module_name = {'module information':['code',year,term,number of sections] ,'section_number': ['section_title', taught_keywords_dict, required_keywords_dict, taught_skills_dict, required_skills_dict]}
'''
#import csv
import pandas as pd
df = pd.read_csv (r'./Modules.csv')
dataframe = {}
for (columnName, columnData) in df.iteritems():
    dataframe[columnName] = list(columnData.values)

num_of_sections = int(dataframe['Module Information'][4])
module_dict = {}

#Get Module information
info_length = len(dataframe['Module Information'])
module_dict['module information'] = []
for i in range(1,info_length):
    if type(dataframe['Module Information'][i]) == str:
        module_dict['module information'].append(dataframe['Module Information'][i])
    else:
        break

for j in range(1, num_of_sections):
    module_dict['section_'+str(j)] = []
    #Add module name
    module_dict['section_'+str(j)].append(dataframe['Section '+str(j)][0])
    #Identify taught keywords
    taught_keywords = []
    len_of_section = len(dataframe['Section '+str(j)])
    for i in range(1,len_of_section):
        if dataframe['Section '+str(j)][i] != 'Keywords (Prerequisite)':
            #Deal with potential for mutliple names for the same term
            if '// ' in dataframe['Section '+str(j)][i]:
                taught_keywords.append(multiple_names(dataframe['Section '+str(j)][i]))
            else:
                taught_keywords.append([dataframe['Section '+str(j)][i]])
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
                required_keywords.append(multiple_names(dataframe['Section '+str(j)][i]))
            else:
                required_keywords.append([dataframe['Section '+str(j)][i]])
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
                taught_skills.append(multiple_names(dataframe['Section '+str(j)][i]))
            else:
                taught_skills.append([dataframe['Section '+str(j)][i]])
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
                required_skills.append(multiple_names(dataframe['Section '+str(j)][i]))
            else:
                required_skills.append([dataframe['Section '+str(j)][i]])
        else:
            break
    module_dict['section_'+str(j)].append(required_skills)

#Function to separate AKA
def multiple_names(string_list):
    num_of_splits = string_list.count('// ') 
    new_list = string_list.split('// ', num_of_splits)
    return new_list