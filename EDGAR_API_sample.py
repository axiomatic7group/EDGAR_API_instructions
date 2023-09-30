
import pandas as pd 
import os
import requests

cwd = os.getcwd()
tickers = pd.read_json(cwd+'/company_tickers.json', orient='index')

def get_cik(ticker, tickers):
    cik = str(tickers[tickers['ticker']==str(ticker)]['cik_str'].iloc[0]).zfill(10)
    cik = "CIK"+str(cik)+".json"
    return cik, tickers[tickers['ticker']==ticker]

### Enter Ticker ###
cik = get_cik('AAPL', tickers)

url = "http://data.sec.gov/api/xbrl/companyfacts/"
headers = {
    "User-Agent": "Daniel M axiomaticgroup@proton.me",
    "Accept-Encoding": "gzip, deflate, br",
    "Host": "data.sec.gov"}
url = url+str(cik[0])
response = requests.get(url=url, headers=headers)
response = response.json()
tmp_facts = response['facts']
tmp_dei = tmp_facts['dei']
tmp_us_gaap = tmp_facts['us-gaap']

tmp_us_gaap_df = pd.DataFrame(columns=['label', 'description', 'units'])
for i, e in enumerate(tmp_us_gaap.keys()):
    temp_df = pd.json_normalize(tmp_us_gaap[e])
    if len(temp_df.columns) == 3:
        #compile dataframe with aall labels, description, and dict with the data
        temp_df.columns = ['label', 'description', 'units']
        tmp_us_gaap_df = pd.concat([tmp_us_gaap_df, temp_df], axis=0)
    else:
        #filter out and show us the none pure items
        print(temp_df.loc[0])

label_list = list(tmp_us_gaap_df['label'])

### Select an item from label_list ex. label_list[15] or 'Revenues'
label = 'Revenues'

data_df = pd.json_normalize(tmp_us_gaap_df[tmp_us_gaap_df['label']==label]['units'][0])

print(tmp_us_gaap_df[tmp_us_gaap_df['label']==label]['label'][0])
print(tmp_us_gaap_df[tmp_us_gaap_df['label']==label]['description'][0])
print(data_df)