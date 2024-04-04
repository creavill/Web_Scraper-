import pandas as pd
import os
import warnings

def fix_dtype_warnings(folder_path):
    """Iterates through CSV files in a folder, detects DTypeWarnings,
    infers appropriate dtypes, and saves corrected files.

    Args:
        folder_path (str): Path to the folder containing CSV files.
    """

    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            filepath = os.path.join(folder_path, filename)

            # Read CSV with dtype inference, handling DTypeWarnings
            try:
                df = pd.read_csv(filepath, dtype=object, low_memory=False)
                warnings.filterwarnings("ignore", category=pd.errors.DtypeWarning)
            except pd.errors.DtypeWarning as e:
                print(f"DTypeWarning in file: {filename}")
                for col, dtype in e.dtype.items():
                    if dtype == "object":  # Only correct object columns
                        print(f"  - Column '{col}' has mixed types. Inferring dtype...")
                        df[col] = pd.to_numeric(df[col], errors='coerce')  # Attempt numeric
                        if not pd.api.types.is_numeric_dtype(df[col]):
                            df[col] = pd.to_datetime(df[col], errors='coerce')  # Try datetime
                        print(f"    Inferred dtype: {df[col].dtype}")

            # Save corrected DataFrame
            df.to_csv(filepath, index=False)
            print(f"Corrected CSV saved: {filename}")

# Specify the folder path
folder_path = "D:\hist_data_sandbox"  # Replace with your actual path

fix_dtype_warnings(folder_path)