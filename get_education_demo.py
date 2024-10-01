import json
import csv
import importlib
import education
importlib.reload(education)
from education import get_education_attainment, get_education_attainment_township,replace_fips
importlib.reload(abbr_fips_dict)
import abbr_fips_dict
from abbr_fips_dict import state_abbrev_fips_dict_1, state_abbrev_fips_dict_2, ne_state_abbrev_fips_dict, btg_state_fips_dict

# For state AL(01) - MS(28)
county_list_1 = []
for abbr, fips in state_abbrev_fips_dict_1.items():
    # print(fips)
    individual_state = get_education_attainment(fips)
    county_list_1.append(individual_state)

# For state MO(29) - WY(56)
county_list_2 = []
for abbr, fips in state_abbrev_fips_dict_2.items():
    # print(fips)
    individual_state = get_education_attainment(fips)
    county_list_2.append(individual_state)

# Combining all states; len(county_list) should equal to 45
county_list = county_list_1 + county_list_2
flattened_counties = [item for sublist in county_list for item in sublist]


# For New England states
township_list = []
for abbr, fips in ne_state_abbrev_fips_dict.items():
    individual_state = get_education_attainment_township(fips)
    township_list.append(individual_state)

# Replace county_subdivision fips with pseudo fips in magic wall
flattened_township_list = [item for sublist in township_list for item in sublist]
flattened_pseudo_township_list = replace_fips(flattened_township_list)

# Combine county dicts and township dicts
flattened_all = flattened_counties + flattened_pseudo_township_list

### Battleground specific
btg_list = []
for abbr, fips in btg_state_fips_dict.items():
    print(fips)
    individual_state = get_education_attainment(fips)
    btg_list.append(individual_state)
flattened_btg = [item for sublist in btg_list for item in sublist]


output_file_name ='education_pseudo_all.csv'
column_names = flattened_all[0].keys()

with open(output_file_name, mode= 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file,column_names)
        dict_writer.writeheader()
        dict_writer.writerows(flattened_all)