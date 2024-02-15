import pandas as pd
import yfinance as yf
import time
from random import randint
import requests
from bs4 import BeautifulSoup
def get_peg(ticker):
  ret=-1
  try:
        
        r = requests.get('https://finance.yahoo.com/quote/{}/key-statistics?p={}'.format(ticker,ticker), headers=headers)
        #print(r.text)
       # Parse the HTML content of the page
        soup = BeautifulSoup(r.text, "html.parser")
        # Find the first table on the page
        first_table = soup.find("table")

        # Check if a table was found
        if first_table:
        # Find all the rows in the table
          rows = first_table.find_all("tr")

        # Check if there are at least 6 rows
          if len(rows) >= 6:
            # Get the 6th row
            sixth_row = rows[5]

            # Find all the cells (columns) in the row
            cells = sixth_row.find_all("td")

            # Check if there are at least 2 columns in the row
            if len(cells) >= 2:
                # Get the content of the 2nd column (index 1)
                header= cells[0].get_text()
                content = cells[1].get_text()
                ret=float(content.strip())
                #print(f"{ticker} {header.strip()}: {ret}")
            else:
                print("Not enough columns in the 6th row.")
          else:
            print("Not enough rows in the table.")

        else:
          print("No table found on the page.")
        #if ret<0:
          #print(f"{ticker} PEG: {ret}")  
        return ret
  except:
   print(f"{ticker} PEG: {ret}")   
   return -1

# Define scoring ranges for each metric (customize as needed)
def score_peg(peg_ratio):
    if peg_ratio <= 0:
        return 0  
    elif peg_ratio < 1:
        return 5
    elif peg_ratio < 1.5:
        return 4
    elif peg_ratio < 2:
        return 3
    elif peg_ratio < 2.5:
        return 2
    
    else:
        return 1