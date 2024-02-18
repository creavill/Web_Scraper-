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

    if table == None:
        return extract_spot_data(soup,url)
    
    else:
        return extract_table_data(table)

def extract_spot_data(soup,url):
    # Find all span elements with class="wanna-item-label"
    labels = soup.find_all('span', {'class': 'wanna-item-label-gps'})
    labels += soup.find_all('span', {'class': 'wanna-item-label'})
    

    # Create an empty dictionary to store the data
    data = {"url": url.replace("/index.html","").replace("https://www.wannasurf.com/spot/","")}

    # Loop through the labels and extract the text and value
    for label in labels:
        # Get the text and value from the label
        text = label.text.strip()
        temp = label.next_sibling

        if temp == None:
            value = "None"
        else:
            value = temp.text.strip()
        
        # Add the data to the dictionary
        data[text] = value

    # Return the dictionary
    #df = pd.DataFrame.from_dict(data, orient='index')
    f = open("demofile2.txt", "a")
    f.write(str(data)+"\n")
    f.close()
    return data

def extract_table_data(table):
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


def scrape_url(url, df):

    baseUrl = 'https://www.wannasurf.com'
    # Base case: check if there is a table with id 'wanna-table'
    
    # Recursive case: scrape sub-URLs
    for sub_url in df['sublink']:
        # Get the sub-URL
        sub_url = baseUrl+sub_url
        print(sub_url)
        # Scrape the sub-URL
        sub_df = web_scraper(sub_url)
      
        if type(sub_df) == dict:
            pass
        elif "sublink" in sub_df.columns:
            # Recursively scrape the sub-URL's sub-URLs
            scrape_url(sub_url, sub_df)


url = "https://www.wannasurf.com/spot/North_America/USA/California/index.html"
#url = "https://www.wannasurf.com/spot/North_America/USA/California/Del_Norte/Smithh_River_-_Kellog_Road/Clifford_Kamph_Memorial_Park/index.html"
#url = 'https://www.wannasurf.com/spot/North_America/USA/California/San_Luis_Obispo/index.html'
#df = web_scraper(url)

scrape_url(url,web_scraper(url))
'''
url = 'https://www.wannasurf.com/spot/North_America/USA/California/San_Luis_Obispo/index.html'
df = web_scraper(url)
print(df)

url = "https://www.wannasurf.com/spot/North_America/USA/California/index.html"
df = web_scraper(url)
print(df)
'''