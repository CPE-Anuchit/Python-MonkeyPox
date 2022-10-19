from _Config import *
from datetime import datetime
import pandas as pd

########################################
# SET DATE AND WEEK
dt = datetime.now().strftime("%Y-%m-%d")
dt_w = datetime.now().strftime("%V")

########################################
# SET Input and Output File
input_file = CONFIG_PATH_DATA["Download"] + "country_who.csv"
output_file = CONFIG_PATH_DATA["Processe"] + "country_who.csv"

########################################
# Read File Process AND Convert Data SET type
df = pd.read_csv(input_file, sep=",", dtype=str)
df["day_stamp"] = pd.to_datetime(df["day_stamp"], format="%Y-%m-%d")
df["week"] = dt_w
df["confirmed_case"] = pd.to_numeric(df["confirmed_case"].str.split(",").str.join(""))
df["probable_case"] = pd.to_numeric(df["probable_case"].str.split(",").str.join(""))

########################################
# Check Case have , number
if df["death"].dtypes != "int64": 
    df["death"] = pd.to_numeric(df["death"].str.split(",").str.join(""))

########################################
# Sort Column
df = df[["day_stamp", "week", "country", "continent", "confirmed_case", "probable_case", "death"]]
df.to_csv(output_file, index=False)

