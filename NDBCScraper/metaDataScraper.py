import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from time import sleep
import sys

def extract_data(url):
    # Send request to URL and get HTML response
    response = requests.get(url)
    html = response.content

    # Create BeautifulSoup object
    soup = BeautifulSoup(html, 'html.parser')

    # Extract data from h1 tags
    h1_data = []
    for h1 in soup.find_all('h1'):
        h1_data.append({'longName': h1.text.strip()})


    # Extract data from divs with id="stn_metadata"
    metadata_data = soup.find('div', {'id': 'stn_metadata'}).find('p').text.split("\n")
    metadata_data = extract_coordinates_and_metadata(metadata_data)
    # Combine data into a single list
    data = h1_data + metadata_data
    data = dict(pair for d in data for pair in d.items())
    # Create a pandas dataframe from the list
    #df = pd.DataFrame(data,index =[0])

    return data

def extract_coordinates_and_metadata(data_list):
    new_list = []
    for item in data_list:
        if isinstance(item, str) and ":" in item:
            # item is in the form "name: value"
            name, value = item.split(":")
            new_list.append({name.strip(): value.strip()})
        elif isinstance(item, str) and "°" in item:
            # item is a coordinate (lat, lon)
            new_list.append({"coordinates":item })
    return new_list


def scrapeTextFiles(lat,lon,url):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')

    lst =[]
    for lines in str(soup).split("\n"):
        if len(lst) == 0:
            lst.append(["lat","lon"]+lines.split())
        else:
            lst.append([lat,lon]+lines.split())
    if len(lst)>2:
        del lst[1]
    return pd.DataFrame(lst)
    

def get_all_data(file_name):
    df = pd.read_csv(file_name)
    dfs = []
    all_files = df.iterrows()
    prevName = df['name'][0]
    no_wvht = []
    for index,rows in all_files:
        print(index)
        if rows['name'] != prevName and len(dfs)>0:
            sys.stdout.write('\r')
            sys.stdout.write(f'{str(index/31507*100)}% : {index}')
            sys.stdout.flush()

            result = pd.concat(dfs)
            result.to_csv(f'./historical_data/{prevName}_histData.csv')
            dfs=[]
            
        if rows['name'] not in no_wvht:
            scrapedDF =scrapeTextFiles(rows["lat"],rows["lon"],rows["url"])
            new_header = scrapedDF.iloc[0] #grab the first row for the header
            scrapedDF = scrapedDF[1:] #take the data less the header row
            scrapedDF.columns = new_header
            #print(scrapedDF['WVHT'])
            dfs.append(scrapeTextFiles(rows["lat"],rows["lon"],rows["url"]))

        prevName = rows['name']
        
    result = pd.concat(dfs)
    row_name = rows['name']
    new_header = result.iloc[0] #grab the first row for the header
    result = result[1:] #take the data less the header row
    result.columns = new_header
    result.to_csv(f'./historical_data/{prevName}_histData.csv')

get_all_data("temp.csv")
#print(extract_data("https://www.ndbc.noaa.gov/station_page.php?station=53046"))
#print(extract_data("https://www.ndbc.noaa.gov/station_page.php?station=46215"))

'''
def get_all_data(file_name):
    df = pd.read_csv(file_name)
    dfs = {}
    for index, row in df.iterrows():
        name = row['name']
        if name not in dfs:
            dfs[name] = []
        dfs[name].append(scrapeTextFiles(row["lat"],row["lon"],row["url"]))

    for name, data in dfs.items():
        result = pd.concat(data)
        new_header = result.iloc[0] #grab the first row for the header
        result = result[1:] #take the data less the header row
        result.columns = new_header
        result.to_csv(f'./historical_data/{name}_histData.csv')

        
'''