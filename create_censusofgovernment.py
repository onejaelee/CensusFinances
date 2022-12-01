'''
@author: One Jae Lee
Adjusted: Oliver Giesecke
'''

import pandas as pd
import csv
import os
import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import seaborn as sns
from scipy import stats
import statistics
from statistics import mean 

dropbox = os.path.expanduser("~/Dropbox/Unfundedpension/")
project_folder = os.path.expanduser("~/Dropbox/Unfundedpension/src/raw/cog/")

def pid_df(text_name):

    f = open(text_name, "r")
    id_code = []
    id_name = []
    county = []
    fip_state = []
    fip_county = []
    fip_place = []
    pop = []
    pop_yr = []
    enroll = []
    enroll_yr = []
    function_dist = []
    school_level = []
    fiscal_yr = []
    survey_yr = []

    
    for line in f:

        id_code.append(line[:12].replace(" ", ""))

        id_name.append(line[12:76].replace(" ", ""))
        
        county.append(line[76:111].replace(" ", ""))

        fip_state.append(line[:2].replace(" ", ""))

        fip_county.append(line[3:6].replace(" ", ""))

        fip_place.append(line[111:116].replace(" ", ""))

        pop.append(line[116:125].replace(" ", ""))

        pop_yr.append(line[125:127].replace(" ", ""))

        enroll.append(line[127:134].replace(" ", ""))

        enroll_yr.append(line[134:136].replace(" ", ""))

        function_dist.append(line[136:138].replace(" ", ""))

        school_level.append(line[138:140].replace(" ", ""))

        fiscal_yr.append(line[140:144].replace(" ", ""))

        survey_yr.append(line[144:146].replace(" ", ""))


    data = {'ID': id_code, 'Name':id_name, 'County':county, 'FIPS Code-State':fip_state, 'FIP county code':fip_county, 'FIP place code':fip_place,'Population':pop, 'Population year':pop_yr, 'Enrollment':enroll, 'Enrollment year': enroll_yr, 'Function code for special districts':function_dist,'Fiscal year ending':fiscal_yr, 'SurveyYr':survey_yr, "SchoolLevel":school_level}
    data = pd.DataFrame(data)
    data.set_index('ID', inplace=True, drop=False)
    return pd.DataFrame(data)

def new_iud_df(FinEst):

    f = open(FinEst,"r")
   
    item_list = {}
    for line in f:
        if str(line[:12]) + str(line[27:31]) in item_list:
            if line[12:13].isdigit():
                item_list[str(line[:12]) + str(line[27:31])].append(('_'+line[12:15], line[15:27].replace(" ", "")))
            else:
                item_list[str(line[:12]) + str(line[27:31])].append((line[12:15], line[15:27].replace(" ", "")))
        else:
            if line[12:13].isdigit():
                item_list[str(line[:12]) + str(line[27:31])] = [('Year4', line[27:31]),('ID',line[:12]),('UniqueID',str(line[:12]) + str(line[27:31])),('_' + line[12:15], line[15:27].replace(" ", ""))]
            else:
                item_list[str(line[:12]) + str(line[27:31])] = [('Year4', line[27:31]),('ID',line[:12]),('UniqueID',str(line[:12]) + str(line[27:31])),(line[12:15], line[15:27].replace(" ", ""))]

    organized = {}
    
    for key in item_list:

        inner = {}
        
        for values in item_list[key]:
            
            inner[values[0]] = values[1].replace(" ", "")
            
            
        organized[key] = inner
    
                
    df =pd.DataFrame.from_dict(organized, orient = 'index')

    df.set_index('ID', inplace = True, drop = False)

    return df

def pid_create_new_data(pid, fin):
    p = pid_df(pid)
    f = new_iud_df(fin)
    m = merge_iud_df(f,p)
    m['tot_charges'] = m.apply (lambda row: tot_charges(row), axis=1)
    m['tot_iglocal'] = m.apply (lambda row: tot_iglocal(row), axis=1)
    m['tot_igstate'] = m.apply (lambda row: tot_igstate(row), axis=1)
    m['tot_igfederal'] = m.apply (lambda row: tot_igfederal(row), axis=1)
    m['tot_othertax'] = m.apply (lambda row: tot_othertax(row), axis=1)
    m['tot_incometax'] = m.apply (lambda row: tot_incometax(row), axis=1)
    m['tot_licensetax'] = m.apply (lambda row: tot_licensetax(row), axis=1)
    m['tot_revenuetax'] = m.apply (lambda row: tot_revenuetax(row), axis=1)
    m['tot_tax'] = m.apply (lambda row: tot_tax(row), axis=1)
    m['tot_rev'] = m.apply (lambda row: tot_rev(row), axis=1)
    return m

def create_crosswalk(filepath):
    f = open(filepath, "r")
    pid_gid = {}
    for line in f:
        pid_gid[line[:6]] = (line[7:21], line[22:106].strip())


    return pid_gid
def gid_df(text_name):

    f = open(text_name, "r")
    id_code = []
    id_name = []
    county = []
    fip_state = []
    fip_county = []
    fip_place = []
    pop = []
    pop_yr = []
    enroll = []
    enroll_yr = []
    function_dist = []
    school_level = []
    fiscal_yr = []
    survey_yr = []

    
    for line in f:

        id_code.append(line[:14].replace(" ", ""))

        id_name.append(line[14:78].replace(" ", ""))
        
        county.append(line[78:113].replace(" ", ""))

        fip_state.append(line[113:115].replace(" ", ""))

        fip_county.append(line[115:118].replace(" ", ""))

        fip_place.append(line[118:123].replace(" ", ""))

        pop.append(line[123:132].replace(" ", ""))

        pop_yr.append(line[132:134].replace(" ", ""))

        enroll.append(line[134:141].replace(" ", ""))

        enroll_yr.append(line[141:143].replace(" ", ""))

        function_dist.append(line[143:145].replace(" ", ""))

        school_level.append(line[145:147].replace(" ", ""))

        fiscal_yr.append(line[147:151].replace(" ", ""))

        survey_yr.append(line[151:153].replace(" ", ""))


    data = {'ID': id_code, 'Name':id_name, 'County':county, 'FIPS Code-State':fip_state, 'FIP county code':fip_county, 'FIP place code':fip_place,'Population':pop, 'Population year':pop_yr, 'Enrollment':enroll, 'Enrollment year': enroll_yr, 'Function code for special districts':function_dist,'Fiscal year ending':fiscal_yr, 'SurveyYr':survey_yr}
    data = pd.DataFrame(data)
    data.set_index('ID', inplace=True, drop=False)
    return pd.DataFrame(data)

def read_iud_gid(folder):
    nineteen = pid_create_new_data(folder +"additional_years/"+ "Fin_PID_2019.txt",folder + "additional_years/"+ "2019FinEstDAT_06102021modp_pu.txt")
    eighteen = pid_create_new_data(folder +"additional_years/"+ "Fin_PID_2018.txt",folder + "additional_years/" + "2018FinEstDAT_06102021modp_pu.txt")
    
    seventeen = create_new_data(folder + "Fin_GID_2017.txt",folder + "2017FinEstDAT_02202020modp_pu.txt")
    sixteen = create_new_data(folder + "Fin_GID_2016.txt",folder + "2016FinEstDAT_10162019modp_pu.txt")
    fifteen = create_new_data(folder + "Fin_GID_2015.txt",folder + "2015FinEstDAT_10162019modp_pu.txt")
    fourteen = create_new_data(folder + "Fin_GID_2014.txt",folder + "2014FinEstDAT_10162019modp_pu.txt")

    thirteen = create_new_data(folder + "Fin_GID_2013.txt",folder + "2013FinEstDAT_10162019modp_pu.txt")

    post_imputed = pd.concat([nineteen,eighteen,seventeen,sixteen,fifteen,fourteen,thirteen])
    
    post_imputed.to_csv(folder + 'post.csv')
    post_imputed.to_pickle(folder + 'post.pkl')
    return post_imputed
def add_columns(master):
    master['tot_charges'] = master.apply (lambda row: tot_charges(row), axis=1)
    master['tot_iglocal'] = master.apply (lambda row: tot_iglocal(row), axis=1)
    master['tot_igstate'] = master.apply (lambda row: tot_igstate(row), axis=1)
    master['tot_igfederal'] = master.apply (lambda row: tot_igfederal(row), axis=1)
    master['tot_othertax'] = master.apply (lambda row: tot_othertax(row), axis=1)
    master['tot_incometax'] = master.apply (lambda row: tot_incometax(row), axis=1)
    master['tot_licensetax'] = master.apply (lambda row: tot_licensetax(row), axis=1)
    master['tot_revenuetax'] = master.apply (lambda row: tot_revenuetax(row), axis=1)
    return master
def create_new_data(gid, fin):
    g = gid_df(gid)
    f = iud_df(fin)
    m = merge_iud_df(f,g)
    m['tot_charges'] = m.apply (lambda row: tot_charges(row), axis=1)
    m['tot_iglocal'] = m.apply (lambda row: tot_iglocal(row), axis=1)
    m['tot_igstate'] = m.apply (lambda row: tot_igstate(row), axis=1)
    m['tot_igfederal'] = m.apply (lambda row: tot_igfederal(row), axis=1)
    m['tot_othertax'] = m.apply (lambda row: tot_othertax(row), axis=1)
    m['tot_incometax'] = m.apply (lambda row: tot_incometax(row), axis=1)
    m['tot_licensetax'] = m.apply (lambda row: tot_licensetax(row), axis=1)
    m['tot_revenuetax'] = m.apply (lambda row: tot_revenuetax(row), axis=1)
    m['tot_tax'] = m.apply (lambda row: tot_tax(row), axis=1)
    m['tot_rev'] = m.apply (lambda row: tot_rev(row), axis=1)
    return m

def add_tot_rev(df):
    df['tot_rev'] = df.apply (lambda row: tot_rev(row), axis=1)
    return df
def add_tot_tax(df):
    df['tot_tax'] = df.apply (lambda row: tot_tax(row), axis=1)
    return df
def tot_tax(row):
    codes = ['T01', 'T09', 'T10','T11', 'T12', 'T13', 'T14', 'T15', 'T16', 'T19', 'T20', 'T21', 'T22', 'T23', 'T24', 'T25', 'T27', 'T28', 'T29', 'T50', 'T51', 'T53','T99','T40','T41']
    total = 0
    for item in codes:
        if item in row:
            if not pd.isnull(row[item]) and str(row[item])!= '':
                total += int(row[item])
    return total

#Use this to tabulate total revenue tax from its individual item codes    
def tot_revenuetax(row):
    total = 0

    if 'T01' in row:
        if not pd.isnull(row['T01']) and str(row['T01']) != '':
            total += int(row['T01'])
    if 'T09' in row:
        if not pd.isnull(row['T09']) and str(row['T09']) != '':
            total += int(row['T09'])
    if 'T10' in row:
        if not pd.isnull(row['T10']) and str(row['T10']) != '':
            total += int(row['T10'])
    if 'T11' in row:
        if not pd.isnull(row['T11']) and str(row['T11']) != '':
            total += int(row['T11'])
    if 'T12' in row:
        if not pd.isnull(row['T12']) and str(row['T12']) != '':
            total += int(row['T12'])
    if 'T13' in row:     
        if not pd.isnull(row['T13']) and str(row['T13']) != '':
            total += int(row['T13'])
    if 'T14' in row:     
        if not pd.isnull(row['T14']) and str(row['T14']) != '':
            total += int(row['T14'])
    if 'T15' in row:  
        if not pd.isnull(row['T15']) and str(row['T15']) != '':
            total += int(row['T15'])
    if 'T16' in row:  
        if not pd.isnull(row['T16']) and str(row['T16']) != '':
            total += int(row['T16'])
    if 'T19' in row:      
        if not pd.isnull(row['T19']) and str(row['T19']) != '':
            total += int(row['T19'])
    return total
#Use this to tabulate total license tax in a given ID-Year row from the individual item codes
def tot_licensetax(row):
    total = 0
    if 'T20' in row:  
        if not pd.isnull(row['T20']) and str(row['T20']) != '':
            total += int(row['T20'])
    if 'T21' in row:  
        if not pd.isnull(row['T21']) and str(row['T21']) != '':
            total += int(row['T21'])
    if 'T22' in row:  
        if not pd.isnull(row['T22']) and str(row['T22']) != '':
            total += int(row['T22'])
    if 'T23' in row:     
        if not pd.isnull(row['T23']) and str(row['T23']) != '':
            total += int(row['T23'])
    if 'T24' in row:  
        if not pd.isnull(row['T24']) and str(row['T24']) != '':
            total += int(row['T24'])
    if 'T25' in row:     
        if not pd.isnull(row['T25']) and str(row['T25']) != '':
            total += int(row['T25'])
    if 'T27' in row:     
        if not pd.isnull(row['T27']) and str(row['T27']) != '':
            total += int(row['T27'])
    if 'T28' in row:  
        if not pd.isnull(row['T28']) and str(row['T28']) != '':
            total += int(row['T28'])
    if 'T29' in row:  
        if not pd.isnull(row['T29']) and str(row['T29']) != '':
            total += int(row['T29'])
        
        
    
    return total
