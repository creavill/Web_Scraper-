import pandas as pd
import os
import sqlite3

# **Configuration**
csv_folder = 'D:\hist_surf_data_cleaned'
database_name = 'hist_database.db'

# **Connect to SQLite database**
conn = sqlite3.connect(database_name)
cursor = conn.cursor()

# **Create the table (adjust if your column names are different)**
cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_data (
        lat REAL,
        lon REAL,
        year INTEGER,
        month INTEGER, 
        day INTEGER,
        hour INTEGER,
        minute INTEGER,
        wdir FLOAT,
        wspd FLOAT,
        gst FLOAT,
        wvht FLOAT,
        dpd FLOAT,
        apd FLOAT,
        mwd FLOAT,
        pres FLOAT,
        atmp FLOAT,
        wtmp FLOAT,
        dewp FLOAT,
        vis FLOAT,
        tide FLOAT,
        PRIMARY KEY (lat, lon, year, month, day, hour, minute) 
    )
''')

# **Process CSV files**
for file in os.listdir(csv_folder):
    if file.endswith(".csv"):
        filepath = os.path.join(csv_folder, file)
        print(filepath)
        df = pd.read_csv(filepath)
        df=df.drop('index',axis=1)
        # **Handle potentially missing columns**
        # wdir FLOAT,
        missing_cols = set(['lat', 'lon', 'year', 'month', 'day', 'hour', 'minute','wdir','wspd','gst','wvht','dpd','apd','mwd','pres','atmp','wtmp','dewp','vis','tide']) - set(df.columns) 
        for col in missing_cols:
            df[col] = None  # Fill with placeholder values if needed

        # **Insert data into the database**
        df.to_sql("weather_data", conn, if_exists='append', index=False)

# **Commit changes and close the connection**
conn.commit()
conn.close()

print("CSV data successfully transformed into the SQL database!")

'''
if __name__ == '__main__':
    folder_path = 'D:\hist_surf_data_cleaned'
    db_name = 'hist_database.db'
    table_name = 'all_hist_data'
    process_csv(folder_path, db_name, table_name)
    '''