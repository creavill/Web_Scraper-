import pandas as pd
from metaDataScraper import extract_data

def get_hist_files(stations, hist):
    dfStations = pd.read_csv(stations)
    dfHistURL = pd.read_csv(hist)

    dictStations ={}
    for index,rows in dfStations.iterrows():
        dictStations[rows["name"]] = rows["coordinates"].split("(")[0].strip()

    finalDf = []
    for index,rows in dfHistURL.iterrows():
        code = rows["URL"].replace("https://www.ndbc.noaa.gov/view_text_file.php?filename=","").split(".txt")[0][:-5]
        cords = dictStations.get(code.upper())
        if(cords is not None and len(cords)>3):
            cords = cordinates(cords)
            finalDf.append([code,cords[0],cords[1], rows["URL"]])
 
    df = pd.DataFrame(finalDf, columns = ["name","lat","lon","url"]) 
    df.to_csv('./temp.csv', index=False)

def cordinates(str):
    cords = str.split()
    if cords[1] == 'S':
        cords[0] = -float(cords[0])
    if cords[3] == 'W':
        cords[2] = -float(cords[2])
    return(float(cords[0]),float(cords[2]))

    
    