#Tabulates the total revenue within the historic data from its individual item codes, with a default setting to include utility insurance

def tot_rev(row, util_insur = True):
    codes = ['C191','U40','T01', 'T09', 'T10','T11', 'T12', 'T13', 'T14', 'T15', 'T16', 'T19', 'T20', 'T21', 'T22', 'T23', 'T24', 'T25', 'T27', 'T28', 'T29', 'T50', 'T51', 'T53','T99','T40','T41', 'B01', 'B21','B27','B30','B42','B46','B47','B50','B59','B79','B80','B89','C21','C28','C30','C42','C46','C47','C50','C79','C80','C89','D11','D21', 'D30','D42','D46','D47','D50','D79','D80','D89','A01','A03','A09','A10','A12','A21','A36','A44','A45','A50','A59','A60','A80','A81','A87','A89','U01','U10','U10','U11','U20','U30','U95','U99']
    
    if util_insur:
        u = ['A90','A91', 'A92', 'A93', 'A94']
        emp = ['X01', 'X04', 'X05','X06','X08','X09']
        unemp = ['Y01','Y02','Y04']
        codes.extend(u)
        codes.extend(emp)
        codes.extend(unemp)
    total = 0
    for item in codes:
        if item == 'X01':
            #Only add to the total if this item has a valid entry, some values don't exist so it must be checked before being summed
            if 'X01' in row:
                if not pd.isnull(row[item]) and str(row[item])!= '':
                    total += int(row[item])
                elif 'X02' in row:
                        if not pd.isnull(row['X02']) and str(row['X02'])!= '':
                            total += int(row['X02'])
            elif 'X02' in row:
                        if not pd.isnull(row['X02']) and str(row['X02'])!= '':
                            total += int(row['X02'])
        #Checks if this item is stored within the row, if not, it is calculated from known invidiual components
        if item == 'C191':
            if 'C191' in row:
                if not pd.isnull(row[item]) and str(row[item])!= '':
                    total += int(row[item])
                else:
                    if 'A16' in row:
                        if not pd.isnull(row['A16']) and str(row['A16'])!= '':
                            total += int(row['A16'])
                    if 'A18' in row:
                        if not pd.isnull(row['A18']) and str(row['A18'])!= '':
                            total += int(row['A18'])
            else:
                if 'A16' in row:
                    if not pd.isnull(row['A16']) and str(row['A16'])!= '':
                        total += int(row['A16'])
                if 'A18' in row:
                    if not pd.isnull(row['A18']) and str(row['A18'])!= '':
                        total += int(row['A18'])
        
        #Checks if this item is stored within the row, if not, it is calculated from known invidiual components
        if item == 'C218':
            if 'C218' in row:
                if not pd.isnull(row[item]) and str(row[item])!= '':
                    total += int(row[item])
                else:
                    if 'U40' in row:
                        if not pd.isnull(row['U40']) and str(row['U40'])!= '':
                            total += int(row['U40'])
                    if 'U41' in row:
                        if not pd.isnull(row['U41']) and str(row['U41'])!= '':
                            total += int(row['U41'])
            else:
                if 'U40' in row:
                    if not pd.isnull(row['U40']) and str(row['U40'])!= '':
                        total += int(row['U40'])
                if 'U41' in row:
                    if not pd.isnull(row['U41']) and str(row['U41'])!= '':
                        total += int(row['U41'])
    
        #Checks if this item is stored within the row, if not, it is calculated from known invidiual components
        if item == 'T40':
            if 'T40' in row:
                if not pd.isnull(row[item]) and str(row[item])!= '':
                    total += int(row[item])
                elif 'T49' in row:
                    if not pd.isnull(row['T49']) and str(row['T49'])!= '':
                        total += int(row['T49'])
            elif 'T49' in row:
                if not pd.isnull(row['T49']) and str(row['T49'])!= '':
                    total += int(row['T49'])
        #Checks if this item is stored within the row, if not, it is calculated from known invidiual components
        elif item == 'B47':
            if 'B47' in row:
                if not pd.isnull(row[item]) and str(row[item])!= '':
                    total += int(row[item])
                elif 'B94' in row:
                    if not pd.isnull(row['B94']) and str(row['B94'])!= '':
                        total += int(row['B94'])
            elif 'B94' in row:
                if not pd.isnull(row['B94']) and str(row['B94'])!= '':
                    total += int(row['B94'])
        #Checks if this item is stored within the row, if not, it is calculated from known invidiual components
        elif item == 'B59':
            if 'B59' in row:
                if not pd.isnull(row[item]) and str(row[item])!= '':
                    total += int(row[item])
                elif 'B94' in row:
                    if not pd.isnull(row['B94']) and str(row['B94'])!= '':
                        total += int(row['B94'])
            elif 'B94' in row:
                if not pd.isnull(row['B94']) and str(row['B94'])!= '':
                    total += int(row['B94'])
        #Checks if this item is stored within the row, if not, it is calculated from known invidiual components
        elif item == 'B89':
            if 'B89' in row:
                if not pd.isnull(row[item]) and str(row[item])!= '':
                    total += int(row[item])
                else:
                    if 'B91' in row:
                        if not pd.isnull(row['B91']) and str(row['B91'])!= '':
                            total += int(row['B91'])
                    if 'B92' in row:
                        if not pd.isnull(row['B92']) and str(row['B92'])!= '':
                            total += int(row['B92'])
                    if 'B93' in row:
                        if not pd.isnull(row['B93']) and str(row['B93'])!= '':
                            total += int(row['B93'])
            else:
                if 'B91' in row:
                    if not pd.isnull(row['B91']) and str(row['B91'])!= '':
                        total += int(row['B91'])
                if 'B92' in row:
                    if not pd.isnull(row['B92']) and str(row['B92'])!= '':
                        total += int(row['B92'])
                if 'B93' in row:
                    if not pd.isnull(row['B93']) and str(row['B93'])!= '':
                        total += int(row['B93'])
        elif item == 'C47':
            #C47 includes C94, but it may not be recorded for certain years, thus C94 is added if C47 isn't
            if 'C47' in row:
                if not pd.isnull(row[item]) and str(row[item])!= '':
                    total += int(row[item])
                elif 'C94' in row:
                    if not pd.isnull(row['C94']) and str(row['C94'])!= '':
                        total += int(row['C94'])
            elif 'C94' in row:
                if not pd.isnull(row['C94']) and str(row['C94'])!= '':
                    total += int(row['C94'])
        elif item == 'C89':
            if 'C89' in row:
                if not pd.isnull(row[item]) and str(row[item])!= '':
                    total += int(row[item])
                #There is a format difference between specific years, where C89 is equivalent to C91, C92, and C93 at times.
                else:
                    if 'C91' in row:
                        if not pd.isnull(row['C91']) and str(row['C91'])!= '':
                            total += int(row['C91'])
                    if 'C92' in row:
                        if not pd.isnull(row['C92']) and str(row['C92'])!= '':
                            total += int(row['C92'])
                    if 'C93' in row:
                        if not pd.isnull(row['C93']) and str(row['C93'])!= '':
                            total += int(row['C93'])
            else:
                if 'C91' in row:
                    if not pd.isnull(row['C91']) and str(row['C91'])!= '':
                        total += int(row['C91'])
                if 'C92' in row:
                    if not pd.isnull(row['C92']) and str(row['C92'])!= '':
                        total += int(row['C92'])
                if 'C93' in row:
                    if not pd.isnull(row['C93']) and str(row['C93'])!= '':
                        total += int(row['C93'])
        elif item == 'D89':
            if 'D89' in row:
                if not pd.isnull(row[item]) and str(row[item])!= '':
                    total += int(row[item])
                #D89 includes D91, D92, and D93. Add these individually if D89 isn't in the data
                else:
                    if 'D91' in row:
                        if not pd.isnull(row['D91']) and str(row['D91'])!= '':
                            total += int(row['D91'])
                    if 'D92' in row:
                        if not pd.isnull(row['D92']) and str(row['D92'])!= '':
                            total += int(row['D92'])
                    if 'D93' in row:
                        if not pd.isnull(row['D93']) and str(row['D93'])!= '':
                            total += int(row['D93'])
            else:
                if 'D91' in row:
                    if not pd.isnull(row['D91']) and str(row['D91'])!= '':
                        total += int(row['D91'])
                if 'D92' in row:
                    if not pd.isnull(row['D92']) and str(row['D92'])!= '':
                        total += int(row['D92'])
                if 'D93' in row:
                    if not pd.isnull(row['D93']) and str(row['D93'])!= '':
                        total += int(row['D93'])
        elif item == 'A59':
            if 'A59' in row:
                if not pd.isnull(row[item]) and str(row[item])!= '':
                    total += int(row[item])
                #A54, A56, and A59 are said to be included in A59 within the user guide.
                #However, it doesn't make sense that A59 would be constructed by itself and other numbers since all values are positive
                #Thus A59 is commented out in the case that A59 is not within the dataset
                else:
                    if 'A54' in row:
                        if not pd.isnull(row['A54']) and str(row['A54'])!= '':
                            total += int(row['A54'])
                    if 'A56' in row:
                        if not pd.isnull(row['A56']) and str(row['A56'])!= '':
                            total += int(row['A56'])
                    # if 'A59' in row:
                    #     if not pd.isnull(row['A59']) and str(row['A59'])!= '':
                    #         total += int(row['A59'])
            else:
                if 'A54' in row:
                    if not pd.isnull(row['A54']) and str(row['A54'])!= '':
                        total += int(row['A54'])
                if 'A56' in row:
                    if not pd.isnull(row['A56']) and str(row['A56'])!= '':
                        total += int(row['A56'])
                # if 'A59' in row:
                #     if not pd.isnull(row['A59']) and str(row['A59'])!= '':
                #         total += int(row['A59'])
        elif item == 'A89':
            #A06 and A14 are added in case A89 is not present, since A06 and A14 is included in A06
            if 'A89' in row:
                if not pd.isnull(row[item]) and str(row[item])!= '':
                    total += int(row[item])
                else:
                    if 'A06' in row:
                        if not pd.isnull(row['A06']) and str(row['A06'])!= '':
                            total += int(row['A06'])
                    if 'A14' in row:
                        if not pd.isnull(row['A14']) and str(row['A14'])!= '':
                            total += int(row['A14'])
            else:
                if 'A06' in row:
                    if not pd.isnull(row['A06']) and str(row['A06'])!= '':
                        total += int(row['A06'])
                if 'A14' in row:
                    if not pd.isnull(row['A14']) and str(row['A14'])!= '':
                        total += int(row['A14'])
        elif item in row:
            if not pd.isnull(row[item]) and str(row[item])!= '':
                total += int(row[item])
    return total

#Sums up the total other tax within a given row from its individual item codes
def tot_othertax(row):
    total = 0
    if 'T50' in row:  
        if not pd.isnull(row['T50']) and str(row['T50']) != '':
            total += int(row['T50'])
    if 'T51' in row:   
        if not pd.isnull(row['T51']) and str(row['T51']) != '':
            total += int(row['T51'])
    if 'T53' in row:  
        if not pd.isnull(row['T53']) and str(row['T53']) != '':
            total += int(row['T53'])
    if 'T99' in row:  
        if not pd.isnull(row['T99']) and str(row['T99']) != '':
            total += int(row['T99'])
    
    return total

#Sums up the total income tax within a given row from its individual item codes
#Used to check how well the individual item codes match up to C129, also used for tabulating the value for post-2012 dataset
def tot_incometax(row):
    total = 0
    if 'T40' in row:  
        if not pd.isnull(row['T40']) and str(row['T40']) != '':
            total += int(row['T40'])
    if 'T41' in row:  
        if not pd.isnull(row['T41']) and str(row['T41']) != '':
            total += int(row['T41'])
        
    return total

