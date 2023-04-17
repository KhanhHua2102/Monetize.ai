from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
plt.style.use('seaborn')    

import yfinance as yf

appl = yf.Ticker("AAPL")

import yfinance as yf


date = "2022-04-10"
data = yf.download("AAPL", start = date, end="2023-04-12")
print(appl.info['longName'])