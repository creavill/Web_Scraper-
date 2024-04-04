import sys
import pandas as pd

def main(args):
    input_fp = args[1]
    output_fp = args[2]

    # Read input CSV into a Pandas DataFrame
    df = pd.read_csv(input_fp)
    print(input_fp)
    
    df = df.drop(df[df['WVHT'] == 'WVHT'].index)
    df.dropna(thresh=8, inplace=True)  

    # Cleaning Logic (Part 1: Columns)
    '''
    def check(n):
    if type(n) == int or type(n) == float:
        return str(int(n)) == '9' * len(str(int(n)))
    return False

    # Remove columns where most of the values are 9's
    threshold = 0.8  # change this to adjust the threshold
    df = df.loc[:, df.apply(lambda x: (x.apply(check)).sum() / len(x) < threshold, axis=0)]

    import pandas as pd

    # Sample dataframe with numbers and strings
    df = pd.DataFrame({
        'A': [1, 2, 9, 19, 99.0],
        'B': [3, 9, 99, 'string', 'another string']
    })

    def check(n):
        if type(n) == int or type(n) == float:
            return str(int(n)) == '9' * len(str(int(n)))
        return False

    # Apply the check function to each element of the dataframe
    df = df.applymap(lambda x: None if check(x) else x)

    print(df)

    '''
    # ***
    # next time you use this code test and replace with the function above
    # ***
    for col in df.columns:
        null_like_values = ['999.0', '99.0', '99', '', '999',99,99.0,999,999.0,float('nan'),'99.00','9999.0',9999.0]
        if df[col].isin(null_like_values).sum() > 0.75 * len(df):  
            df.drop(col, axis=1, inplace=True)


    # Output the cleaned DataFrame to the output CSV
    df.to_csv(output_fp, index=False)

    # Column Output Logic
    filename = input_fp.split('/')[-1]  # Extract filename from path
    columns_string = filename + ":" + ",".join(df.columns) + "\n"

    with open("000_columns.txt", "a") as f:  # 'a' for appending
        f.write(columns_string)

if __name__ == "__main__":
    main(sys.argv)
#main([0,"D:\hist_surf_data/32488_histData.csv","D:\hist_surf_data_cleaned/32488_histData.csv"])