#Sums up the total income tax within a given row from its individual item codes
#Used to check how well the subtotals match up to C156, also used for tabulating the value for post-2012 dataset
#In the future, might change it to a for loop to make it look nicer
def tot_igfederal(row):
    total = 0
    if 'B01' in row:  
        if not pd.isnull(row['B01']) and str(row['B01']) != '':
            total += int(row['B01'])
    if 'B21' in row:  
        if not pd.isnull(row['B21']) and str(row['B21']) != '':
            total += int(row['B21'])
    if 'B22' in row:  
        if not pd.isnull(row['B22']) and str(row['B22']) != '':
            total += int(row['B22'])
    if 'B27' in row:  
        if not pd.isnull(row['B27']) and str(row['B27']) != '':
            total += int(row['B27'])
    if 'B30' in row:  
        if not pd.isnull(row['B30']) and str(row['B30']) != '':
            total += int(row['B30'])
    if 'B42' in row:  
        if not pd.isnull(row['B42']) and str(row['B42']) != '':
            total += int(row['B42'])
    if 'B46' in row:   
        if not pd.isnull(row['B46']) and str(row['B46']) != '':
            total += int(row['B46'])
    if 'B47' in row:    
        if not pd.isnull(row['B47']) and str(row['B47']) != '':
            total += int(row['B47'])
    if 'B50' in row:  
        if not pd.isnull(row['B50']) and str(row['B50']) != '':
            total += int(row['B50'])
    if 'B59' in row:  
        if not pd.isnull(row['B59']) and str(row['B59']) != '':
            total += int(row['B59'])
    if 'B79' in row:     
        if not pd.isnull(row['B79']) and str(row['B79']) != '':
            total += int(row['B79'])
    if 'B80' in row:   
        if not pd.isnull(row['B80']) and str(row['B80']) != '':
            total += int(row['B80'])
    if 'B89' in row:    
        if not pd.isnull(row['B89']) and str(row['B89']) != '':
            total += int(row['B89'])
    return total

#Sums up the total intergovernmental revenue from state
#Used to check how well the subtotals match up to C156, also used for tabulating the value for post-2012 dataset
#In the future, might change it to a for loop to make it look nicer
def tot_igstate(row):
    total = 0
    if 'C21' in row:  
        if not pd.isnull(row['C21']) and str(row['C21']) != '':
            total += int(row['C21'])
    if 'C28' in row:  
        if not pd.isnull(row['C28']) and str(row['C28']) != '':
            total += int(row['C28'])
    if 'C30' in row:     
        if not pd.isnull(row['C30']) and str(row['C30']) != '':
            total += int(row['C30'])
    if 'C42' in row:      
        if not pd.isnull(row['C42']) and str(row['C42']) != '':
            total += int(row['C42'])
    if 'C46' in row:         
        if not pd.isnull(row['C46']) and str(row['C46']) != '':
            total += int(row['C46'])
    if 'C47' in row:      
        if not pd.isnull(row['C47']) and str(row['C47']) != '':
            total += int(row['C47'])
    if 'C50' in row:     
        if not pd.isnull(row['C50']) and str(row['C50']) != '':
            total += int(row['C50'])
    if 'C79' in row:  
        if not pd.isnull(row['C79']) and str(row['C79']) != '':
            total += int(row['C79'])
    if 'C80' in row:  
        if not pd.isnull(row['C80']) and str(row['C80']) != '':
            total += int(row['C80'])
    if 'C89' in row:     
        if not pd.isnull(row['C89']) and str(row['C89']) != '':
            total += int(row['C89'])
    
    return total
#Calculates the total charges from the individul item codes. Used to check how well
    #it matches up with C183, also used for tabulating the value for post-2012 dataset
    #In the future, might change it to a for loop to make it look nicer
def tot_charges(row):
    total = 0
    if 'A01' in row:  
        if not pd.isnull(row['A01']) and str(row['A01']) != '':
            total += int(row['A01'])
    if 'A03' in row:  
        if not pd.isnull(row['A03']) and str(row['A03']) != '':
            total += int(row['A03'])
    if 'A09' in row:  
        if not pd.isnull(row['A09']) and str(row['A09']) != '':
            total += int(row['A09'])
    if 'A10' in row:  
        if not pd.isnull(row['A10']) and str(row['A10']) != '':
            total += int(row['A10'])
    if 'A12' in row:  
        if not pd.isnull(row['A12']) and str(row['A12']) != '':
            total += int(row['A12'])
    if 'A21' in row:  
        if not pd.isnull(row['A21']) and str(row['A21']) != '':
            total += int(row['A21'])
    if 'A36' in row:  
        if not pd.isnull(row['A36']) and str(row['A36']) != '':
            total += int(row['A36'])
    if 'A44' in row:  
        if not pd.isnull(row['A44']) and str(row['A44']) != '':
            total += int(row['A44'])
    if 'A45' in row:  
        if not pd.isnull(row['A45']) and str(row['A45']) != '':
            total += int(row['A45'])
    if 'A50' in row:  
        if not pd.isnull(row['A50']) and str(row['A50']) != '':
            total += int(row['A50'])
    if 'A59' in row:  
        if not pd.isnull(row['A59']) and str(row['A59']) != '':
            total += int(row['A59'])
    if 'A60' in row:  
        if not pd.isnull(row['A60']) and str(row['A60']) != '':
            total += int(row['A60'])
    if 'A61' in row:  
        if not pd.isnull(row['A61']) and str(row['A61']) != '':
            total += int(row['A61'])
    if 'A80' in row:  
        if not pd.isnull(row['A80']) and str(row['A80']) != '':
            total += int(row['A80'])
    if 'A81' in row:  
        if not pd.isnull(row['A81']) and str(row['A81']) != '':
            total += int(row['A81'])
    if 'A87' in row:  
        if not pd.isnull(row['A87']) and str(row['A87']) != '':
            total += int(row['A87'])
    if 'A89' in row:  
        if not pd.isnull(row['A89']) and str(row['A89']) != '':
            total += int(row['A89'])
            
    return total
#Calculates total intergovernmental revenue from local government from its individual units.
    #Used to check how well it matches up to C168, also used for tabulating the value for post-2012 dataset
#In the future, might change it to a for loop to make it look nicer
def tot_iglocal(row):
    
    total = 0
    if 'D11' in row:  
        if not pd.isnull(row['D11']) and str(row['D11']) != '':
            total += int(row['D11'])
    if 'D21' in row:          
        if not pd.isnull(row['D21']) and str(row['D21']) != '':
            total += int(row['D21'])
    if 'D30' in row:      
        if not pd.isnull(row['D30']) and str(row['D30']) != '':
            total += int(row['D30'])
    if 'D42' in row:     
        if not pd.isnull(row['D42']) and str(row['D42']) != '':
            total += int(row['D42'])
    if 'D46' in row:   
        if not pd.isnull(row['D46']) and str(row['D46']) != '':
            total += int(row['D46'])
    if 'D47' in row:  
        if not pd.isnull(row['D47']) and str(row['D47']) != '':
            total += int(row['D47'])
        elif 'D94' in row:  
            if not pd.isnull(row['D94']) and str(row['D94']) != '':
                total += int(row['D94'])
    elif 'D94' in row:  
        if not pd.isnull(row['D94']) and str(row['D94']) != '':
            total += int(row['D94'])
    if 'D50' in row:    
        if not pd.isnull(row['D50']) and str(row['D50']) != '':
            total += int(row['D50'])
    if 'D79' in row:    
        if not pd.isnull(row['D79']) and str(row['D79']) != '':
            total += int(row['D79'])
    if 'D80' in row:   
        if not pd.isnull(row['D80']) and str(row['D80']) != '':
            total += int(row['D80'])
    if 'D89' in row:     
        if not pd.isnull(row['D89']) and str(row['D89']) != '':
            total += int(row['D89'])
        
    return total
#Used to merge the dataframe previously created from the yearly FinEst file with the yearly Fin_GID file
def merge_iud_df(fin,gid):
    fin['Name'] = np.nan
    fin['County'] = np.nan
    fin['FIPS Code-State'] = np.nan
    fin['FIP county code'] = np.nan
    fin['FIP place code'] = np.nan
    fin['Population'] = np.nan
    fin['Enrollment'] = np.nan
    fin['Enrollment year'] = np.nan
    fin['Function code for special districts'] = np.nan
    fin['Fiscal year ending'] = np.nan
    fin['SurveyYr'] = np.nan
    for index, row in gid.iterrows():
        fin.loc[index,['Name']] = row['Name']
        fin.loc[index,['County']] = row['County']
        fin.loc[index,['FIPS Code-State']] = row['FIPS Code-State']
        fin.loc[index, ['FIP county code']] = row['FIP county code']
        fin.loc[index,['FIP place code']] = row['FIP place code']
        fin.loc[index, ['Population']] = row['Population']
        fin.loc[index,['Enrollment']] = row['Enrollment']
        fin.loc[index, ['Enrollment year']] = row['Enrollment year']
        fin.loc[index, ['Function code for special districts']] = row['Function code for special districts']
        fin.loc[index, ['Fiscal year ending']] = row['Fiscal year ending']
        fin.loc[index, ['SurveyYr'] ]= row['SurveyYr']
  
    fin.set_index('UniqueID', inplace=True, drop=True)
    return fin
#Used to read a FinEst file path and returns the file in a dataframe format
def iud_df(FinEst):
    '''
    Did not split up the ID into (positions 1-2 = state, position 3 = type, positions
    4-6 = county or county-type area where government is
    located, positions 7-9 = unit identifier, positions 10-14
    should be 00000 to indicate that the unit is not part of
    another government)
    '''
    f = open(FinEst,"r")
   
    item_list = {}
    for line in f:
        if str(line[:9]) + str(line[29:33]) in item_list:
            if line[14:15].isdigit():
                item_list[str(line[:9]) + str(line[29:33])].append(('_'+line[14:17], line[17:29].replace(" ", "")))
            else:
                item_list[str(line[:9]) + str(line[29:33])].append((line[14:17], line[17:29].replace(" ", "")))
        else:
            if line[14:15].isdigit():
                item_list[str(line[:9]) + str(line[29:33])] = [('Year4', line[29:33]),('ID',line[:14]),('UniqueID',str(line[:9]) + str(line[29:33])),('_' + line[14:17], line[17:29].replace(" ", ""))]
            else:
                item_list[str(line[:9]) + str(line[29:33])] = [('Year4', line[29:33]),('ID',line[:14]),('UniqueID',str(line[:9]) + str(line[29:33])),(line[14:17], line[17:29].replace(" ", ""))]
     
    organized = {}
    
    for key in item_list:

        inner = {}
        
        for values in item_list[key]:
            
            inner[values[0]] = values[1].replace(" ", "")
            
            
        organized[key] = inner
    
                
    df =pd.DataFrame.from_dict(organized, orient = 'index')

    df.set_index('ID', inplace = True, drop = False)

    return df

#Takes in a statetypeu file path and returns the file as a dataframe
def puf_df(statetypepu):
    f = open(statetypepu,"r")
    state = []
    est = []
    item = []
    amount = []
    var = []
    survey_yr = []
    for line in f:
        state.append(line[:2])
        est.append(line[2:3])
        item.append(line[4:7])
        amount.append(line[8:20])
        var.append(line[22:32])
        survey_yr.append(line[33:35])
    data = {'State code':state, "Level of estimate code":est,"Item code":item,"Amount":amount,"Coefficient of variation":var, "Last two digits of survey year":survey_yr}
    return pd.DataFrame(data)

#Takes in an IndFin type file path (this is a historical data format) and returns the file as a dataframe
def indfin_df(folder, name):
    with open(folder + name) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        labels = []
        df_list = []
        for ind, row in enumerate(readCSV):
            if ind == 0:
                for label in row:
                    labels.append(label)

            else:
                d = dict(zip(labels,row))
                df = pd.DataFrame.from_dict([d])
                df_list.append(df)
        f_df = pd.concat(df_list)
        f_df.to_pickle(folder + name[:-4] + ".pkl")
        print(name[:-4] + ".pkl made")
        print(f_df)

#Quickly read a folder of the historical data files IndFin
def read_indfin_folder(folder_directory):

    for i in os.listdir(project_folder + folder_directory):
        if i[i.rfind('.')-1:] == 'a.Txt':
            indfin_df(project_folder + folder_directory,i)
        if i[i.rfind('.')-1:] == 'b.Txt':
            indfin_df(project_folder + folder_directory,i)
        if i[i.rfind('.')-1:] == 'c.Txt':
            indfin_df(project_folder + folder_directory,i)

#I have intermediate pickle files created in order in case of future use
#This is just all the historical data files turned into pickle files
def pickle_folder_to_std_format(folder_directory):
    
    for i in os.listdir(project_folder + folder_directory):
        if i[i.rfind('.')-1:] == 'a.pkl':
            pickle_to_std_ind_pickle(i, project_folder + folder_directory)
        if i[i.rfind('.')-1:] == 'b.pkl':
            pickle_to_std_ind_pickle(i, project_folder + folder_directory)
        if i[i.rfind('.')-1:] == 'c.pkl':
            pickle_to_std_ind_pickle(i, project_folder + folder_directory)  
            
