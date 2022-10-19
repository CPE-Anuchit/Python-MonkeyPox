from _Config import *
import requests
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib.parse
# from datetime import datetime

# dt = datetime.now().strftime("%Y-%m-%d")

token = ""
url = 'https://notify-api.line.me/api/notify'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+ token}

csv_file = CONFIG_PATH_DATA["Processe"] + "country_who.csv"

df = pd.read_csv(csv_file, encoding="utf-8", dtype=str)
row, column = df.shape
dt = df["day_stamp"].loc[0]

txt = f'''
Report WHO Monkey Pox Date : {dt}
Row Total : {row}
'''

msg = urllib.parse.urlencode({"message": txt})

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

try:
    r = session.post(url, headers=headers, data=msg)            
except OSError as Error:
    print (Error)
