import requests
from bs4 import BeautifulSoup
import pandas as pd

def web_scraper(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table with id='wanna-table'
    table = soup.find('table', {'id': 'wanna-table'})

    # Extract the table headers
    headers = [th.text.strip() for th in table.find('thead').find_all('th')]

    # Extract the table data
    data = []
    for row in table.find('tbody').find_all('tr'):
        rows = [td.text.strip() for td in row.find_all('td')]
        # Check if there is a <a href> tag in the first column
        if row.find('td').find('a'):
            if "sublink" not in headers:
                headers.append("sublink")
            # Extract the link text and URL
            link_url = row.find('td').find('a')['href']
            # Add a new column "sublink" with the link text and URL
            rows.append( link_url)
        data.append(rows)

    # Create a Pandas DataFrame with the extracted data
    df = pd.DataFrame(data, columns=headers)
    print(clean_df(df))
    print("\n")
    return clean_df(df)

def clean_df(df):
    # Remove columns with empty or '' labels
    df = df.drop(columns=[col for col in df.columns if col == '' or col is None])

    # Remove columns where all data points are empty
    df = df.drop(columns=[col for col in df.columns if df[col].isnull().all() or df[col][0]==""])
    
    return df

def get_spot_data():
    # This function is called when there is no table with id='wanna-table'
    # You can modify this function to return some default data or raise an error
    print("spot")
    return pd.DataFrame([], columns=[])

def scrape_url(url, df):

    baseUrl = 'https://www.wannasurf.com'
    # Base case: check if there is a table with id 'wanna-table'
    
    if not df.empty and 'sublink' not in df.columns :
        # If there is a table with id 'wanna-table', call get_spot_data()
        get_spot_data(url)
        return

    # Recursive case: scrape sub-URLs
    for sub_url in df['sublink']:
        # Get the sub-URL
        sub_url = baseUrl+sub_url
        print(sub_url)
        # Scrape the sub-URL
        sub_df = web_scraper(sub_url)

        # Recursively scrape the sub-URL's sub-URLs
        scrape_url(sub_url, sub_df)


url = "https://www.wannasurf.com/spot/North_America/USA/California/index.html"

scrape_url(url,web_scraper(url))
'''
url = 'https://www.wannasurf.com/spot/North_America/USA/California/San_Luis_Obispo/index.html'
df = web_scraper(url)
print(df)

url = "https://www.wannasurf.com/spot/North_America/USA/California/index.html"
df = web_scraper(url)
print(df)
'''