#Converts the pickle files from the previous function into one that can be merged with other
#Pickle files by adding a unique identifier (which is the ID merged with the year)
def pickle_to_std_ind_pickle(pickle, folder_directory):
    #print(pickle[:-4])
    #print(folder_directory)
    unpickled_df = pd.read_pickle(folder_directory + pickle)
    unpickled_df['UniqueID'] = unpickled_df.ID.map(str) + unpickled_df.Year4
    unpickled_df.set_index('UniqueID', inplace=True, drop=True)
    unpickled_df.to_pickle(folder_directory + pickle[:-4] + "std.pkl")
    print(pickle[:-4] + "std.pkl made")

#Merges all the given pickle files from the previous function by the three subcategories of a, b, and c
#These intermediate files are created for specific use cases
def union_std_pickle(folder_directory):
    df_list_a = []
    df_list_b = []
    df_list_c = []
    for i in os.listdir(project_folder + folder_directory):
        if i[i.rfind('.')-4:] == 'astd.pkl':
            x = pd.read_pickle(project_folder + folder_directory + i)
            df_list_a.append(x)
        if i[i.rfind('.')-4:] == 'bstd.pkl':
            x = pd.read_pickle(project_folder + folder_directory + i)
            df_list_b.append(x)
        if i[i.rfind('.')-4:] == 'cstd.pkl':
            x = pd.read_pickle(project_folder + folder_directory + i)
            df_list_c.append(x) 
    
    a = pd.concat(df_list_a)
    a.to_pickle(project_folder + folder_directory + 'a.pkl')
    b = pd.concat(df_list_b)
    b.to_pickle(project_folder + folder_directory + 'b.pkl')
    c = pd.concat(df_list_c)
    c.to_pickle(project_folder + folder_directory + 'c.pkl')

#Merges the three different pickle files from the previous function into a single pickle file
def union_abc_pickle(folder_directory):
    a = pd.read_pickle(project_folder + folder_directory + 'a.pkl')
    b = pd.read_pickle(project_folder + folder_directory + 'b.pkl')
    c = pd.read_pickle(project_folder + folder_directory + 'c.pkl')
    print(len(b.columns),len(c.columns))
    b = b.drop(['SortCode', 'Year4', 'ID'], axis = 1)
    c = c.drop(['SortCode', 'Year4', 'ID'], axis = 1)
    print(b)
    print(c)
    print(len(b.columns),len(c.columns))
    d = pd.concat([a,b,c], axis = 1)
    print(d)
    print(len(d))
    print(len(a),len(b),len(c))
    
    d.to_pickle(project_folder+ folder_directory + '/abc.pkl')

#Relabel the variables in IndFin files with the item codes found in the UserGuide file
#folder_directory is the subfolder within the project folder where the UserGuide is placed, and where the new csv file will be saved
def abc_to_itemcode(folder_directory, excel_name):
    print(project_folder + folder_directory + 'fincodename.pkl')
    print(project_folder + folder_directory + 'fincodename.csv')
    workbook = pd.read_excel(project_folder + folder_directory + excel_name,sheet_name = '2. Variables')
    #These exist to create different column names
    b = workbook.iloc[268:,2].tolist()
    # a = workbook.iloc[268:,1]
    e = workbook.iloc[268:,6]
    g = workbook.iloc[268:,5].tolist()
    # d = workbook.iloc[268:,4].tolist()
    
    #e_list = e.tolist()

    name_list = []
    
    
    for index, name in enumerate(e):
        if str(name) != 'nan' and str(name) != 'F':
            name_list.append(g[index]) 
    

    print(len(name_list))
    abc = pd.read_pickle(project_folder + folder_directory + '/abc.pkl')
    abc.to_csv(project_folder + folder_directory + '/abc.csv')
    index = 0
    for i, j in abc.iterrows():
        if index < 1:
            for k,l in j.iteritems():
                if index > 24:
                    abc.rename(columns = {k:name_list[index-25]}, inplace= True)
                index += 1
                if(index%10 == 0):
                    print(index)
        else:
            break
    print(abc)
    print(abc.columns)
    abc.to_csv(project_folder + folder_directory + 'fincodename.pkl')
    abc.to_csv(project_folder + folder_directory + 'fincodename.csv')

#Creates various files that are used to check frequencies of certain cities, and coverage for a given year
def count_per_year(file_directory):
    #Currently coded for Connecticut
    df = pd.read_pickle(file_directory)
    every = {}
    years = {}
    occurences = {}
    state ={}
    county = {}
    city = {}
    town = {}
    sp = {}
    school = {}
    
    yearly_county = {}
    yearly_state = {}
    yearly_city = {}
    yearly_town = {}
    yearly_sp = {}
    yearly_school = {}

    
    yearly_id= {}
    
    city_years = {}
    
    ct_year = {}
    for i, j in df.iterrows():
        code = j['ID']
        year = j['Year4']
        state_code = j['State Code']
        years[year] = 0
        every[year] = every.get(year, 0) + 1
        
        if (j['Name'],code) in city_years:
            city_years[(j['Name'],code)].append(year)
        else:
            city_years[(j['Name'],code)] = [year]
        #state, currently it is set for conneticut since the code is looking for '07'
        if str(state_code) == '07':
            #this block counts the cities, '2' 
            if str(code)[2] == '2':
                if j['Name'] in ct_year:
                    ct_year[j['Name']].append(year)
                else:
                    ct_year[j['Name']] = [year]
        if str(code)[2] == '0':
        #county
            state[year] = state.get(year, 0) + 1
            if year in yearly_state:
                yearly_state[year].append(j['Name'])
            else:
                yearly_state[year] = [j['Name']]
        elif str(code)[2] == '1':
        #city
            county[year] = county.get(year, 0) + 1
            if year in yearly_county:
                yearly_county[year].append(j['Name'])
            else:
                yearly_county[year] = [j['Name']]
        elif str(code)[2] == '2':
            city[year] = city.get(year, 0) + 1
            if year in yearly_city:
                yearly_city[year].append(j['Name'])
            else:
                yearly_city[year] = [j['Name']]
        #Township
        elif str(code)[2] == '3':
            town[year] = town.get(year, 0) + 1
            if year in yearly_town:
                yearly_town[year].append(j['Name'])
            else:
                yearly_town[year] = [j['Name']]
        #Special District
        elif str(code)[2] == '4':
            sp[year] = sp.get(year, 0) + 1
            if year in yearly_sp:
                yearly_sp[year].append(j['Name'])
            else:
                yearly_sp[year] = [j['Name']]
        #School district
        elif str(code)[2] == '5':
            school[year] =school.get(year, 0) + 1
            if year in yearly_school:
                yearly_school[year].append(j['Name'])
            else:
                yearly_school[year] = [j['Name']]
    yearly_cities = {}
    #sorts the list for each year
    for key in ct_year:
        ct_year[key].sort()
    df = pd.DataFrame.from_dict(ct_year, orient = 'index')
    df.to_csv(project_folder + '/2012_1967/' + 'ct.csv')
    df.to_pickle(project_folder + '/2012_1967/' + 'ct.pkl')
    
    df = pd.DataFrame.from_dict(city_years, orient = 'index')
    
    df.to_csv(project_folder + '/2012_1967/' + 'city_years.csv')
    df.to_pickle(project_folder + '/2012_1967/' + 'city_years.pkl')
    #creates a dictionary yearly_id that has everycity, county, town, etc occurs in a given year
    #creates a dictionary occurences that has the count of each level of government (currently not used)
    for key in years:
        yearly_cities[key] = [yearly_city.get(key, None)]
        
        yearly_id[key] = [yearly_state.get(key, None)]
        yearly_id[key].append(yearly_county.get(key, None))
        yearly_id[key].append(yearly_city.get(key,None))
        yearly_id[key].append(yearly_town.get(key, None))
        yearly_id[key].append(yearly_sp.get(key, None))
        yearly_id[key].append(yearly_school.get(key, None))

        
        occurences[key] = [every.get(key, 0)]
        occurences[key].append(state.get(key, 0))
        occurences[key].append(county.get(key, 0))
        occurences[key].append(city.get(key, 0))
        occurences[key].append(town.get(key, 0))
        occurences[key].append(sp.get(key, 0))
        occurences[key].append(school.get(key, 0))
    
    #A file that has a list of survey years a given place occurs in
    df.to_csv(project_folder + '/2012_1967/' + 'surveycounts.csv')
    df.to_pickle(project_folder + '/2012_1967/' + 'surveycounts.pkl')
    df = pd.DataFrame.from_dict(yearly_id, orient = 'index', columns = ['State', 'Counties', 'Cities', 'Townships', 'Special Districts', 'School Districts'])
    
    #List of cities, counties, etc broken down in categories, for a given survey year
    df.to_csv(project_folder + '/2012_1967/' + 'surveynames.csv')
    df.to_pickle(project_folder + '/2012_1967/' + 'surveynames.pkl')
    
    df = pd.DataFrame.from_dict(yearly_cities, orient = 'index', columns = ['Cities'])
    #List of cities in a given survey year
    df.to_csv(project_folder + '/2012_1967/' + 'surveycities.csv')
    df.to_pickle(project_folder + '/2012_1967/' + 'surveycities.pkl')


    
#Formatted to take in Stata-created variable names, hence the lowercase.
#Calculates the share of expenditures that are made to local governments
def sum_local(row):
    
    total = 0
    rank = {}
    
    rank_dict = {}
    total_exp = 0
    expend = {'m01':'Air Trans IG-Local',
              'm05':'Corrections IG-Local',
              'm12':'Elementary & Sec IG-Local',
              'm18':'Higher Ed IG-Local',
              'm21':'Other Ed IG-Local',
              'm23':'Financial Admin IG-Local',
              'm24':'Fire Protection IG-Local',
              'm25':'Judicial & Legal IG-Local',
              'm29':'Central Staff IG-Local',
              'm32':'Health IG-Local',
              'm38':'Other Hospital IG-Local',
              'm44':'Reg Highway IG-Local',
              'm47':'Transit Subsidies IG-Local',
              'm50':'Housing & Community Dev IG-Local',
              'm52':'Libraries IG-Local',
              'm59':'Natural Resources IG-Local',
              'm60':'Parking Facilities IG-Local',
              'm61':'Park & Rec IG-Local',
              'm62':'Police Protect IG-Local',
              'm66':'Protective Insp & Reg IG-Local',
              'm67':'Public Welfare-Categorical IG-Local',
              
              'm68':'Public Welfare-Other IG-Local',
              
              'm79':'Public Welfare-NEC IG-Local',
              'm80':'Sewerage IG-Local',
              'm81':'Solid Waste manage IG-Local',
              'm87':'Sea & Inland Port IG-Local',
              'm89':'Gen Exp NEC IG-Local',
              'c589c':'Hospital IG-Local'}
    if not pd.isnull(row['c315']) and str(row['c315']) != '':
            total_exp = int(row['c315'])
            
            
    for item in expend:
        if not pd.isnull(row[item]) and str(row[item]) != '':
            total += int(row[item])
            rank[item] = int(row[item])
        else:
            # rank[item] = 0
            # total += 0
            rank[item] = None

    return total/total_exp

#Calculates and returns a tuple containing the share of total revenue from sources of revenue by levels of government
#mode is simply added in case of future uses for other csv formats
def sum_rank_rev(row, mode = 'historic revenue'):
    rank = {}
    
    rank_dict = {}
    total_rev = 0
    rev = []
    
    if mode == 'historic revenue':
        
        rev = ['C156',
                    'C168',
                    'C139']
    
    if 'historic' in mode:
        if not pd.isnull(row['C138']) and str(row['C138']) != '':
                total_rev = int(row['C138'])
            
            
    for item in rev:
        if not pd.isnull(row[item]) and str(row[item]) != '':
            rank[item] = int(row[item])
        else:

            rank[item] = None
    rank_dict = rank.copy()
    for i in rank.keys():
        if total_rev != 0:
            rank[i] = rank[i]/total_rev
        else:
            rank[i] = 0

    return (rank, rank_dict)


