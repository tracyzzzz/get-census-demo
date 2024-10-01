import requests

def get_race_and_ethnicity(state_code):
    # url = f'https://api.census.gov/data/2022/acs/acs5?get=group(B03002)&for=county:*&in=state:{state_code}'
    url = f'https://api.census.gov/data/2022/acs/acs5?get=group(B03002)&for=county:*&in=state:{state_code}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(f'Race and ethnicity retrieved successfully for {state_code}!')
    else:
        print("Failed to retrieve data.")

    column_names = data[0]

    race_dicts = [
        {column_names[i]: row[i] for i in range(len(column_names))}
        for row in data[1:]
    ]

    # selected_columns =  {
    #     'GEO_ID':'fips',
    #     'NAME':'county',
    #     'B02001_001E':'total_pop',
    #     'B02001_002E':'White',
    #     'B02001_003E':'Black',
    #     'B02001_004E':'Native American',
    #     'B02001_005E':'Asian',
    #     'B02001_006E':'Pacific Islander'
    # }

    selected_columns =  {
        'GEO_ID':'fips',
        'NAME':'county',
        'B03002_001E':'total_pop',
        'B03002_003E':'White',
        'B03002_004E':'Black',
        'B03002_012E':'Latino',
        'B03002_005E':'Native American',
        'B03002_006E':'Asian',
        'B03002_007E':'Pacific Islander'
    }

    modified_race_dicts = [
        {new_name: row[old_name] for old_name, new_name in selected_columns.items() if old_name in row}
        for row in race_dicts
    ]

    for d in modified_race_dicts:
        d['fips'] = d['fips'][-5:]
        white = int(d['White'])
        black = int(d['Black'])
        latino = int(d['Latino'])
        native_american = int(d['Native American'])
        asian = int(d['Asian'])
        pacific_islander = int(d['Pacific Islander'])
        total_pop = int(d['total_pop'])
        d['White'] = round((white/total_pop)*100,1)
        d['Black'] = round((black/total_pop)*100,1)
        d['Latino'] = round((latino/total_pop)*100,1)
        d['Native American'] = round((native_american/total_pop)*100,1)
        d['Asian'] = round((asian/total_pop)*100,1)
        d['Pacific Islander'] = round((pacific_islander/total_pop)*100,1)
        d.pop('total_pop',None)

    return modified_race_dicts

def get_race_and_ethnicity_township(state_code):
    url = f'https://api.census.gov/data/2022/acs/acs5?get=group(B03002)&for=county%20subdivision:*&in=state:{state_code}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(f'Race and ethnicity retrieved successfully for {state_code}!')
    else:
        print("Failed to retrieve data.")

    column_names = data[0]

    race_dicts = [
        {column_names[i]: row[i] for i in range(len(column_names))}
        for row in data[1:]
    ]

    # selected_columns =  {
    #     'GEO_ID':'fips',
    #     'NAME':'county',
    #     'B02001_001E':'total_pop',
    #     'B02001_002E':'White',
    #     'B02001_003E':'Black',
    #     'B02001_004E':'Native American',
    #     'B02001_005E':'Asian',
    #     'B02001_006E':'Pacific Islander'
    # }

    selected_columns =  {
        'GEO_ID':'fips',
        'NAME':'county',
        'B03002_001E':'total_pop',
        'B03002_003E':'White',
        'B03002_004E':'Black',
        'B03002_012E':'Latino',
        'B03002_005E':'Native American',
        'B03002_006E':'Asian',
        'B03002_007E':'Pacific Islander'
    }

    modified_race_dicts = [
        {new_name: row[old_name] for old_name, new_name in selected_columns.items() if old_name in row}
        for row in race_dicts
    ]

    # get rid of the empty townships
    filtered_race_dicts = [d for d in modified_race_dicts if int(d['total_pop']) != 0]

    for d in filtered_race_dicts:
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
        white = int(d['White'])
        black = int(d['Black'])
        latino = int(d['Latino'])
        native_american = int(d['Native American'])
        asian = int(d['Asian'])
        pacific_islander = int(d['Pacific Islander'])
        total_pop = int(d['total_pop'])
        d['White'] = round((white/total_pop)*100,1)
        d['Black'] = round((black/total_pop)*100,1)
        d['Latino'] = round((latino/total_pop)*100,1)
        d['Native American'] = round((native_american/total_pop)*100,1)
        d['Asian'] = round((asian/total_pop)*100,1)
        d['Pacific Islander'] = round((pacific_islander/total_pop)*100,1)
        d.pop('total_pop',None)

    return filtered_race_dicts
