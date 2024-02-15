import pandas as pd
import yfinance as yf
import time
from random import randint
import requests
from bs4 import BeautifulSoup
#Function to calculate ESG Score 
def calculate_ESG_score(ticker):
  try:
    url = 'https://query2.finance.yahoo.com/v1/finance/esgChart'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}

    # List of dataframes
    # List of dataframes
    dfs = {}
    #print(url)
    response = requests.get(url, headers=headers, params={"symbol": ticker})
    data = response.json()
    #print(response.json())
    if response.ok:
 
      try:
            df = pd.DataFrame(data['esgChart']['result'][0]['symbolSeries'])
            #print(df[df.groupby['timestamp'].transform('max') == df['date']])
            #print(df.iloc[df["timestamp"].argmax()] )
            dfs[ticker] = df
      except Exception as e:
            #print( f"ESG Error 1: {str(e)} Ticker: {ticker}")
            pass            

      df = pd.concat(dfs, names=['symbol']).reset_index(level='symbol')
      df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

      df_new=df[df.groupby('symbol')['timestamp'].transform('max') ==       
      df['timestamp']]
      #print(df_new)
      return df_new['esgScore'].values[0]
  except Exception as e:
        #print( f"ESG Error: {str(e)} Ticker: {ticker}")
        return -1