#Creates histogram and summary stats of school district intergovernmental revenue sources
def school_ig_rev(df):
    rev_dict = {'C156':'IGR State',
                'C168':'IGR Local',
                'C139':'IGR Federal',
                'C138':'Total IGR'}
    year = 2012
    rows = df.loc[df['Year4'] == year].copy()
    rows['sum_expend_diff'] = rows.apply (lambda row: sum_rank_rev(row,'historic revenue'), axis=1)

    t= 0
    gt = 0
    rank = {}
    er = 0
    
    rank_list = {}
    # print(len(rows['ID']))
    # print(len(rows['sum_expend_diff']))
    for x,y in zip(rows['sum_expend_diff'],rows['ID']):
        gt+=1
        if str(str(y)[2]) == '5':

            if x[0] is not None and not pd.isnull(x):
                t+= 1
                for i in x[0].keys():
                    if i in rank:                        
                        if x[0][i] is not None:
                            rank_list[i][0].append(x[0][i])
                            rank_list[i][1] += 1
                            rank[i] += x[0][i]
                    else:
                        if x[0][i] is not None:
                            rank_list[i] = [[x[0][i]],1]
                            rank[i] = x[0][i]

    # print(t,gt)
    # print("er", er)
    for i in rank.keys():
        rank[i]= rank[i]/t
    sort_rank = sorted(rank.items(),
                       key=lambda x: x[1],
                       reverse = True)
    
    
   
    table_list = []
    headers = ['Name','mean','min','max','std','Q1','median','Q3','count']
    for i in sort_rank:
        table_list.append([rev_dict[i[0]],i[1],min(rank_list[i[0]][0]),max(rank_list[i[0]][0]),statistics.stdev(rank_list[i[0]][0]),np.quantile(rank_list[i[0]][0],.25),statistics.median(rank_list[i[0]][0]),np.quantile(rank_list[i[0]][0],.75),rank_list[i[0]][1]] )
        # print(mean(rank_list[i[0]][0]),i[1],rev_dict[i[0]])
        # print(np.percentile(rank_list[i[0]][0],[25, 50, 75,80,90,99]))
        
        plt.hist(rank_list[i[0]][0], 'auto')
        plt.title(rev_dict[i[0]] +' Year ' + str(year))
        if not os.path.exists(project_folder + '/Histogram_school_master_auto/'+ str(year) + '/'):
            os.makedirs(project_folder + '/Histogram_school_master_auto/'+ str(year) + '/')
        plt.savefig(project_folder + '/Histogram_school_master_auto/' + str(year) + '/' + rev_dict[i[0]] + str(year) + '.png')
        plt.show()
        

        
        
        
    df = pd.DataFrame(table_list, columns = headers)
    df = df.set_index('Name')
    df = df.round(2)
    with open('school.tex','w') as tf:
        tf.write(df.to_latex(float_format="{:0.2f}".format))
    
    
#Creates summary stats of expenditures made by school districts
def school_exp(df):
    
    expend_dict ={'C315':'General Expenditure',
              'C327':'General Current Expenditure',
        'C350':'Air Transportation',
        'C365':'Misc Commercial Activities',
        'C391':'Corrections',
        'C406':'Education',
        'C472':'Employ Secur Admin',
        'C478':'Financial Administration',
        'C493':'Fire Protection',
        'C508':'Judicial & Legal',
        'C529':'Central Staff Service',
        'C551':'General Public Buildings',
        'C562':'Health',
        'C577':'Hospitals',
        'C603':'Highways',
        'C650':'Transit Subsidies',
        'C660':'Housing & Community Dev',
        'C675':'Libraries',
        'C740':'Natural Resources',
        'C755':'Parking Facilities',
        'C770':'Parks & Recreation',
        'C785':'Police Protection',
        'C800':'Protective Inspection & Reg',
        'C815':'Public Welfare',
        'C878':'Sewerage',
        'C893':'Solid Waste Management',
        'C916':'Sea & Inland Port Facilities',
        'I89':'Interest on Gen Debt',
        'C938':'Gen Exp NEC'
        }
    year = 2012
    rows = df.loc[df['Year4'] == year].copy()
    rows['sum_expend_diff'] = rows.apply (lambda row: sum_rank_expend(row,'historic'), axis=1)

    t= 0
    gt = 0
    rank = {}
    er = 0
    
    rank_list = {}
    print(len(rows['ID']))
    print(len(rows['sum_expend_diff']))
    for x,y in zip(rows['sum_expend_diff'],rows['ID']):
    # for x,y in zip(rows['sum_expend_diff'],rows['id']):
        gt+=1
        if str(str(y)[2]) == '5':
            # print("hey")
        # or str(str(y)[2]) == '3':
            # print(y)
        # if str(y[2]) == '2':
            if x[0] is not None and not pd.isnull(x):
                t+= 1
                for i in x[0].keys():
                    if i in rank:
                        # if x[0][i] is not None
                        
                        if x[0][i] is not None:
                            rank_list[i][0].append(x[0][i])
                            rank_list[i][1] += 1
                            rank[i] += x[0][i]
                            #Use this to manually check for outliers
                            # if(x[0][i] > 0.5):
                            #     print(str(y),i, x[0][i])
                            #     er+= 1
                    else:
                        if x[0][i] is not None:
                            rank_list[i] = [[x[0][i]],1]
                            rank[i] = x[0][i]
            #Use this if you want summary statistic for the raw value
            # if x[1] is not None and not pd.isnull(x):
            #     for i in x[1].keys():
            #         if i in rank_list:
            #             rank_list[i].append(x[1][i])
            #         else:
            #             rank_list[i] = [x[1][i]]
    print(t,gt)
    print("er", er)
    for i in rank.keys():
        rank[i]= rank[i]/t
    sort_rank = sorted(rank.items(),
                       key=lambda x: x[1],
                       reverse = True)
    
    
   
    table_list = []
    headers = ['Name','mean','min','max','std','Q1','median','Q3','count']
    for i in sort_rank:
        table_list.append([expend_dict[i[0]],i[1],min(rank_list[i[0]][0]),max(rank_list[i[0]][0]),statistics.stdev(rank_list[i[0]][0]),np.quantile(rank_list[i[0]][0],.25),statistics.median(rank_list[i[0]][0]),np.quantile(rank_list[i[0]][0],.75),rank_list[i[0]][1]] )
        # print(mean(rank_list[i[0]][0]),i[1],expend_dict[i[0]])
        # print(np.percentile(rank_list[i[0]][0],[25, 50, 75,80,90,99]))
        
        plt.hist(rank_list[i[0]][0], 'auto')
        plt.title(expend_dict[i[0]] +' Year ' + str(year))
        if not os.path.exists(project_folder + '/Histogram_school_master_auto/'+ str(year) + '/'):
            os.makedirs(project_folder + '/Histogram_school_master_auto/'+ str(year) + '/')
        plt.savefig(project_folder + '/Histogram_school_master_auto/' + str(year) + '/' + expend_dict[i[0]] + str(year) + '.png')
        
        plt.show()
        

        
        
        
    df = pd.DataFrame(table_list, columns = headers)
    df = df.set_index('Name')
    df = df.round(2)
    with open('schoolexp.tex','w') as tf:
        tf.write(df.to_latex(float_format="{:0.2f}".format))

#creates tex table of the summary stats of education expenditures in DESC order, also creates a histogram
def education_expend(df):
    expend_dict = {
        'C416':'Elem & Secondary Capital Outlays',
        'C415':'Elem & Secondary Current Operations',
        'C413':'Elem & Secondary IG Expenditure',
        'C442':'Higher Ed Capital Outlays',
        'C441':'Higher Ed Current Operations',
        'C439':'Higher Ed IG Expenditure',
        'C460':'Ed NEC Capital Outlays',
        'C459':'Ed NEC Current Operations',
        'E19':'Ed NEC Assistance and Subsidies',
        'C457':'Ed NEC IG Expenditure'
        }
    year = 2012
    rows = df.loc[df['Year4'] == year].copy()
    rows['sum_expend_diff'] = rows.apply (lambda row: sum_education(row), axis=1)

    t= 0
    rank = {}
    
    rank_list = {}
    for x,y in zip(rows['sum_expend_diff'],rows['ID']):
        if str(str(y)[2]) == '5':
            if x[0] is not None and not pd.isnull(x):
                t+= 1
                for i in x[0].keys():
                    if i in rank:                        
                        if x[0][i] is not None:
                            rank_list[i][0].append(x[0][i])
                            rank_list[i][1] += 1
                            rank[i] += x[0][i]
                            #Use this to manually check for outliers
                            # if(x[0][i] > 0.5):
                            #     print(str(y),i, x[0][i])
                            #     er+= 1
                    else:
                        if x[0][i] is not None:
                            rank_list[i] = [[x[0][i]],1]
                            rank[i] = x[0][i]
    for i in rank.keys():
        rank[i]= rank[i]/t
    sort_rank = sorted(rank.items(),
                       key=lambda x: x[1],
                       reverse = True)
    
    
   
    table_list = []
    headers = ['Name','mean','min','max','std','Q1','median','Q3','count']
    for i in sort_rank:
        table_list.append([expend_dict[i[0]],i[1],min(rank_list[i[0]][0]),max(rank_list[i[0]][0]),statistics.stdev(rank_list[i[0]][0]),np.quantile(rank_list[i[0]][0],.25),statistics.median(rank_list[i[0]][0]),np.quantile(rank_list[i[0]][0],.75),rank_list[i[0]][1]] )
        # print(mean(rank_list[i[0]][0]),i[1],expend_dict[i[0]])
        # print(np.percentile(rank_list[i[0]][0],[25, 50, 75,80,90,99]))
        plt.hist(rank_list[i[0]][0], 'auto')
        plt.title(expend_dict[i[0]] +' Year ' + str(year))
        if not os.path.exists(project_folder + '/Histogram_school_exp_breakdown_auto/'+ str(year) + '/'):
            os.makedirs(project_folder + '/Histogram_school_exp_breakdown_auto/'+ str(year) + '/')
        plt.savefig(project_folder + '/Histogram_school_exp_breakdown_auto/' + str(year) + '/' + expend_dict[i[0]] + str(year) + '.png')
        plt.show()
        
    df = pd.DataFrame(table_list, columns = headers)
    df = df.set_index('Name')
    df = df.round(2)
    with open('school_educ_exp_breakdown.tex','w') as tf:
        tf.write(df.to_latex(float_format="{:0.2f}".format))
        
#Used to manually sum all education expenditures
def sum_education(row):
    rank = {}
    rank_dict = {}
    total_exp = 0
    
    exp = [
        'C416',
        'C415',
        'C413',
        'C442',
        'C439',
        'C441',
        'C460',
        'C459',
        'E19',
        'C457'
        ]
    
    if not pd.isnull(row['C315']) and str(row['C315']) != '':
                total_exp = int(row['C315'])
    
    # if not pd.isnull(row['C406']) and str(row['C406']) != '':
    #             total_exp = int(row['C406'])
            
            
    for item in exp:
        if item == 'C415':
            rank[item] = 0
            if not pd.isnull(row['C414']) and str(row['C414']) != '':
                rank['C415'] += int(row['C414'])
                if not pd.isnull(row['C416']) and str(row['C416']) != '':
                    rank['C415'] = rank['C415'] - int(row['C416'])
        elif item =='C413':
            rank[item] = 0
            if not pd.isnull(row['C412']) and str(row['C412']) != '':
                rank['C413'] += int(row['C412'])
                if not pd.isnull(row['C414']) and str(row['C414']) != '':
                    rank['C413'] = rank['C413'] - int(row['C414'])
        elif item == 'C441':
            rank[item] = 0
            if not pd.isnull(row['C440']) and str(row['C440']) != '':
                rank['C441'] += int(row['C440'])
                if not pd.isnull(row['C442']) and str(row['C442']) != '':
                    rank['C441'] = rank['C441'] - int(row['C442'])
        elif item == 'C439':
            rank[item] = 0
            if not pd.isnull(row['C438']) and str(row['C438']) != '':
                rank['C439'] += int(row['C438'])
                if not pd.isnull(row['C440']) and str(row['C440']) != '':
                    rank['C439'] = rank['C439'] - int(row['C440'])
        elif item == 'C459':
            rank[item] = 0
            if not pd.isnull(row['C458']) and str(row['C458']) != '':
                rank['C459'] += int(row['C458'])
                if not pd.isnull(row['E19']) and str(row['E19']) != '':
                    rank['C459'] = rank['C459'] - int(row['E19'])
                    if not pd.isnull(row['C460']) and str(row['C460']) != '':
                        rank['C459'] = rank['C459'] - int(row['C460'])
        elif item == 'C457':
            rank[item] = 0
            if not pd.isnull(row['C456']) and str(row['C456']) != '':
                rank['C457'] += int(row['C456'])
                if not pd.isnull(row['C458']) and str(row['C458']) != '':
                    rank['C457'] = rank['C457'] - int(row['C458'])
        elif not pd.isnull(row[item]) and str(row[item]) != '':
            rank[item] = int(row[item])
        else:

            rank[item] = None
    rank_dict = rank.copy()
    for i in rank.keys():
        if total_exp != 0:
            rank[i] = rank[i]/total_exp
        else:
            rank[i] = 0

    return (rank, rank_dict)

