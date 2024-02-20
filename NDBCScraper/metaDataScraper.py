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
    del lst[1]
    return pd.DataFrame(lst)
    

def get_all_data(file_name):
    df = pd.read_csv(file_name)
    dfs = []
    prevName = ""
    for index,rows in df.iterrows():
        dfs.append(scrapeTextFiles(rows["lat"],rows["lon"],rows["url"]))

        if rows['name'] != prevName:
            result = pd.concat(dfs)
            sys.stdout.write('\r')
            # the exact output you're looking for:
            sys.stdout.write(f'{str(index/31507*100)}% : {index}')
            sys.stdout.flush()
            row_name = rows['name']
            new_header = result.iloc[0] #grab the first row for the header
            result = result[1:] #take the data less the header row
            result.columns = new_header
            result.to_csv(f'./historical_data/{row_name}_histData.csv')
    result = pd.concat(dfs)
    row_name = rows['name']
    new_header = result.iloc[0] #grab the first row for the header
    result = result[1:] #take the data less the header row
    result.columns = new_header
    result.to_csv(f'./historical_data/{prevName}_histData.csv')
get_all_data("temp.csv")
#print(extract_data("https://www.ndbc.noaa.gov/station_page.php?station=53046"))
#print(extract_data("https://www.ndbc.noaa.gov/station_page.php?station=46215"))