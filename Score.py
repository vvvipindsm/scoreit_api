import pandas as pd
import yfinance as yf
import time
from random import randint
import requests
from bs4 import BeautifulSoup
import score_peg as speg
import score_ESG as sesg
import score_margin as smargin
import score_ebit as sebit
import score_risk as srisk
# import score_senti¸ments as ssenti


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}

# Define a list of stock symbols (tickers) you want to analyze
stock_symbols=["DELTACORP.BO","000333.SZ","03690.HK","BATAINDIA.BO","TITAN.BO","HEROMOTOCO.BO","M&M.BO","BOSCHLTD.BO","TATAMOTORS.BO","MARUTI.BO","BAJAJ-AUTO.BO","JUBLFOOD.BO","601888.SS","AEO","AMZN","ANF","APTV","AZO","BABA","BBW","BBY","BNED","BURL","BWA","CAAS","CAKE","CCL.L","CMG","CPG.L","CZR","DG","DLTR","DOL.TO","DOM.L","EDU","ETSY","F","FL","GM","GOOS.TO","GPS","GRMN","GRPN","H","HAS","HD","HIBB","HMC","HOG","HRB","HSW.L","IHG.L","KMX","LCII","LE","LOOK.L","LOW","LREN3.SA","LULU","LVS","M","MAR","MAT","MCD","MGLU3.SA","MOV","NCLH","NKE","NXT.L","ORLY","OTB.L","PLNT","PTON","PZZA","QSR.TO","SBUX","SFIX","SONY","SWBI","TAL","TCS","TGT","TJX","TM","TSLA","TXRH","UAA","ULTA","URBN","VFC","VOW.F","VRA","WEN","WH","WSM","WTB.L","YUM"]

#Define Weights

weights = {
    "PEG": 0.35,
    "EBIT": 0.25,
    "Operating_Profit_Margin": 0.1,
    "ROA": 0.1,
    "ROE": 0.1,
    "Net_Profit_Margin": 0.1
}
stocks_score = []



# Fetch and score the metrics for each stock
for symbol in stock_symbols:
  try: 
    
    stock = yf.Ticker(symbol)
    info = stock.info
    name = info.get("shortName", "")
    peg=speg.get_peg(symbol)
    if peg < 0:
       peg = info.get("pegRatio", 0)
    if symbol == "NVDA":
       peg=3.08
       
    peg_score = speg.score_peg(peg)* weights["PEG"]

    ebitdaMargins = info.get("ebitdaMargins", 0)
    ebit_score = sebit.score_ebit(ebitdaMargins)* weights["EBIT"]

    op_margin = info.get("operatingMargins", 0)
    op_margin_score = smargin.score_margin(op_margin)*weights["Operating_Profit_Margin"]
  

    np_margin = info.get("profitMargins", 0)
    np_margin_score = smargin.score_margin(np_margin)*weights["Net_Profit_Margin"]


    roa= info.get("returnOnAssets", 0)
    roa_score = smargin.score_margin(roa)*weights["ROA"]
  
    roe= info.get("returnOnEquity", 0)
    roe_score = smargin.score_margin(roe)*weights["ROE"]

    max_fundamental_score = 5
    # Calculate Fundamental score
    fundamental_score = (peg_score + ebit_score + op_margin_score + roa_score + roe_score + np_margin_score)/max_fundamental_score 

#Calculate Risk Score
    debt_obj = srisk.calculate_debt_equity_ratio_and_score(stock, symbol)
    risk_score = debt_obj.get('risk_score', 0)


    #calculate ESG Score
    esg_score = sesg.calculate_ESG_score(symbol)
    
    # Define the weights for each score (you can adjust these weights based on your preferences)
    risk_weight = 0.3  # Weight for the risk score
    fundamental_weight = 0.7  # Weight for the fundamental score

      # Calculate the overall score as a weighted average
    overall_score = (risk_weight * (risk_score/5)) + (fundamental_weight * fundamental_score)
   

    obj= {"ticker" :symbol
          ,"Name": name
          ,"Overall_Score": overall_score
          ,"Fundamental_Score": fundamental_score
          ,"PEG": peg
          ,"EBITDA_Margins": ebitdaMargins
          ,"Operating_Margin": op_margin
          ,"NetProfitMargins": np_margin
          ,"Return on Asset": roa
          ,"Return on Equity": roe
          ,"PEG_Score": peg_score
          ,"EBIT_score": ebit_score
          ,"Operating_Margin_Score": op_margin_score
          ,"NetProfitMargins_Score": np_margin_score
          ,"Return on Asset_Score": roa_score
          ,"Return on Equity_Score": roe_score
          ,"Risk ": debt_obj
          ,"Risk_score": risk_score 
          ,"ESG_Score": esg_score
          }
  
  except Exception as e:
          print(f"Error: {e}")
          obj= {"ticker" :symbol
          ,"Name":""
          ,"Overall_Score": -1
          ,"Fundamental_Score": -1
          ,"PEG": -1
          ,"EBIT": -1
          ,"Operating_Margin": -1
          ,"NetProfitMargins": -1
          ,"Return on Asset": -1
          ,"Return on Equity": -1
          ,"PEG_Score": -1  
          ,"EBIT_score": -1
          ,"Operating_Margin_Score": -1
          ,"NetProfitMargins_Score": -1
          ,"Return on Asset_Score": -1
          ,"Return on Equity_Score": -1
          ,"Risk ": "N/A"
          ,"Risk_score": -1
          ,"ESG_Score": -1
          }
      
  stocks_score.append(obj)
    
   

sorted_stocks = sorted(stocks_score, key=lambda x: x["Overall_Score"], reverse=True)
i=1
# Print the sorted stocks with their overall scores
for stock in sorted_stocks:
    
    print(f"{i}. {stock['ticker']}: Overall Score = {stock['Overall_Score']:.2f} Fundamental Score = {stock['Fundamental_Score']:.2f} Risk Score = {stock['Risk_score']:.2f} ESG Score = {stock['ESG_Score']:.2f}")
    print(f"==============================")
    if i<25 :
        print(f"{stock}" ) 
    print(f"==============================")
    print()
    i=i+1
   
   