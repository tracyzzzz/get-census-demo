import requests

def get_poverty_status(state_code):
    url = f'https://api.census.gov/data/2022/acs/acs5?get=group(B17001)&for=county:*&in=state:{state_code}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print("Poverty status retrieved successfully!")
    else:
        print("Failed to retrieve data.")

    column_names = data[0]

    poverty_dicts = [
        {column_names[i]: row[i] for i in range(len(column_names))}
        for row in data[1:]
    ]

    selected_columns =  {
        'GEO_ID':'fips',
        'B17001_001E':'total_pop',
        'B17001_002E':'poverty',
        'NAME': 'county'
    }

    modified_poverty_dicts = [
        {new_name: row[old_name] for old_name, new_name in selected_columns.items() if old_name in row}
        for row in poverty_dicts
    ]

    keys_to_remove= ['total_pop','poverty']
    for d in modified_poverty_dicts:
        d['fips'] = d['fips'][-5:]
        poverty = int(d['poverty'])
        total_pop = int(d['total_pop'])
        d['below_poverty'] = round((poverty/total_pop)*100,1)
        for key in keys_to_remove:
            d.pop(key,None)

    return modified_poverty_dicts



def get_poverty_status_township(state_code):
    url = f'https://api.census.gov/data/2022/acs/acs5?get=group(B17001)&for=county%20subdivision:*&in=state:{state_code}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print("Poverty status retrieved successfully!")
    else:
        print("Failed to retrieve data.")

    column_names = data[0]

    poverty_dicts = [
        {column_names[i]: row[i] for i in range(len(column_names))}
        for row in data[1:]
    ]

    selected_columns =  {
        'B17001_001E':'total_pop',
        'B17001_002E':'poverty',
        'NAME': 'township'
    }

    modified_poverty_dicts = [
        {new_name: row[old_name] for old_name, new_name in selected_columns.items() if old_name in row}
        for row in poverty_dicts
    ]
    # get rid of the empty townships
    filtered_poverty_dicts = [d for d in modified_poverty_dicts if int(d['total_pop']) != 0]

    keys_to_remove= ['total_pop','poverty']
    for d in filtered_poverty_dicts:
        if ' town,' in d['township']:
            d['township'] = d['township'].split(" town,")[0]
        elif ' city,' in d['township']:
            d['township'] = d['township'].split(" city,")[0]
        elif ' Valley,' in d['township']:
            d['township'] = d['township'].split(" valley,")[0]
        elif ' township,' in d['township']:
            d['township'] = d['township'].split(" township,")[0]
        elif ' location,' in d['township']:
            d['township'] = d['township'].split(" location,")[0]           
        else:
            d['township'] = d['township']    
        poverty = int(d['poverty'])
        total_pop = int(d['total_pop'])
        d['below_poverty'] = round((poverty/total_pop)*100,1)
        for key in keys_to_remove:
            d.pop(key,None)

    return filtered_poverty_dicts