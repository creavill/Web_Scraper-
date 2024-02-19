import pandas as pd

def process_row(row):
    # do something with the row data
    print(row['name'], row['coordinates'])

def process_csv(filename):
    df = pd.read_csv(filename)
    for index, row in df.iterrows():
        process_row(row)

# call the function with a csv file
process_csv('./NDBCScraper/CleanedStationList.csv')