#Creates summary stats of intergovernmental expenditures to local governments
def local_e(historic):
    
    expend_dict = {'m01':'Air Trans IG-Local',
              'm05':'Corrections IG-Local',
              'm12':'Elementary & Sec IG-Local',
              'm18':'Higher Ed IG-Local',
              'm21':'Other Ed IG-Local',
              'm23':'Financial Admin IG-Local',
              'm24':'Fire Protection IG-Local',
              'm25':'Judicial & Legal IG-Local',
              'm29':'Central Staff IG-Local',
              'm32':'Health IG-Local',
              'm38':'Other Hospital IG-Local',
              'm44':'Reg Highway IG-Local',
              'm47':'Transit Subsidies IG-Local',
              'm50':'Housing & Community Dev IG-Local',
              'm52':'Libraries IG-Local',
              'm59':'Natural Resources IG-Local',
              'm60':'Parking Facilities IG-Local',
              'm61':'Park & Rec IG-Local',
              'm62':'Police Protect IG-Local',
              'm66':'Protective Insp & Reg IG-Local',
              'm67':'Public Welfare-Categorical IG-Local',
              
              'm68':'Public Welfare-Other IG-Local',
              
              'm79':'Public Welfare-NEC IG-Local',
              'm80':'Sewerage IG-Local',
              'm81':'Solid Waste manage IG-Local',
              'm87':'Sea & Inland Port IG-Local',
              'm89':'Gen Exp NEC IG-Local',
              'c589c':'Hospital IG-Local'}
    year = 2017
    rows = historic.loc[historic['year4'] == year].copy()
    # print(rows)
    rows['sum_expend_diff'] = rows.apply (lambda row: sum_local(row), axis=1)
    # results = []
    
    # s = 0
    # d = 0
    t= 0
    gt = 0
    er = 0
    
    rank_list = []
    print(len(rows['id']))
    print(len(rows['sum_expend_diff']))
    for x,y in zip(rows['sum_expend_diff'],rows['id']):
    # for x,y in zip(rows['sum_expend_diff'],rows['id']):
        gt+=1
        if str(str(y)[2]) == '3':
        # or str(str(y)[2]) == '3':
            # print(y)
        # if str(y[2]) == '2':
            if x > 0.5:
                print(y)
            if x is not None and not pd.isnull(x):
                t+= 1
                
                if x is not None:
                    rank_list.append(x)
                
            #Use this if you want summary statistic for the raw value
            # if x[1] is not None and not pd.isnull(x):
            #     for i in x[1].keys():
            #         if i in rank_list:
            #             rank_list[i].append(x[1][i])
            #         else:
            #             rank_list[i] = [x[1][i]]
    print(t,gt)
    print("er", er)
    
   
    # n = 0
    # t = 0
    table_list = []
    headers = ['Name','mean','min','max','std','Q1','median','Q3','count']
    # for i in sort_rank:
    table_list.append(['Local IG divided by Gen Exp',mean(rank_list),min(rank_list),max(rank_list),statistics.stdev(rank_list),np.quantile(rank_list,.25),statistics.median(rank_list),np.quantile(rank_list,.75),len(rank_list)] )
    # print(mean(rank_list[i[0]][0]),i[1],expend_dict[i[0]])
    # print(np.percentile(rank_list[i[0]][0],[25, 50, 75,80,90,99]))
    
    plt.hist(rank_list, 'auto')
    plt.title(' Local IG divided by Gen Exp ' + str(year))
    if not os.path.exists(project_folder + '/Histogram_balanced_mid_IGL/'+ str(year) + '/'):
        os.makedirs(project_folder + '/Histogram_balanced_mid_IGL/'+ str(year) + '/')
    plt.savefig(project_folder + '/Histogram_balanced_mid_IGL/' + str(year) + '/' + 'Local IG divided by Gen Exp' + str(year) + '.png')
    
    plt.show()
    

        
    # print("Average ", t/n)
    # print("Count ",n)
    print("Functional Code Table For Cities")
    df = pd.DataFrame(table_list, columns = headers)
    df = df.set_index('Name')
    print(df)
    df = df.round(2)
    # df = df.round({'min':0})
    # print(df)
    # df.to_csv(project_folder +'/2012_1967/'+ 'sumstatstate.csv')
    with open('test.tex','w') as tf:
        tf.write(df.to_latex(float_format="{:0.2f}".format))
        
#formated to take in STATA created variable names, creates a summary stat for (currently) expenditures of all cities
def rank_expend(historic):
    
    
    expend_dict ={'c315':'General Expenditure',
              'c327':'General Current Expenditure',
        'c350':'Air Transportation',
        'c365':'Misc Commercial Activities',
        'c391':'Corrections',
        'c406':'Education',
        'c472':'Employ Secur Admin',
        'c478':'Financial Administration',
        'c493':'Fire Protection',
        'c508':'Judicial & Legal',
        'c529':'Central Staff Service',
        'c551':'General Public Buildings',
        'c562':'Health',
        'c577':'Hospitals',
        'c603':'Highways',
        'c650':'Transit Subsidies',
        'c660':'Housing & Community Dev',
        'c675':'Libraries',
        'c740':'Natural Resources',
        'c755':'Parking Facilities',
        'c770':'Parks & Recreation',
        'c785':'Police Protection',
        'c800':'Protective Inspection & Reg',
        'c815':'Public Welfare',
        'c878':'Sewerage',
        'c893':'Solid Waste Management',
        'c916':'Sea & Inland Port Facilities',
        'i89':'Interest on Gen Debt',
        'c938':'Gen Exp NEC'
        }
    #Following are different dictionaries that can be used for different variable name format or different categories of expenditure
    #Will later add an option to function to select the desired dictionary
    
    # expend_dict ={'C315':'General Expenditure',
    #           'C327':'General Current Expenditure',
    #     'C350':'Air Transportation',
    #     'C365':'Misc Commercial Activities',
    #     'C391':'Corrections',
    #     'C406':'Education',
    #     'C472':'Employ Secur Admin',
    #     'C478':'Financial Administration',
    #     'C493':'Fire Protection',
    #     'C508':'Judicial & Legal',
    #     'C529':'Central Staff Service',
    #     'C551':'General Public Buildings',
    #     'C562':'Health',
    #     'C577':'Hospitals',
    #     'C603':'Highways',
    #     'C650':'Transit Subsidies',
    #     'C660':'Housing & Community Dev',
    #     'C675':'Libraries',
    #     'C740':'Natural Resources',
    #     'C755':'Parking Facilities',
    #     'C770':'Parks & Recreation',
    #     'C785':'Police Protection',
    #     'C800':'Protective Inspection & Reg',
    #     'C815':'Public Welfare',
    #     'C878':'Sewerage',
    #     'C893':'Solid Waste Management',
    #     'C916':'Sea & Inland Port Facilities',
    #     'I89':'Interest on Gen Debt',
    #     'C938':'Gen Exp NEC'
    #     }
    # expend_dict ={'C315':'General Expenditure',
    #           'C327':'General Current Expenditure',
    #     'C350':'Total Air Transportation',
    #     'C365':'Total Misc Commercial Activities',
    #     'C391':'Total Corrections',
    #     'C406':'Total Education',
    #     'C472':'Total Employ Secur Admin',
    #     'C478':'Total Financial Administration',
    #     'C493':'Total Fire Protection',
    #     'C508':'Total Judicial & Legal',
    #     'C529':'Total Central Staff Service',
    #     'C551':'Total General Public Buildings',
    #     'C562':'Total Health',
    #     'C577':'Total Hospitals',
    #     'C603':'Total Highways',
    #     'C650':'Total Transit Subsidies',
    #     'C660':'Total Housing & Community Dev',
    #     'C675':'Total Libraries',
    #     'C740':'Total Natural Resources',
    #     'C755':'Total Parking Facilities',
    #     'C770':'Total Parks & Recreation',
    #     'C785':'Total Police Protection',
    #     'C800':'Total Protective Inspection & Reg',
    #     'C815':'Total Public Welfare',
    #     'C878':'Total Sewerage',
    #     'C893':'Total Solid Waste Management',
    #     'C916':'Total Sea & Inland Port Facilities',
    #     'I89':'Total Interest on Gen Debt',
    #     'C938':'Total Gen Exp NEC'
    #     }
    # e_prefix = {
    #     'E19a':'Tot Educ Assistance & Subsidies',
    #     'E19': 'Other Educ Assistance & Subsidies',
    #     'E47':'Direct Subsidies to Private Transit Co',
    #     'E67':'Pub Welfare Cash Assistance Payments',
    #     'E68':'Other Pub Welfare Cash Assistance Payments',
    #     'E74':'Vendor Payment for Medical Care',
    #     'E75':'Vendor Payment for Other',
    #     'E84':'State Veterans Assistance-Current Op'
    #     }
    
    # local = {'m01':'Air Trans IG-Local',
    #           'm05':'Corrections IG-Local',
    #           'm12':'Elementary & Sec IG-Local',
    #           'm18':'Higher Ed IG-Local',
    #           'm21':'Other Ed IG-Local',
    #           'm23':'Financial Admin IG-Local',
    #           'm24':'Fire Protection IG-Local',
    #           'm25':'Judicial & Legal IG-Local',
    #           'm29':'Central Staff IG-Local',
    #           'm32':'Health IG-Local',
    #           'm38':'Other Hospital IG-Local',
    #           'm44':'Reg Highway IG-Local',
    #           'm47':'Transit Subsidies IG-Local',
    #           'm50':'Housing & Community Dev IG-Local',
    #           'm52':'Libraries IG-Local',
    #           'm59':'Natural Resources IG-Local',
    #           'm60':'Parking Facilities IG-Local',
    #           'm61':'Park & Rec IG-Local',
    #           'm62':'Police Protect IG-Local',
    #           'm66':'Protective Insp & Reg IG-Local',
    #           'm67':'Public Welfare-Categorical IG-Local',
              
    #           'm68':'Public Welfare-Other IG-Local',
              
    #           'm79':'Public Welfare-NEC IG-Local',
    #           'm80':'Sewerage IG-Local',
    #           'm81':'Solid Waste manage IG-Local',
    #           'm87':'Sea & Inland Port IG-Local',
    #           'm89':'Gen Exp NEC IG-Local',
    #           'c589c':'Hospital IG-Local'}
    
    # state = {'L01':'Air Trans IG-State',
    #          'L05':'Corrections IG-State',
    #          'L12':'Elementary & Sec IG-State',
    #          'L18':'Higher Ed IG-State',
    #          'L21':'Other Ed IG-State',
    #          'L23':'Financial Admin IG-State',
    #          'L24':'Fire Protection IG-State',
    #          'L25':'Judicial & Legal IG-State',
    #          'L29':'Central Staff IG-State',
    #          'L32':'Health IG-State',
    #          'L38':'Other Hospital IG-State',
    #          'L44':'Reg Highway IG-State',
    #          'L47':'Transit Subsidies IG-State',
    #          'L50':'Housing & Community Dev IG-State',
    #          'L52':'Libraries IG-State',
    #          'L59':'Natural Resources IG-State',
    #          'L60':'Parking Facilities IG-State',
    #          'L61':'Park & Rec IG-State',
    #          'L62':'Police Protect IG-State',
    #          'L66':'Protective Insp & Reg IG-State',
    #          'L67':'Public Welfare-Categorical IG-State',
    #          'L79':'Public Welfare-NEC IG-State',
    #          'L80':'Sewerage IG-State',
    #          'L81':'Solid Waste Manage IG-State',
    #          'L87':'Sea & Inland Port IG-State',
    #          'L89':'Gen Exp NEC IG-State',
    #          'C589b':'Hospital IG-State'
    #          }
    # rows = historic
    # year = 'all_years'
    # year = 2017
    # rows = historic.loc[historic['year4'] == year].copy()
    rows = historic 
    year_dict = {}
    for x,y in zip(rows['year4'],rows['id']):
        if x not in year_dict:
            year_dict[x] = [y]
        else:
            year_dict[x].append(y)
    for x in year_dict:
        print(len(year_dict.keys()))
        print(x, len(year_dict[x]))
        
    # print(rows)
    rows['sum_expend_diff'] = rows.apply (lambda row: sum_rank_expend(row,'stata'), axis=1)
    # results = []
    
    # s = 0
    # d = 0
    t= 0
    gt = 0
    rank = {}
    er = 0
    
    rank_list = {}
    print(len(rows['id']))
    print(len(rows['sum_expend_diff']))
    for x,y in zip(rows['sum_expend_diff'],rows['id']):
    # for x,y in zip(rows['sum_expend_diff'],rows['id']):
        gt+=1
        if str(str(y)[2]) == '2' or str(str(y)[2]) == '3':
        # or str(str(y)[2]) == '3':
            # print(y)
        # if str(y[2]) == '2':
            if x[0] is not None and not pd.isnull(x):
                t+= 1
                for i in x[0].keys():
                    if i in rank:
                        # if x[0][i] is not None
                        
                        if x[0][i] is not None:
                            rank_list[i][0].append(x[0][i])
                            rank_list[i][1] += 1
                            rank[i] += x[0][i]
                            # if(x[0][i] > 0.5):
                            #     print(str(y),i, x[0][i])
                            #     er+= 1
                    else:
                        if x[0][i] is not None:
                            rank_list[i] = [[x[0][i]],1]
                            rank[i] = x[0][i]
        else:
            print(y)
            #Use this if you want summary statistic for the raw value
            # if x[1] is not None and not pd.isnull(x):
            #     for i in x[1].keys():
            #         if i in rank_list:
            #             rank_list[i].append(x[1][i])
            #         else:
            #             rank_list[i] = [x[1][i]]
    print(t,gt)
    print("er", er)
    for i in rank.keys():
        rank[i]= rank[i]/t
    sort_rank = sorted(rank.items(),
                       key=lambda x: x[1],
                       reverse = True)
    
    
   
    n = 0
    t = 0
    table_list = []
    headers = ['Name','mean','min','max','std','Q1','median','Q3','count']
    for i in sort_rank:
        table_list.append([expend_dict[i[0]],i[1],min(rank_list[i[0]][0]),max(rank_list[i[0]][0]),statistics.stdev(rank_list[i[0]][0]),np.quantile(rank_list[i[0]][0],.25),statistics.median(rank_list[i[0]][0]),np.quantile(rank_list[i[0]][0],.75),rank_list[i[0]][1]] )
        # print(mean(rank_list[i[0]][0]),i[1],expend_dict[i[0]])
        # print(np.percentile(rank_list[i[0]][0],[25, 50, 75,80,90,99]))
        
        # plt.hist(rank_list[i[0]][0], 'auto')
        # plt.title(expend_dict[i[0]] +' Year ' + str(year))
        # if not os.path.exists(project_folder + '/Histogram_balanced_mid_auto/'+ str(year) + '/'):
        #     os.makedirs(project_folder + '/Histogram_balanced_mid_auto/'+ str(year) + '/')
        # plt.savefig(project_folder + '/Histogram_balanced_mid_auto/' + str(year) + '/' + expend_dict[i[0]] + str(year) + '.png')
        
        # plt.show()
        

        
        n += 1
        t += i[1]
    print("Average ", t/n)
    print("Count ",n)
    print("Functional Code Table For Cities")
    df = pd.DataFrame(table_list, columns = headers)
    df = df.set_index('Name')
    print(df)
    df = df.round(2)
    # df = df.round({'min':0})
    # print(df)
    # df.to_csv(project_folder +'/2012_1967/'+ 'sumstatstate.csv')
    with open('test.tex','w') as tf:
        tf.write(df.to_latex(float_format="{:0.2f}".format))

