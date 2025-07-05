from talib.abstract import SMA, EMA
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import text
import mplfinance as mpf

from routers import MySQLRouter
from BackTest import ChartTrade, Performance

HOST = "localhost:3306"
USER = "root"
PASSWORD = "stock"
DBNAME = "TWSE"

conn = MySQLRouter(HOST, USER, PASSWORD, DBNAME).mysql_conn
query = """
    SELECT * 
    FROM DailyPrice
    WHERE Date BETWEEN '2025-01-01' AND '2025-06-20' 
    AND SecurityCode = '2330'
"""
results = conn.execute(text(query)).fetchall()
conn.close()

data = pd.DataFrame(results)

data['Date'] = pd.to_datetime(data['Date'])
columns_to_convert = ['TradeVolume', 'OpeningPrice', 'HighestPrice', 'LowestPrice', 'ClosingPrice']
data[columns_to_convert] = data[columns_to_convert].astype(float)

data.rename({"Date": "date",
             "TradeVolume": "volume", 
             "OpeningPrice": "open",
             "HighestPrice": "high",
             "LowestPrice": "low",
             "ClosingPrice": "close"}, axis=1, inplace=True)

data.set_index('date', inplace=True)

data['ceil'] = data['high'].rolling(3).max().shift()

prod = "0050"

df = EMA(data, timeperiod=20)