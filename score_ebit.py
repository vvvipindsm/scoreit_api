import pandas as pd
import yfinance as yf
import time
from random import randint
import requests
from bs4 import BeautifulSoup
def score_ebit(ebit):
    if ebit*100 > 50:
        return 5
    elif ebit*100 > 40:
        return 4
    elif ebit *100> 30:
        return 3
    elif ebit > 20:
        return 2
    else:
        return 1