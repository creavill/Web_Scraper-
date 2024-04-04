import pandas as pd
import numpy as np
import sys
import numbers

def check(n):
    nines=[9,99,999,9999,'9','99','999','9999',9.0,99.0,999.0,9999.0,'9.0','99.0','999.0','9999.0',99.00,'99.00']
    if(n in nines):
        return True    
    return False

def convert_to_datetime(df):
    
    df.rename(columns={'YY':'year','#YY': 'year','YYYY': 'year', 'MM': 'month','DD': 'day', 'hh': 'hour','mm':'minute' }, inplace=True)
    #print(df['year'])
    df['year'] = df['year'].astype(str).apply(lambda x: int('19' + str(int(float(x)))) if len(str(int(float(x)))) == 2 else int(float(x)))

    if 'minute' in df.columns:
        df['DateTime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour', 'minute']])
        df.drop(['minute'], axis=1, inplace=True)
    else:
        df['DateTime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
    df.drop(['year', 'month', 'day', 'hour'], axis=1, inplace=True)
    return df

def create_id_column(df):
    df['id'] = list(zip(df['lat'], df['lon']))
    return df

def replace_nines(df):
    # Use applymap to apply the check function to all elements in the DataFrame
    #df.applymap(check)

    # Replace all values that are all 9s with np.nan
    df[df.applymap(check)] = np.nan

    # Print the updated DataFrame
    return df

def clean_data(input_fp,output_fp):
    df = pd.read_csv(input_fp)
    df = df.drop(df[df['lat'] == 'lat'].index)
    df.dropna(thresh=8, inplace=True)  
    df = convert_to_datetime(df)
    df = create_id_column(df)
    df = replace_nines(df)
    df.to_csv(output_fp, index=False) 
    return df



def main(args):
    input_fp = args[1]
    output_fp = args[2]
    print(input_fp)
    clean_data(input_fp,output_fp)
    # Read input CSV into a Pandas DataFrame

    
if __name__ == "__main__":
    main(sys.argv)

#main([0,"D:\hist_surf_data/41006_histData.csv","D:\hist_surf_data\41006_histData.csv"])
'''
D:\hist_surf_data\bthd1_histData.csv
D:\hist_surf_data\frfn7_histData.csv
D:\hist_surf_data\jprn7_histData.csv
D:\hist_surf_data\knoh1_histData.csv
D:\hist_surf_data\ljpc1_histData.csv
D:\hist_surf_data\mrsl1_histData.csv
D:\hist_surf_data\nbba3_histData.csv
D:\hist_surf_data\nlma3_histData.csv
D:\hist_surf_data\sbbn2_histData.csv
D:\hist_surf_data\slmn2_histData.csv
D:\hist_surf_data\spll1_histData.csv
D:\hist_surf_data\ssbn7_histData.csv
D:\hist_surf_data\tybg1_histData.csv
'''
