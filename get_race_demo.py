import json
import csv
import importlib
from education import get_education_attainment, get_education_attainment_township
import race_ethnicity
importlib.reload(race_ethnicity)
from race_ethnicity import get_race_and_ethnicity, get_race_and_ethnicity_township
from income import get_income, get_income_township
from poverty import get_poverty_status, get_poverty_status_township
from abbr_fips_dict import state_abbrev_fips_dict_1, state_abbrev_fips_dict_2, ne_state_abbrev_fips_dict


county_list_1 = []
for abbr, fips in state_abbrev_fips_dict_1.items():
    # print(fips)
    individual_state = get_race_and_ethnicity(fips)
    county_list_1.append(individual_state)

county_list_2 = []
for abbr, fips in state_abbrev_fips_dict_2.items():
    # print(fips)
    individual_state = get_race_and_ethnicity(fips)
    county_list_1.append(individual_state)

county_list = county_list_1 + county_list_2

township_list = []
for abbr, fips in ne_state_abbrev_fips_dict.items():
    individual_state = get_race_and_ethnicity_township(fips)
    township_list.append(individual_state)
flattened_county = [item for sublist in county_list for item in sublist]


all_list = county_list + township_list
flattened_all = [item for sublist in all_list for item in sublist]


output_file_name ='race_ethnicity_all.csv'
column_names = flattened_all[0].keys()

with open(output_file_name, mode= 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file,column_names)
        dict_writer.writeheader()
        dict_writer.writerows(flattened_all)