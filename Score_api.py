import pandas as pd
import yfinance as yf
import time
from random import randint
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request 

import score_peg as speg
import score_ESG as sesg
import score_margin as smargin
import score_ebit as sebit
import score_risk as srisk
# import score_sentiments as ssenti

# creating a Flask app 
app = Flask(__name__) 


@app.route('/get_stock_score/<string:ticker_name>', methods = ['GET']) 
def disp(ticker_name):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}

    
    # Define a list of stock symbols (tickers) you want to analyze
    stock_symbols=["DELTACORP.BO"]

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
    for symbol in [ticker_name]:
      try: 
        
        stock = yf.Ticker(symbol)

        info = stock.info

        name = info.get("shortName", "")
        peg = speg.get_peg(symbol)
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
      

        obj= {"ticker" :symbol,
              "scores" :[
                 { 'ScoreName' : "Overall Score","Score" : overall_score,"Comments" : ""},
                { 'ScoreName' : "Fundamental Score","Score": fundamental_score,"Comments" : ""},
                { 'ScoreName' : "Risk Score" ,"Score": risk_score,"Comments" : ""},
                { 'ScoreName' : "PEG Score" ,"Score":peg_score,"Comments" : ""},
              ]
              }
      
      except Exception as e:
              print(f"Error: {e}")
              obj= {"status" : False
              ,"ticker" :symbol,
             
             
              }
          
      stocks_score.append(obj)
        
      

    # sorted_stocks = sorted(stocks_score, key=lambda x: x["Overall_Score"], reverse=True)

    return jsonify(stocks_score[0]) 


   
   

# driver function 
if __name__ == '__main__': 
    app.run(debug = True) 