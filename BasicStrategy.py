# Basic In and Out Strategy for Stock Trading

import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import text

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

prod = "2330"

position = 0
trade = pd.DataFrame()

for i in range(data.shape[0]-1):
    c_time = data.index[i]
    c_low = data.loc[c_time, 'low']
    c_high = data.loc[c_time, 'high']
    c_close = data.loc[c_time, 'close']
    c_open = data.loc[c_time, 'open']

    n_time = data.index[i+1]
    n_open = data.loc[n_time, 'open']

    if position == 0:
        if c_close > c_open and (c_close-c_open) * 2 < (c_open-c_low):
            position = 1
            order_i = i
            order_time = n_time
            order_price = n_open
            order_unit = 1

    elif position == 1:
        if i > order_i + 3 and c_close > c_open:
            position = 0
            cover_time = n_time
            cover_price = n_open
            trade = pd.concat([trade, pd.DataFrame([[
                prod,
                "Buy",
                order_time,
                order_price,
                cover_time,
                cover_price,
                order_unit
            ]])], ignore_index=True)


Performance(trade, prodtype='Stock')
ChartTrade(data, trade, v_enable=True)
            