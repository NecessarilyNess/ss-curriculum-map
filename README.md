# StudentShapers Curriculum Mapping Project
## Table of Contents
1. [General Information](#general-information)
2. [Prerequisites](#prerequisites)
3. [CSV Formatting](#csv-formatting)
### General Information
This packaged was written for the StudentShapers Curriculum Mapping Project in the Department of Mathematics at Imperial College London. 
Given information about modules (csv), this code can be used to load all the modules into one data structure and to compare the keywords in each module to all the other available modules. Keywords are split into required and taught to help establish the nature of links between modules (i.e similar or prerequisite).

### Prerequisites 
This package was written in python 3.8

### CSV Formatting
In order to play nicely with the code that loads the module information into the data structure (JSON) that houses all the modules, the csv file for the module has to be written in a specific way. See example below
![My Image](example.png)

A few notes about this
1. If using a xslx or numbers file, only one sheet should be populated otherwise information will be lost when converting to csv.
2. Headings should be exactly as is shown (including capitalisation). This includes
    * Module Information
    * Section # (index starting from 1)
    * Keywords (Prerequisite)
    * Skills (Taught)
    * Skills (Prerequisite)
3. If a term has synonyms, the syntax for handling this is
    > term// term
I.e term 1 followed by two forward slashes followed by a space follow by synonym for term 1 and so on.
4. We used an indexing system to handle the same word being used for different concepts which will not be included here.
5. There should be no blank cells in the column before the end of the Skills (Prerequisite)

