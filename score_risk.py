def calculate_debt_equity_ratio_and_score(stock, ticker):

    try:
        # Fetch the balance sheet data
        balance_sheet = stock.balance_sheet
     

        #for index, row in balance_sheet.iterrows():
          #print(index, row)

         # Fetch beta and current ratio data
        beta = stock.info.get("beta", None)
        balance_sheet = stock.balance_sheet
      
        current_ratio = stock.info.get("currentRatio", None)

        # Extract long-term debt and shareholders' equity
        total_debt = balance_sheet.loc["Total Debt"].values[0]
        total_stockholder_equity = balance_sheet.loc["Stockholders Equity"].values[0]


        # Calculate the debt-equity ratio
        debt_equity_ratio = total_debt / total_stockholder_equity

      
        # Define risk score thresholds
        low_risk_threshold = 0.5
        moderate_risk_threshold = 1
        high_risk_threshold = 2.0
        very_high_risk_threshold = 2.0

        # Assign a risk score based on the debt-equity ratio
        if debt_equity_ratio <= low_risk_threshold and debt_equity_ratio>0:
            risk_score=5 
            risk_score_text = "Low Risk (5)"
        elif debt_equity_ratio <= moderate_risk_threshold and debt_equity_ratio>0:
            risk_score=4 
            risk_score_text = "Moderate Risk (4)"
        elif debt_equity_ratio <= high_risk_threshold and debt_equity_ratio>0:
            risk_score=3
            risk_score_text = "High Risk (3)"
        elif debt_equity_ratio <= very_high_risk_threshold and debt_equity_ratio>0:  
            risk_score=2
            risk_score_text = "Very High Risk (2) and debt_equity_ratio>0"
        else:
            risk_score=1 
            risk_score_text = "Very Very High Risk (1)"

        debt_obj= {
                    "total_debt":total_debt
                   ,"total_stockholder_equity":total_stockholder_equity                              ,"debt_equity_ratio":debt_equity_ratio
                   ,"risk_score": risk_score 
                   ,"risk_score_text": risk_score_text
                   ,"beta": beta
                   ,"Current Ratio": current_ratio 
                  }
        return debt_obj

    except Exception as e:
        #print( f"Error: {str(e)} Ticker: {ticker}")
        return {
                    "total_debt": "N/A"
                   ,"total_stockholder_equity":"N/A"                               
                   ,"debt_equity_ratio":"N/a"
                   ,"risk_score": -1 
                   ,"risk_score_text": "Couln't retrieve"
        }