# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 12:05:35 2021

@author: One Jae Lee
"""
import os
import pandas as pd
import re
dropbox = os.path.expanduser("~/Dropbox/Unfundedpension/src/raw/")
#Currently set to create a dictionary between Fin code and name, change remove_parantheses if you want extra info about variable
def abc_to_itemcode(excel_directory = dropbox + '/indfin_files/UserGuide.xls', remove_parantheses = True):
    workbook = pd.read_excel(excel_directory,sheet_name = '2. Variables')
    #These exist to create different column names
    # b = workbook.iloc[268:,2].tolist()
    # a = workbook.iloc[268:,1]
    e = workbook.iloc[268:,6]
    g = workbook.iloc[268:,5].tolist()
    names = workbook.iloc[268:,7].tolist()

    name_list = []
    names_dict = {}
    for index, name in enumerate(e):
        if str(name) != 'nan' and str(name) != 'F':
            name_list.append(g[index])
            if remove_parantheses:
                word = re.sub(r"\([^()]*\)", "", re.sub('[.]', '',names[index]))
            else:
                word = re.sub('[.]', '',names[index])
            if len(word) == len(word.lstrip()):
                leading_word = word.lstrip().split(",")[0]
                names_dict[g[index]] = word.lstrip()
            else:
                if g[index] in ['C1856', 'C1864','C1872']:
                    names_dict[g[index]] = word.lstrip()
                else:  
                    names_dict[g[index]] = leading_word + ', ' + word.lstrip()
            
    
    return names_dict

print(abc_to_itemcode())

