import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_data(url, class_name):
    # Send request to URL and get HTML response
    response = requests.get(url)
    html = response.content

    # Create BeautifulSoup object
    soup = BeautifulSoup(html, 'html.parser')

    # Find all elements with the specified class name
    elements = soup.find_all('div', {'class': class_name})

    # Create a list to store the data
    data = []

    # Loop through each element
    for element in elements:
        # Find the <a> tag inside the element
        anchor = element.find('a')

        # Check if the <a> tag has a 'type' attribute with value 'none'
        if anchor and anchor.get('type') != 'none':
            # Extract the name and URL from the <a> tag
            name = anchor.text.strip()
            url = anchor['href']

            # Add the data to the list
            data.append({'name': name, 'URL': "https://www.ndbc.noaa.gov/" + url})

    # Create a pandas data frame from the list
    #df = pd.DataFrame(data)

    return df


url = 'https://www.ndbc.noaa.gov/to_station.shtml'
class_name = 'station-list'
df = scrape_data(url, class_name)
df.to_csv('./StationList.csv', index=False)
print(df)