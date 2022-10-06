# CensusFinances
Compiles US Census Bureau's State &amp; Local Government Finance Historical Datasets spanning back to 1967 into DataFrames

Census of Governments (cog)

create_censusofgovernment.py assembles and outputs the CoG data. Produces basic summary statistics.

formatter_pickle.py alters CoG data and fixes FIPS Code-State and UniqueID into fixed length strings.

cog_names.py reads UserGuide for CoG data to create a dictionary that connects Finance Codes to its corresponding full name.

connect_cog.py bridges 1967-2017 PID formatted data to 2018-2019 GID formatted data. It also fills in gaps in information in fips data where applicable.
