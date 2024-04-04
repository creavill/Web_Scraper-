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

    reavill_conner@instance-1:~/historical_data
scp -r reavill_conner@instance-1:~/historical_data  D:\hist_surf_data
gcloud storage cp --recursive gs://reavill_conner@instance-1:~/historical_data/* D:\hist_surf_data
gsutil rsync -r gs://historical_data/ D:\hist_surf_data
gcloud compute scp -r reavill_conner@instance-1:~/historical_data reavi@Conners-stuff:D:\hist_surf_data
gcloud compute scp -r reavill_conner@instance-1:~/historical_data reavi@192.168.1.232:D:\hist_surf_data
192.168.1.232

reavi@Conners-stuff:~/test
gcloud compute copy-files example-instance:~/REMOTE-DIR ~/LOCAL-DIR --zone=us-central1-a
reavi@Conners-stuff:~/test
gcloud compute copy-files reavill_conner@instance-1:~/historical_data ~/test --zone=us-central1-a

lost
46069_histData.csv
46063_histData.csv
'''

