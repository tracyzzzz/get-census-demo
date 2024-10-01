import requests
import json

def get_education_attainment(state_code):
    url = f'https://api.census.gov/data/2022/acs/acs5/subject?get=group(S1501)&for=county:*&in=state:{state_code}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(f'Education retrieved successfully for {state_code}')
    else:
        print("Failed to retrieve data.")

    column_names = data[0]

    education_dicts = [
        {column_names[i]: row[i] for i in range(len(column_names))}
        for row in data[1:]
    ]

    # selected_columns =  {
    #     'GEO_ID':'fips',
    #     'NAME':'county',
    #     'S1501_C01_006E':'total_pop',
    #     'S1501_C01_009E':'highschool',
    #     'S1501_C01_011E':'associates',
    #     'S1501_C01_012E':'bachelor',
    #     'S1501_C01_013E':'graduate',
    #     'S1501_C01_015E':'bachelor_up'
    # }

    selected_columns =  {
        'GEO_ID':'fips',
        'NAME':'county',
        'S1501_C01_006E':'total_pop',
        'S1501_C01_009E':'highschool',
        'S1501_C01_011E':'associates',
        'S1501_C01_015E':'bachelor_up'
    }

    modified_education_dicts = [
        {new_name: row[old_name] for old_name, new_name in selected_columns.items() if old_name in row}
        for row in education_dicts
    ]


    # keys_to_remove= ['total_pop','associates','highschool','bachelor','graduate','bachelor_up']
    keys_to_remove= ['total_pop','associates','highschool']

    for county_dict in modified_education_dicts:
        county_dict['fips'] = county_dict['fips'][-5:]
        highschool = int(county_dict['highschool'])
        associates = int(county_dict['associates'])
        # bachelor = int(county_dict['bachelor'])
        # graduate = int(county_dict['graduate'])
        bachelor_up = int(county_dict['bachelor_up'])
        total_pop = int(county_dict['total_pop'])
        county_dict['no_college_degree'] = round((1-(associates+bachelor_up)/total_pop)*100,1)
        county_dict['high_school_degree'] = round((highschool/total_pop)*100,1)
        county_dict['associates_degree'] = round((associates/total_pop)*100,1)
        county_dict['bachelor_up'] = round((bachelor_up/total_pop)*100,1)
        # county_dict['bachelors_degree'] = round((bachelor/total_pop)*100,1)
        # county_dict['graduate_or_professional'] = round((graduate/total_pop)*100,1)
        for key in keys_to_remove:
            county_dict.pop(key,None)
    
    # print(modified_education_dicts)
    return modified_education_dicts


def get_education_attainment_township(state_code):
    url = f'https://api.census.gov/data/2022/acs/acs5/subject?get=group(S1501)&for=county%20subdivision:*&in=state:{state_code}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(f'Education retrieved successfully for {state_code}')
    else:
        print("Failed to retrieve data.")

    column_names = data[0]

    education_dicts = [
        {column_names[i]: row[i] for i in range(len(column_names))}
        for row in data[1:]
    ]

    # selected_columns =  {
    #     'GEO_ID':'fips',
    #     'NAME':'county',
    #     'S1501_C01_006E':'total_pop',
    #     'S1501_C01_009E':'highschool',
    #     'S1501_C01_011E':'associates',
    #     'S1501_C01_012E':'bachelor',
    #     'S1501_C01_013E':'graduate',
    #     'S1501_C01_015E':'bachelor_up'
    # }

    selected_columns =  {
        'GEO_ID':'fips',
        'NAME':'county',
        'S1501_C01_006E':'total_pop',
        'S1501_C01_009E':'highschool',
        'S1501_C01_011E':'associates',
        'S1501_C01_015E':'bachelor_up'
    }

    modified_education_dicts = [
        {new_name: row[old_name] for old_name, new_name in selected_columns.items() if old_name in row}
        for row in education_dicts
    ]

    # get rid of the empty townships
    filtered_education_dicts = [d for d in modified_education_dicts if int(d['total_pop']) >=  65000]


    # keys_to_remove= ['total_pop','associates','highschool','bachelor','graduate','bachelor_up']
    keys_to_remove= ['total_pop','associates','highschool']

    for d in filtered_education_dicts:
        d['fips'] = d['fips'][-10:]
        # if ' town,' in d['township']:
        #     d['township'] = d['township'].split(" town,")[0]
        # elif ' city,' in d['township']:
        #     d['township'] = d['township'].split(" city,")[0]
        # elif ' Valley,' in d['township']:
        #     d['township'] = d['township'].split(" valley,")[0]
        # elif ' township,' in d['township']:
        #     d['township'] = d['township'].split(" township,")[0]
        # elif ' location,' in d['township']:
        #     d['township'] = d['township'].split(" location,")[0]           
        # else:
        #     d['township'] = d['township']
        associates = int(d['associates'])
        highschool = int(d['highschool'])
        # bachelor = int(d['bachelor'])
        # graduate = int(d['graduate'])
        bachelor_up = int(d['bachelor_up'])
        total_pop = int(d['total_pop'])
        d['no_college_degree'] = round((1-(associates+bachelor_up)/total_pop)*100,1)
        d['high_school_degree'] = round((highschool/total_pop)*100,1)
        d['associates_degree'] = round((associates/total_pop)*100,1)
        d['bachelor_up'] = round((bachelor_up/total_pop)*100,1)
        # d['bachelors_degree'] = round((bachelor/total_pop)*100,1)
        # d['graduate_or_professional'] = round((graduate/total_pop)*100,1)
        for key in keys_to_remove:
            d.pop(key,None)

    # print(modified_education_dicts)
    return filtered_education_dicts

def replace_fips(dicts):
    with open('ne_cousubs_to_fips_2022.json', 'r') as file:
        json_data = json.load(file)
    for d in dicts:
        fips_key = d['fips']
        if fips_key in json_data:
            d['fips'] = json_data[fips_key]['FIPS']
    return dicts


