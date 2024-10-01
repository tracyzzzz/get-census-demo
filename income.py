import requests

def get_income(state_code):
    url = f'https://api.census.gov/data/2022/acs/acs5?get=group(B19001)&for=county:*&in=state:{state_code}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(f'Income retrieved successfully for {state_code}!')
    else:
        print("Failed to retrieve data.")

    column_names = data[0]

    income_dicts = [
        {column_names[i]: row[i] for i in range(len(column_names))}
        for row in data[1:]
    ]

    selected_columns =  {
        'GEO_ID':'fips',
        'NAME':'county',
        'B19001_001E':'total_hh',
        'B19001_002E':'<10',
        'B19001_003E':'10_14',
        'B19001_004E':'15_20',
        'B19001_005E':'20_25',
        'B19001_006E':'25_30',
        'B19001_007E':'30_35',
        'B19001_008E':'35_40',
        'B19001_009E':'40_45',    
        'B19001_010E':'45_50', 
        'B19001_011E':'50_60',
        'B19001_012E':'60_75',
        'B19001_013E':'75_100',
        'B19001_014E':'100_125',
        'B19001_015E':'125_150',
        'B19001_016E':'150_200',
        'B19001_017E':'>200',
    }

    modified_income_dicts = [
        {new_name: row[old_name] for old_name, new_name in selected_columns.items() if old_name in row}
        for row in income_dicts
    ]

    keys_to_remove= [
        '<10','10_14','15_20','20_25',
        '25_30','30_35','35_40','40_45','45_50','50_60','60_75',
        '75_100','100_125',
        '125_150','150_200',
        '>200',
        'total_hh'
    ]

    for d in modified_income_dicts:
        d['fips'] = d['fips'][-5:]
        lower_25 = int(d['<10'])+int(d['10_14'])+int(d['15_20'])+int(d['20_25'])
        lower_75 = int(d['25_30'])+int(d['30_35'])+int(d['35_40'])+int(d['40_45'])+int(d['45_50'])+int(d['50_60'])+int(d['60_75'])
        lower_125 = int(d['75_100'])+int(d['100_125'])
        lower_200 = int(d['125_150'])+int(d['150_200'])
        higher_200 = int(d['>200'])
        # bachelor_up = int(county_dict['bachelor_up'])
        total_hh = int(d['total_hh'])
        d['<$25k'] = round((lower_25/total_hh)*100,1)
        d['<$75k'] = round((lower_75/total_hh)*100,1)
        d['<$125k'] = round((lower_125/total_hh)*100,1)
        d['<$200k'] = round((lower_200/total_hh)*100,1)
        d['$200k+'] = round((higher_200/total_hh)*100,1)

        for key in keys_to_remove:
            d.pop(key,None)
    
    return modified_income_dicts


def get_income_township(state_code):
    url = f'https://api.census.gov/data/2022/acs/acs5?get=group(B19001)&for=county%20subdivision:*&in=state:{state_code}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(f'Income retrieved successfully for {state_code}!')
    else:
        print("Failed to retrieve data.")

    column_names = data[0]

    income_dicts = [
        {column_names[i]: row[i] for i in range(len(column_names))}
        for row in data[1:]
    ]

    selected_columns =  {
        'GEO_ID':'fips',
        'NAME':'county',
        'B19001_001E':'total_hh',
        'B19001_002E':'<10',
        'B19001_003E':'10_14',
        'B19001_004E':'15_20',
        'B19001_005E':'20_25',
        'B19001_006E':'25_30',
        'B19001_007E':'30_35',
        'B19001_008E':'35_40',
        'B19001_009E':'40_45',    
        'B19001_010E':'45_50', 
        'B19001_011E':'50_60',
        'B19001_012E':'60_75',
        'B19001_013E':'75_100',
        'B19001_014E':'100_125',
        'B19001_015E':'125_150',
        'B19001_016E':'150_200',
        'B19001_017E':'>200',
    }

    modified_income_dicts = [
        {new_name: row[old_name] for old_name, new_name in selected_columns.items() if old_name in row}
        for row in income_dicts
    ]

    # get rid of the empty townships
    filtered_income_dicts = [d for d in modified_income_dicts if int(d['total_hh']) != 0]

    keys_to_remove= [
        '<10','10_14','15_20','20_25',
        '25_30','30_35','35_40','40_45','45_50','50_60','60_75',
        '75_100','100_125',
        '125_150','150_200',
        '>200',
        'total_hh'
    ]

    for d in filtered_income_dicts:
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
        lower_25 = int(d['<10'])+int(d['10_14'])+int(d['15_20'])+int(d['20_25'])
        lower_75 = int(d['25_30'])+int(d['30_35'])+int(d['35_40'])+int(d['40_45'])+int(d['45_50'])+int(d['50_60'])+int(d['60_75'])
        lower_125 = int(d['75_100'])+int(d['100_125'])
        lower_200 = int(d['125_150'])+int(d['150_200'])
        higher_200 = int(d['>200'])
        # bachelor_up = int(county_dict['bachelor_up'])
        total_hh = int(d['total_hh'])
        d['<$25k'] = round((lower_25/total_hh)*100,1)
        d['<$75k'] = round((lower_75/total_hh)*100,1)
        d['<$125k'] = round((lower_125/total_hh)*100,1)
        d['<$200k'] = round((lower_200/total_hh)*100,1)
        d['$200k+'] = round((higher_200/total_hh)*100,1)

        for key in keys_to_remove:
            d.pop(key,None)
    
    return filtered_income_dicts

