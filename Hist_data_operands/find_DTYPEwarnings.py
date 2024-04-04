import pandas as pd
import os
import warnings
warnings.simplefilter('error', pd.errors.DtypeWarning)

def find_csv_with_dtype_warnings(folder_path):
    """Iterates through a folder of CSV files and prints filenames where a DtypeWarning occurs.

    Args:
        folder_path (str): The path to the folder containing CSV files.
    """

    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            filepath = os.path.join(folder_path, filename)
            try:
                pd.read_csv(filepath)
            except pd.errors.DtypeWarning:
                print(f"DtypeWarning in file: {filename}")

# Example usage
folder_path ="D:\hist_data_sandbox/" # Replace with your folder path
find_csv_with_dtype_warnings(folder_path)