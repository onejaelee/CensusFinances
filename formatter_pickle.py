# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 15:37:26 2021

@author: One
"""
import pandas as pd
import numpy as np
import os
def format_master():
    print("Formatter Pickle")
    dropbox = os.path.expanduser("~/Dropbox/Unfundedpension/src/int")
    file_path = dropbox + '/master.csv'
    
    master = pd.read_csv(file_path, low_memory = False,dtype = {'UniqueID':'string','Year4':'string', 'ID':'string'})
    print(master)
    master['UniqueID']=master['UniqueID'].apply(lambda x: str(x) if len(x) == 13 else '0' + str(x))
    print(master['UniqueID'])
    master['UniqueID'] = master.UniqueID.astype("string")
    print(master['UniqueID'].dtypes)
    
    print(master['FIPS Code-State'].unique())
    idx_label = master[master['FIPS Code-State'] == ' '].index.tolist()
    for x in idx_label:
        #Change this based on how you want Federal Government Data to be classified as
        master.loc[x,'FIPS Code-State'] = '99'
    print(master['FIPS Code-State'].unique())
    #Need to work on fixing this condition's UniqueID's data
    idx_label = master[master['FIPS Code-State'] == '0'].index.tolist()
    for x in idx_label:
        master.loc[x,'FIPS Code-State'] = '18'
    print(master['FIPS Code-State'].unique())
    
    df_nan = master[master['FIPS Code-State'].isnull()]
    master = master.drop(df_nan.index, axis=0)
    
    print(master['FIPS Code-State'].unique())
    master = master.astype({"FIPS Code-State": float})
    master['FIPS Code-State'] = master['FIPS Code-State'].apply(np.int64)
    print(master['FIPS Code-State'].unique())
    master['FIPS Code-State'] = master['FIPS Code-State'].astype(str)
    print(master['FIPS Code-State'].unique())
    
    idx_label = master[master['FIPS Code-State'].str.len() == 1].index.tolist()
    for x in idx_label:
        master.loc[x,'FIPS Code-State'] = '0' + master.loc[x,'FIPS Code-State']
    try:
        master = master.drop(columns = ['Unnamed: 0'])
    except:
        print("unnamed column does not exist")
    print(master['FIPS Code-State'].unique())
    print(master)
    master.to_pickle(dropbox + '/master_formatted.pkl')
format_master()


