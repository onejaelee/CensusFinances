# -*- coding: utf-8 -*-
"""
Created on Sat Aug  7 20:26:35 2021

@author: One
"""
import pandas as pd
import os
import numpy as np

dropbox = os.path.expanduser("~/Dropbox/Unfundedpension/")
project_folder = os.path.expanduser("~/Dropbox/Unfundedpension/src/raw/cog/gid_files/")
folder = project_folder + "/additional_years/"
codes = dropbox + "/src/raw/cog/2012_1967/GOVS_ID_to_FIPS_Place_Codes_2012.xls"

crosswalk_file = os.path.expanduser("~/Dropbox/Unfundedpension/src/raw/cog/PID_GID_Crosswalk.txt")

#Utilize if you want to convert GID to PID format
def convert_id(row):
    return str(row["FIPS Code-State"]) + str(row["GID"][2]) + str(row["FIP county code"]) + str(row["GID"][6:9])


def create_crosswalk(filepath):
    f = open(filepath, "r")
    pid_gid = {}
    for line in f:
        pid_gid[line[:6]] = (line[7:21], line[22:106].strip())


    return pid_gid
print("Starting..")

crosswalk = create_crosswalk(crosswalk_file)


ex = pd.read_pickle('C:/Users/ligna/Dropbox/Unfundedpension/src/int/master_formatted_extended.pkl')

print("Loaded pkl file")
ex["county_fips"] = ex['FIP county code'].apply(lambda x:f"{float(x):03.0f}")

ex["state_fips"] = ex['FIPS Code-State'].apply(lambda x:f"{float(x):02.0f}")

ex["place_fips"] = ex['FIP place code'].apply(lambda x:f"{float(x):05.0f}")


ex["PID6"] = ex.apply(lambda row: row["UniqueID"][-10:-4] if row["Year4"] in ("2019","2018") else np.nan, axis = 1)

ex["GID"] = ex.apply(lambda row: row["UniqueID"][:9] if row["Year4"] not in ("2019","2018") else np.nan, axis = 1)

print("Created New Columns")
for x in crosswalk:
    ex.loc[ex["PID6"] == x, 'GID'] = crosswalk[x][0][:9]
    ex.loc[ex["GID"] == crosswalk[x][0][:9], "PID6"] = x

ex.to_pickle(dropbox + '/src/int/master_fipsprogress.pkl')

ex = pd.read_pickle(dropbox + '/src/int/master_fipsprogress.pkl')
#If IDs that existed pre2018 was found in 2018+ data, revise the UniqueID to go by GID convention
ex["UniqueID"] = ex.apply(lambda row: row["UniqueID"] if pd.isna(row["GID"]) else row["GID"] + row["Year4"], axis = 1)



#ex["incrosswalk"] = ex["county_fips"].apply(lambda x: x != 'nan')
ex["statecounty"] = ex.apply(lambda row: row["GID"][:2] + row["GID"][3:6] if row["Year4"] not in ("2019","2018") else np.nan, axis = 1)

print("Filling in missing county fips information...")
for x in list(ex[ex["county_fips"] == 'nan']["GID"].unique()):
    county = list(ex[ex["GID"] == x]['county_fips'].unique())
    if len(county) > 1:
        county.remove("nan")
        ex.loc[ex['ID'] == x, 'county_fips'] = county[0]


###############
codes = dropbox + "src/raw/cog/GOVS_ID_to_FIPS_Place_Codes_2012.xls"

workbook = pd.read_excel(codes)
#workbook = pd.read_excel("/GOVS_ID_to_FIPS_Place_Codes_2012.xls")

ids = workbook.iloc[16:,1].tolist()
state =  workbook.iloc[16:,3].tolist()
typec = workbook.iloc[16:,4].tolist()
county = workbook.iloc[16:,5].tolist()

fstate = workbook.iloc[16:,8].tolist()
fcounty = workbook.iloc[16:,9].tolist()
fplace = workbook.iloc[16:,10].tolist()

crosswalk_state = {}
crosswalk_id = {}

for x in range(len(ids) - 4):
    crosswalk_state[(state[x],county[x])] = (fstate[x],fcounty[x])
    crosswalk_id[ids[x]] = (fstate[x],fcounty[x],fplace[x])

for x in list(ex[ex['county_fips'] == "nan"]['GID'].unique()):
    if x in crosswalk_id:
        ex.loc[ex["GID"] == x, 'state_fips'] = crosswalk_id[x][0]
        ex.loc[ex["GID"] == x, 'county_fips'] = crosswalk_id[x][1]
        ex.loc[ex["GID"] == x, 'place_fips'] = crosswalk_id[x][2]


for x in list(ex[ex["county_fips"] == 'nan']["statecounty"].unique()):
    if (x[:2], x[2:]) in crosswalk_state:
        info = crosswalk_state[(x[:2],x[2:])]
        ex.loc[ex["statecounty"] == x, 'state_fips'] = info[0]
        ex.loc[ex["statecounty"] == x, 'county_fips'] = info[1]
        
for x in list(ex[ex["place_fips"] == '00nan']["GID"].unique()):
    county = list(ex[ex["GID"] == x]['place_fips'].unique())
    if len(county) > 1:
        county.remove("00nan")
        ex.loc[ex['GID'] == x, 'place_fips'] = county[0]
        

ex.to_pickle(dropbox + '/src/int/master_fips2019.pkl')
