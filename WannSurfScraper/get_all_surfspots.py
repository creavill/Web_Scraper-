import pandas as pd

def combine_text_files(file_list):
    dictionaries = []
    for file in file_list:
        with open(file, 'r',encoding="utf8") as f:
            for line in f:
                dictionaries.append(eval(line))

    # combine the dictionaries into a single dataframe
    df = pd.DataFrame(dictionaries)
    # output the dataframe to a csv file
    df.to_csv('All_Surf_Spots.csv', index=False)

files = ["Africa.txt","Asia.txt","Australia_Pacific.txt","Central_America.txt","Europe.txt","Middle_East.txt","North_America.txt","South_America.txt"]
combine_text_files(files)