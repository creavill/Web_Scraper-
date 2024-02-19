import pandas as pd

# assume 'data.csv' is the path to your csv file
df = pd.read_csv('./NDBCScraper/AdvancedStationList.csv')
df.dropna(subset=['coordinates'], inplace=True)
# get the count of non-null values for each column
counts = df.count()

# get the columns with most values being empty, None, or null

empty_cols = df.columns[counts < df.shape[0] / 2]

# remove the empty columns from the dataframe
df.drop(empty_cols, axis=1, inplace=True)
df.to_csv('./NDBCScraper/CleanedStationList.csv', index=False)  
# print the removed columns to console
print("Removed columns:")
print(empty_cols)