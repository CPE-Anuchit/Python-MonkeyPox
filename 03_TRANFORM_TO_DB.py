from _Config import *
from datetime import datetime
import pandas as pd
import pyodbc

########################################
# SET DATE
dt = datetime.now().strftime("%Y-%m-%d")

# Set table name
table_name = "covid_case_sum_week"

# Set path country_who.csv file
csv_file = CONFIG_PATH_DATA["Processe"] + "country_who.csv"

# pandas Read file country_who.csv file
df = pd.read_csv(csv_file, encoding="utf-8", dtype=str)

if dt == df["day_stamp"].loc[0]:    
    conn = pyodbc.connect(CONFIG_DB["MSSQL"])
    cursor = conn.cursor()
    for index, row in df.iterrows():
        cursor.execute("INSERT INTO who_monkey (day_stamp, week, country, continent, confirmed_case, probable_case, death) values(?,?,?,?,?,?,?)", row.day_stamp, row.week, row.country, row.continent, row.confirmed_case, row.probable_case, row.death)

    conn.commit()
    cursor.close()
    conn.close()
