import requests
from bs4 import BeautifulSoup
import pandas as pd


def getCountries(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table with id='wanna-table'
    table =[]
    for a in soup.find_all('a', {'class': 'wanna-sublink countryWithSpot'}, href=True):
       table.append( a['href'])

    return table

print(getCountries("https://www.wannasurf.com/spot/"))