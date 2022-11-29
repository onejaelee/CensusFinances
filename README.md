# CensusFinances
Compiles US Census Bureau's State &amp; Local Government Finance Historical Datasets spanning back to 1967 into DataFrames

#### Public datasets can be found from the following links

2020-1993 will show up for each year named "Public Use Files": https://www.census.gov/programs-surveys/gov-finances/data/datasets.html
1967-2012 under filename "_IndFin_1967-2012": https://www.census.gov/programs-surveys/gov-finances/data/historical-data.html

2020-1993 and 1967-2012 have two different ways of formatting the CoG data and can be merged using ```connect_cog.py```

#### Census of Governments (cog)
* ```create_censusofgovernment.py``` assembles and outputs the CoG data. Produces basic summary statistics.
* ```formatter_pickle.py``` alters CoG data and fixes FIPS Code-State and UniqueID into fixed length strings.
* ```cog_names.py``` reads UserGuide for CoG data to create a dictionary that connects Finance Codes to its corresponding full name.
* ```connect_cog.py``` bridges 1967-2017 PID formatted data to 2018-2019 GID formatted data. It also fills in gaps in information in fips data where applicable.
* ```id_map.py```Creates a dictionary of CoG IDs as keys and FIPS State code as values. Corresponds CoG keys (corresponding to a government entity) to a specific state.