#Used to calculate a tuple consisting of the different levels of government intergovernmental revenue and the total of all intergovernmental revenue
def sum_levels(row):
    total = 0
    local = 0
    state = 0
    federal = 0
    if 'C316' in row:  
        if not pd.isnull(row['C316']) and str(row['C316']) != '':
            total += int(row['C316'])
            state += int(row['C316'])
    if 'C317' in row:  
        if not pd.isnull(row['C317']) and str(row['C317']) != '':
            total += int(row['C317'])
            local += int(row['C317'])
    if 'C324' in row:  
        if not pd.isnull(row['C324']) and str(row['C324']) != '':
            total += int(row['C324'])
            federal += int(row['C324'])
            
    return (state,local,federal,total)

#Prints out the share of intergovernmental revenue by levels of government for 2012 
def compare_levels(historic):
    state = [0,0,0,0]
    county = [0,0,0,0]
    city = [0,0,0,0]
    town = [0,0,0,0]
    federal = [0,0,0,0]
    #Change this line '2012' to change what year you want the share to output
    rows = historic.loc[historic['Year4']=='2012'].copy()
    rows['compare_levels'] = rows.apply (lambda row: sum_levels(row), axis=1)
    for x,y in zip(rows['compare_levels'],rows['ID']):
        #State
        if y[2] == '0' and int(x[3]) != 0:
            state[0] += int(x[0])/int(x[3])
            state[1] += int(x[1])/int(x[3])
            state[2] += int(x[2])/int(x[3])
            state[3] += 1
        #county
        elif y[2] == '1' and int(x[3]) != 0:
            county[0] += int(x[0])/int(x[3])
            county[1] += int(x[1])/int(x[3])
            county[2] += int(x[2])/int(x[3])
            county[3] += 1
        #city
        elif y[2] == '2' and int(x[3]) != 0:
            city[0] += int(x[0])/int(x[3])
            city[1] += int(x[1])/int(x[3])
            city[2] += int(x[2])/int(x[3])
            city[3] += 1
        #Township
        elif y[2] == '3' and int(x[3]) != 0:
            town[0] += int(x[0])/int(x[3])
            town[1] += int(x[1])/int(x[3])
            town[2] += int(x[2])/int(x[3])
            town[3] += 1
        elif y[2] == '6' and int(x[3]) != 0:
            federal[0] += int(x[0])/int(x[3])
            federal[1] += int(x[1])/int(x[3])
            federal[2] += int(x[2])/int(x[3])
            federal[3] += 1
    if state[3] != 0:
        state[0] = state[0]/state[3]
        state[1] = state[1]/state[3]
        state[2] = state[2]/state[3]
    if county[3] != 0:
        county[0] = county[0]/county[3]
        county[1] = county[1]/county[3]
        county[2] = county[2]/county[3]
    if city[3] != 0:
        city[0] = city[0]/city[3]
        city[1] = city[1]/city[3]
        city[2] = city[2]/city[3]
    
    if town[3] != 0:
        town[0] = town[0]/town[3]
        town[1] = town[1]/town[3]
        town[2] = town[2]/town[3]
    print("(state,local,federal,count)")
    print("Federal",federal, "State",state,"County",county,"City",city,"Town",town)

#Compares the difference between the total of all functional expenditure to the general expenditure for 2012
def compare_expend(historic):
    #change the year for this to make it a different year
    rows = historic.loc[historic['Year4']=='2012'].copy()
    rows['sum_expend_diff'] = rows.apply (lambda row: sum_expend(row), axis=1)
    # results = []
    t = 0
    s = 0
    d = 0
    for x in rows['sum_expend_diff']:
        if x is not None and not pd.isnull(x):
            t+= 1
            if str(x) == 'Same':
                s+=1
                d+=0
            else:

                d+= x
    if d == 0 or t == 0:
        avgdiff = 0
        print("Maybe something went wrong?")
    else:
       avgdiff = d/t
    print("Functional Total compared to General Expenditure")
    print("Same for: ", s, " out of ", t)
    print("Average Percent diff: ", avgdiff)

#Helper function that returns a tuple of a dictionary "rank" of the percentage share of each expenditure and a dictionary
#rank_dict with the values of each expenditure category
def sum_rank_expend(row, mode):
    total = 0
    # actual = 0
    rank = {}
    
    rank_dict = {}
    total_exp = 0
    
    
    
    if mode == 'stata':
        expend = ['c350','c365','c391','c406',
                  'c472'
                  ,'c478','c493','c508','c529',
                  'c551','c562',
                  'c577',
                  'c603',
                  'c650','c660','c675','c740',
                  'c755','c770','c785','c800',
                  'c815',
                  'c878','c893','c916',
                  'i89','c938'
                  ]
    else:
        expend = ['C350','C365','C391','C406',
              'C472'
              ,'C478','C493','C508','C529',
              'C551','C562',
              'C577',
              'C603',
              'C650','C660','C675','C740',
              'C755','C770','C785','C800',
              'C815',
              'C878','C893','C916',
              'I89','C938'
              ]
    if mode == 'stata':
        if not pd.isnull(row['c315']) and str(row['c315']) != '':
                total_exp = int(row['c315'])
    else:
        if not pd.isnull(row['C315']) and str(row['C315']) != '':
                total_exp = int(row['C315'])
            
            
    for item in expend:
        if not pd.isnull(row[item]) and str(row[item]) != '':
            total += int(row[item])
            rank[item] = int(row[item])
        else:
            # New line
            # rank[item] = 0
            # total += 0
            rank[item] = None
    # if not pd.isnull(row['C315']) and str(row['C301']) != '':
    #         actual += int(row['C315'])
    rank_dict = rank.copy()
    for i in rank.keys():
        # if total != 0:
        #     if rank[i] is not None:
        #         # if rank[i] < 0:
        #         #     print(i)
        #         rank[i] = rank[i]/total
        #     else:
        #         rank[i] = None
        # else:
        #     return (None,None)
        
        if total_exp != 0:
            rank[i] = rank[i]/total_exp
        else:
            rank[i] = 0
            
            
            
        # if total != 0:
        #     rank[i] = rank[i]/total
        # else:
        #     rank[i] = 0
            
            
            # return (None, None)
    return (rank, rank_dict)
    
 #Creates kmeans clusters of the functional revenue categories of the 2012 data
def kmeans_functional(historic):
    col = ['UniqueID','T01','C107','C118','C129',
            'other','C139','C156','C168',
            'C183','C211']
    rev = ['T01','C107','C118','C129',
            'other','C139','C156','C168',
            'C183','C211']
    other = ['T50','T51','T53','T99']
    # col = [
    #     'UniqueID',
    #     'C350','C365','C391','C406',
    #           'C472'
    #           ,'C478','C493','C508','C529',
    #           'C551','C562',
    #           'C577',
    #           'C603',
    #           'C650','C660','C675','C740',
    #           'C755','C770','C785','C800',
    #           'C815',
    #           'C878','C893','C916',
    #           'I89','C938'
    #           ]
    # expend = ['C350','C365','C391','C406',
    #           'C472'
    #           ,'C478','C493','C508','C529',
    #           'C551','C562',
    #           'C577',
    #           'C603',
    #           'C650','C660','C675','C740',
    #           'C755','C770','C785','C800',
    #           'C815',
    #           'C878','C893','C916',
    #           'I89','C938'
    #           ]        nmjkiu
    # print(historic)
    
    #Change year to change year of data, sometimes it needs to be in string format
    rows = historic.loc[historic['Year4']== 2012].copy()
    #Calls helper function kmeans_list that calculates the share of each functional category of the total
    rows['kmeans'] = rows.apply (lambda row: kmeans_list(row), axis=1)
    kmeans_l = []
    
    for x,y in zip(rows['kmeans'],rows['ID']):
        if str(y[2]) == '2':
            if x is not None:
                kmeans_l.append(x)
    
    df = pd.DataFrame(kmeans_l, columns = col )
    df = df.fillna(0)
    kmeans = KMeans(n_clusters = 5)
    y = kmeans.fit_predict(df[rev])
    df['cluster'] = y
    print(kmeans.cluster_centers_)
    clusters = [[ '%.2f' % elem for elem in i ] for i in kmeans.cluster_centers_]
    print(clusters)
    df.to_csv(project_folder + '/2012_1967/' + 'clusters_rev.csv')
    print(df.head())
    print(df.tail())
    reduced = PCA(n_components = 2).fit_transform(df[rev])
    results = pd.DataFrame(reduced, columns = ['PCA1','PCA2'])
    
    sns.scatterplot(x="PCA1", y="PCA2", hue= df['cluster'], data=results)
    plt.title('K-means Clustering reduced to 2-D')

    
#helper function kmeans_list that calculates the share of each functional category of the total
def kmeans_list(row):
    total = 0
    func_list = []
    
    rev = ['T01','C107','C118','C129',
            'other','C139','C156','C168',
            'C183','C211']
    other = ['T50','T51','T53','T99']
    #option to calculate for expenditure will be added later
    
    # expend = ['C350','C365','C391','C406',
    #           'C472','C478','C493','C508',
    #           'C529',
    #           'C551','C562',
    #           'C577',
    #           'C603',
    #           'C650','C660','C675','C740',
    #           'C755','C770','C785','C800',
    #           'C815',
    #           'C878','C893','C916',
    #           'I89','C938']
    func_list.append(str(row['ID']) + str(row['Year4']))
    
    for item in rev:
        if item == 'other':
            subtotal = 0
            for i in other:
                if not pd.isnull(row[i]) and str(row[i]) != '':
                    subtotal += int(row[i])
            
            if subtotal != 0:
                total += subtotal
                func_list.append(subtotal/int(row['C101']))
            else:
                func_list.append(0)
                
        else:
            
            if not pd.isnull(row[item]) and str(row[item]) != '':
                if int(row[item]) != 0:
                    # print(int(row[item]),int(row['C101']))
                    func_list.append(int(row[item])/int(row['C101']))
                    total += int(row[item])
            else:
                func_list.append(0)
                
                
    # print(func_list)
    if total != 0:
        return func_list
    else:
        return None
