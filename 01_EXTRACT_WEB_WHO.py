from _Config import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

import pandas as pd
from time import sleep
import datetime

dt = datetime.datetime.now().strftime("%Y-%m-%d")

chrome_executable = Service(executable_path=CONFIG_PATH_EXE, log_path='NUL')

chrome_options = Options()
chrome_options.add_argument(f'user-agent=Mozilla/5.0')
chrome_options.add_argument('--ignore-certificate-errors-spki-list')
chrome_options.add_argument('ignore-certificate-errors')
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(service=chrome_executable, options=chrome_options)

driver.get("https://worldhealthorg.shinyapps.io/mpx_global/#section-global")
print("Running Scrapping Web WHO")
sleep(5)

# Click tab 2.3 tables is tag li
btn_li = driver.find_element(By.XPATH, '//li[@data-unique="23_Tables"]')
btn_li.click()

sleep(3)
# Click  head 2.3.2 Cumulative cases and deaths by country 
btn = driver.find_element(By.XPATH, '//a[@href="#section-cumulative-cases-and-deaths-by-country"]')
btn.click()

sleep(3)
# Find Data in tag
tab_country = driver.find_element(By.ID, "section-cumulative-cases-and-deaths-by-country")
div_tab = tab_country.find_element(By.XPATH, "div")
tbody = div_tab.find_element(By.XPATH, "table//tbody")
tr = tbody.find_elements(By.XPATH, "tr")

# Set Variable
Continent_name = ''
Continent = []
Country = []
Total_Confirmed_Cases = []
Total_Probable_Cases = []
Total_Deaths = []

# Loop Data in tag
for row in tr:
    th = row.find_elements(By.XPATH, "th")
    td = row.find_elements(By.XPATH, "td")
        
    if len(td) == 1 and td[0].text != "-":
        # print("Continent_name => ", td[0].text)
        Continent_name = td[0].text
    
    for row_th in th:
        if row_th.text != "Cases shown include those in mainland China, Hong Kong SAR and Taipei":
            # print("Country => ", row_th.text)
            Country.append(row_th.text)

    if len(td) == 3:        
        Continent.append(Continent_name)
        Total_Confirmed_Cases.append(td[0].text)
        Total_Probable_Cases.append(td[1].text)
        Total_Deaths.append(td[2].text)

# Set data from Variable to pandas DataFrame 
df = pd.DataFrame({
    "day_stamp": dt,   
    "country": Country,
    "continent": Continent,
    "confirmed_case": Total_Confirmed_Cases,
    "probable_case": Total_Probable_Cases,
    "death": Total_Deaths
})

# delete last row
df.drop(df.index[-1], inplace=True)

# Create file .csv
df.to_csv(CONFIG_PATH_DATA["Download"] + "country_who.csv", mode="w+", index=False)
driver.close()
