import os 
import pandas as pd

files =  os.listdir('D:\hist_surf_data')
new_files = []
for f in files:
    new_files.append(f.split("_")[0])

#print(new_files)
df = pd.read_csv("CleanedStationList.csv")

not_collected = [] 
for names in df['name']:
    if names not in new_files:
        not_collected.append(names)

#print(not_collected)
final_url_list =[]
bigDf = pd.read_csv("temp.csv")
for index,rows in bigDf.iterrows():
    if rows['name'] not in new_files:
        final_url_list.append(rows)


print(len(final_url_list))
#12428