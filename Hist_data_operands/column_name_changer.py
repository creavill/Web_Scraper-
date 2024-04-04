import pandas as pd
import os

# Specify the path to your folder containing CSV files
folder_path = "D:\hist_surf_data_cleaned"  

# Iterate through the CSV files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        filepath = os.path.join(folder_path, filename)

        # Read the CSV into a Pandas DataFrame
        df = pd.read_csv(filepath)

        # Change column names to lowercase
        df.columns = df.columns.str.lower()

        # Rename the first 8 columns
        new_names = ['index', 'lat', 'lon', 'year', 'month', 'day', 'hour', 'minute']
        df.rename(columns=dict(zip(df.columns[:8], new_names)), inplace=True)

        # Save the modified DataFrame back to the CSV file
        df.to_csv(filepath, index=False)