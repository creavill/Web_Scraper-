import pandas as pd
from metaDataScraper import extract_data

def enrich_data(csv_file):
    df = pd.read_csv(csv_file)
    newDf =[]
    for index, row in df.iterrows():
        url = row['URL']
        data = extract_data(url)
        newDf.append(combine_dicts(row.to_dict() ,data))
        print(newDf)
    
    return pd.DataFrame.from_dict(newDf)


def combine_dicts(dict1, dict2):
    combined_dict = dict1.copy()
    combined_dict.update(dict2)
    return combined_dict

df = enrich_data('./NDBCScraper/StationList.csv')
df.to_csv('AdvancedStationList.csv', index=False)  
print(df)