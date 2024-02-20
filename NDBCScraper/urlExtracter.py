import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_data(url, class_name):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.find_all('ul', {'class': class_name})
    print(elements)
    data = []

    # Loop through each element
    for element in elements:
        anchor = element.find_all('a')
        for a in anchor:
            if a and a.get('type') != 'none':
                name = a.text.strip()
                url = a['href']
                print(name)
                data.append({'name': name, 'URL': "https://www.ndbc.noaa.gov/" + url})
    df = pd.DataFrame(data)

    return df

'''
url = 'https://www.ndbc.noaa.gov/historical_data.shtml#drift'
class_name = 'histfiles'
df = scrape_data(url, class_name)
df.to_csv('./HistData.csv', index=False)
print(df)
'''