#Sums all the individual expenditure category (without double counting) to compare to the existing general expenditure of census data
def sum_expend(row):
    total = 0
    actual = 0
    rank = {}
    expend = ['C350','C365','C391','C406',
              # 'C412','C438', 'C456',
              'C472'
              ,'C478','C493','C508','C529',
              'C551','C562',
              'C577',
              #'C582',
              #'C588',
              'C603',
              #'C608','C623',
              'C650','C660','C675','C740',
              'C755','C770','C785','C800',
              'C815',
              # 'C821','C831','E74',
              # 'E75','S74','C843','C858',
              'C878','C893','C916',
              'I89','C938'
              ]
    for item in expend:
        if not pd.isnull(row[item]) and str(row[item]) != '':
            total += int(row[item])
            rank[item] = int(row[item])
        else:
            rank[item] = 0
    if not pd.isnull(row['C315']) and str(row['C315']) != '':
            actual += int(row['C315'])

    # return rank
    
    if actual != 0 and total != 0:
        if total == actual:
            return 'Same'
        else:
            # print(abs(total-actual)/((actual+total)/2))
            return (total-actual)/((actual+total)/2)
    else:
        return None
#Prints out the percentage difference of the computed general expenditure and existing general expenditure for the given year  
def compare_expenditure(historic):
    rows = historic.loc[historic['Year4']=='2012'].copy()
    rows['sum_expend_diff'] = rows.apply (lambda row: sum_expenditure(row), axis=1)
    # results = []
    t = 0
    s = 0
    d = 0
    for x in rows['sum_expend_diff']:
        if x is not None and not pd.isnull(x):
            d+= x
            t+=1
            if int(x) == 0:
                s+=1
                
    # for x,y in zip(rows['sum_expend'],rows['C315']):
    #     if not pd.isnull(x) and not pd.isnull(y) and int(y) != 0 and int(x) != 0:
    #         if int(x) == int(y):
    #             s+=1
    #             t+=1
    #         else:
    #             t+=1
            
    #         d += abs(x-int(y))/int(y)
    
    # t = 0
    # s = 0
    # d = 0
    # for x in results:
    #     if x[1] == x[0]:
    #         s += 1
    #         t += 1
    #     else:
    #         t+= 1
    #     d += abs(x[0]-x[1])/x[0]
    avgdiff = d/t
    
    print("Same for: ", s, " out of ", t)
    print("Average Percent diff: ", avgdiff)
#Similar to sum_expend, but includes liquor categories
def sum_expenditure(row):
    #Does C406 include C412?
    items = ['C350', 'C365', 'C391','C412','C406','C412','C438', 'C456', 'C472','C478','C493','C508','C529','C551','C562','C577','C582','C588','C603','C608','C623','C650','C660','C675','C740','C755','C770','C785','C800','C815','C821','C831','E74','E75','S74','C843','C858','C878','C893','C916','I89','C938','C953','C959','C965','C974','C981','C988','C988','C995','C1000']
    total = 0
    actual = 0
    for x in items:
        if x in row:  
            if not pd.isnull(row[x]) and str(row[x]) != '':
                total += int(row[x])
    if 'C315' in row:  
        if not pd.isnull(row['C315']) and str(row['C315']) != '':
            actual += int(row['C315'])
            
    if actual != 0 and total != 0:
        
        return abs(total-actual)/((int(actual)+int(total))/2)
    else:
        return None
'''Runs various plots and calculates R^2 values between historical and current data formats, specifically
   Looks at 2012 because it occurs in both formats, checks how well the calculated totals from individual
   item codes compare to the actual totals entered within the historical data format
'''
#new = post 2012 format 2012 data with manuly added sums, and old is pre 2012 format 2012 data with manually added sums, old_c is pre 2012 data with existing item codes
#this time computed total revenue is compared to Total Revenue and General Revenue found in the historical data
def compare_revenue(old,new):
    
    old_prop = {}
    new_prop = {}
    old_cprop = {}
    old_genprop = {}
    for x,y in zip(new['ID'],new['tot_rev']):
        if str(x[2]) == '2' or str(x[2]) == '3':
            if str(y) != 'nan':
                if str(y) != '0':
                    # new_prop[x:-5] = y
                # print(x,y)
                    # print(x[:-5])
                    new_prop[x[:-5]] = int(y)
    
    for x,y,z in zip(old['ID'],old['Year4'], old['tot_rev']):
        if y == '2012':
            if str(x[2]) == '2' or str(x[2]) == '3':
                if str(z) != '0':
                    old_prop[x] = int(z)
                    
    for x,y,z in zip(old['ID'],old['Year4'], old['C101']):
        if y == '2012':
            if str(x[2]) == '2' or str(x[2]) == '3':
                if str(z) != '0':
                    old_cprop[x] = int(z)
                    
    for x,y,z in zip(old['ID'],old['Year4'], old['C103']):
        if y == '2012':
            if str(x[2]) == '2' or str(x[2]) == '3':
                if str(z) != '0':
                    old_genprop[x] = int(z)
                    
    # nl = []
    # ol = []
    # for keys in new_prop:
    #     if keys in old_prop.keys():
    #         nl.append(new_prop[keys])
    #         ol.append(old_prop[keys])

    # plt.scatter(nl,ol, color = 'r')
    # plt.title('tot_rev vs tot_rev')
    # plt.show()
    # slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(nl), np.array(ol))
    # print(slope,intercept, r_value, p_value, std_err)
    # print(r_value**2)
    
    ol_c = []
    ol = []
    t= 0
    s = 0
    for keys in old_prop:
        if keys in old_cprop.keys():
            ol_c.append(old_cprop[keys])
            ol.append(old_prop[keys])
            if old_prop[keys] != old_cprop[keys]:
                t += 1
            else:
                t += 1
                s += 1
    print('C101 vs Historic tot_rev')
    print("Same for ", s, "out of ", t)

    plt.scatter(ol_c,ol, color = 'r')
    plt.title('C101 vs Historic tot_rev')
    plt.show()
    slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(ol_c), np.array(ol))
    
    print("Slope",slope,"Intercept",intercept, "r_value",r_value,"p_value", p_value,"R^2",r_value**2, "std_err",std_err)
    # print(r_value**2)
    
    # nl = []
    # ol_c = []
    # for keys in new_prop:
    #     if keys in old_prop.keys():
    #         nl.append(new_prop[keys])
    #         ol_c.append(old_cprop[keys])

    # plt.scatter(nl,ol_c, color = 'r')
    # plt.title('New tot_rev vs C101')
    # plt.show()
    # slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(nl), np.array(ol_c))
    # print(slope,intercept, r_value, p_value, std_err)
    # print(r_value**2)
    
    ol_gen = []
    ol = []
    for keys in old_prop:
        if keys in old_cprop.keys():
            ol_gen.append(old_genprop[keys])
            ol.append(old_prop[keys])
            if old_genprop[keys] != old_cprop[keys]:
                t += 1
            else:
                t += 1
                s += 1
    print('C103 vs Historic tot_rev')
    print("Same for ", s, "out of ", t)
    plt.scatter(ol_gen,ol, color = 'r')
    plt.title('C103 vs Historic tot_rev')
    plt.show()
    slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(ol_gen), np.array(ol))
    print("Slope",slope,"Intercept",intercept, "r_value",r_value,"p_value", p_value,"R^2",r_value**2, "std_err",std_err)

#calculates max, min and median of the Total Insurance Trust Benefits for the year 2012
def analyze_insur(historic):
    
    rows = historic.loc[historic['Year4']=='2012'].copy()
    maximum = float("-inf")
    minimum = float("inf")
    values = []
    for x in rows['C313']:
        if x is not None and not pd.isnull(x):
            if x > maximum:
                maximum = x
            if x < minimum:
                minimum = x
            values.append(int(x))
    print("Max", maximum)
    print("Min", minimum)
    print("median", statistics.median(values))

#Ignore this function
def ig_exp(historic):
 
    rows = historic.loc[historic['Year4']=='2012'].copy()
    rows['sum_expend_diff'] = rows.apply (lambda row: sum_expend(row), axis=1)
    # results = []
    t = 0
    s = 0
    d = 0
    for x in rows['sum_expend_diff']:
        if x is not None and not pd.isnull(x):
            t+= 1
            if str(x) == 'Same':
                s+=1
                d+=0
            else:

                d+= x
    if d == 0 or t == 0:
        avgdiff = 0
        print("Maybe something went wrong?")
    else:
       avgdiff = d/t
    print("Functional Total compared to General Expenditure")
    print("Same for: ", s, " out of ", t)
    print("Average Percent diff: ", avgdiff)
#Compares computed sum of intergovernmetal revenue in state and local level to preexisting sums in the data
def compare_ig(historic):
    rows = historic.loc[historic['Year4']=='2012'].copy()
    rows['state_diff'] = rows.apply (lambda row: sum_ig_state(row), axis=1)
    rows['local_diff'] = rows.apply (lambda row: sum_ig_local(row), axis=1)
    # results = []
    t = 0
    s = 0
    d = 0
    for x in rows['state_diff']:
        if x is not None and not pd.isnull(x):
            t+= 1
            if str(x) == 'Same':
                s+=1
                d+=0
            else:

                d+= x
    if d == 0 or t == 0:
        avgdiff = 0
        print("Maybe something went wrong?")
    else:
       avgdiff = d/t
    print("Sum of Functional State IG vs C316")
    print("Same for: ", s, " out of ", t)
    print("Average diff: ", avgdiff)
    
    t = 0
    s = 0
    d = 0
    for x in rows['local_diff']:
        if x is not None and not pd.isnull(x):
            t+= 1
            if str(x) == 'Same':
                s+=1
                d+=0
            else:

                d+= x
    if d == 0 or t == 0:
        avgdiff = 0
        print("Maybe something went wrong?")
    else:
       avgdiff = d/t
    print("Sum of Functional Local IG vs C317")
    print("Same for: ", s, " out of ", t)
    print("Average Percent diff: ", avgdiff)

#Manual sum of intergovernmental state revenue
def sum_ig_state(row):
    total = 0
    actual = 0
    state = ['L01','L05','L12','L18',
             'L21','L23','L24','L25','L29',
             'L32','L38','L44','L47',
             'L50','L52','L59','L60',
             'L61','L62','L66','L67',
             'L79','L80','L81','L87',
             'L89',
             'C589b'
             ]
    
    # local = ['M01','M05','M12','M18',
    #          'M21','M23','M25','M29',
    #          'M32','M38','M44','M47',
    #          'M50','M52','M59','M60',
    #          'M61','M62','M66','M67',
    #          'M68',
    #          'M79','M80','M81','M87',
    #          'M89']
    for x in state:
        if x in row:  
            if not pd.isnull(row[x]) and str(row[x]) != '':
                total += int(row[x])
    if 'C316' in row:  
        if not pd.isnull(row['C316']) and str(row['C316']) != '':
            actual += int(row['C316'])
            
    if actual != 0 and total != 0:
        if total == actual:
            return 'Same'
        else:
            return total-actual
    
    else:
        return None
    
#Manual sum of intergovernmental local revenue

def sum_ig_local(row):
    total = 0
    actual = 0

    local = ['M01','M05','M12','M18',
              'M21','M23','M24','M25','M29',
              'M32','M38','M44','M47',
              'M50','M52','M59','M60',
              'M61','M62','M66','M67',
              'M68',
              'M79','M80','M81','M87',
              'M89','C589c']
    for x in local:
        if x in row:  
            if not pd.isnull(row[x]) and str(row[x]) != '':
                total += int(row[x])
    if 'C317' in row:  
        if not pd.isnull(row['C317']) and str(row['C317']) != '':
            actual += int(row['C317'])
            
    if actual != 0 and total != 0:
        if total == actual:
            return 'Same'
        else:
            return (total-actual)/((actual+total)/2)
    else:
        return None
if __name__ == '__main__':
    gid_iud_folder = '/gid_files/'
    indfin_folder = '/2012_1967/'
    user_guide_name = '/UserGuide.xls'
    #Creates a file in project_folder + '/2012_1967/' named 'post.csv'
    read_iud_gid(project_folder + gid_iud_folder)
    read_indfin_folder(indfin_folder)
    pickle_folder_to_std_format(indfin_folder)
    union_std_pickle(indfin_folder)
    union_abc_pickle(indfin_folder)
    abc_to_itemcode(indfin_folder,user_guide_name)
    
    unpickled_df = pd.read_csv(project_folder + '/2012_1967/fincodename.csv')
    print(unpickled_df)
    post = pd.read_pickle(project_folder + '/gid_files/post.pkl')
    post = post.reset_index()
    print(post)
    
    master = post.append([unpickled_df], ignore_index = True)
    dropbox = os.path.expanduser("~/Dropbox/Unfundedpension/src/int")
    filepath = dropbox + '/master.csv'
    print("master before formatting")
    print(master)
    master.to_csv(filepath)
    #You need to have formatter_pickle.py to do this part
    import formatter_pickle as helper
    helper.format_master()

    print(post)
    print(master)
    
    import pandas as pd
    import os
    dropbox = os.path.expanduser("~/Dropbox/Unfundedpension/src/int")
    master = pd.read_pickle(dropbox + '/master_formatted_extended.pkl')    
    print(master['Year4'].unique())
    print(master)
    
    
