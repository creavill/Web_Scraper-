import requests
from bs4 import BeautifulSoup
import pandas as pd

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

#print(extract_data("https://www.ndbc.noaa.gov/station_page.php?station=53046"))
#print(extract_data("https://www.ndbc.noaa.gov/station_page.php?station=46215"))