# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 12:15:07 2021

@author: One
"""

import pandas as pd
import os
dropbox = os.path.expanduser("~/Dropbox/Unfundedpension/src/int/")
#master = pd.read_pickle(dropbox + '/master_formatted.pkl')    
master = pd.read_pickle(dropbox + '/master_revised_test.pkl')  
# master[master['Year4']== '2010']
# master[master['Year4'] == '2014']
master['Fixed_ID'] = master['UniqueID'].str[:-4]
ids = master['Fixed_ID'].unique()

state_map = {}
county_map = {}

#This chunk is the part that makes the dictionary, run this chunk only with the code above
#to create a state_map
for cid in ids:
    #print(cid)
    if len(cid) == 9:
        for x in range(2012, 1999, -1):
            if len(master[master['UniqueID']== cid + str(x)]['FIPS Code-State']) < 1:
                continue
            else:
                state_map[cid] = master[master['UniqueID']== cid + str(x)]['FIPS Code-State'].values[0]
                
        # for x in range(2012, 1999, -1):
        #     if len(master[master['UniqueID'] == cid + str(x)]['FIP county code']) < 1:
        #         continue
        #     elif np.isnan(master[master['UniqueID'] == cid + str(x)]['FIP county code'].values[0]):
        #         continue
        #     else:
        #         county_map[cid] = master[master['UniqueID'] == cid + str(x)]['FIP county code'].values[0]
        # print(cid)
        
for cid in ids:
    if len(cid) == 9:
        for x in range(2012, 1999, -1):
            if len(master[master['UniqueID']== cid + str(x)]) < 1:
                continue
            else:
                master[master['UniqueID']== cid + str(x)]['FIPS Code-State'] = state_map[cid]
                
master.to_pickle(dropbox + 'master_mapped.pkl')