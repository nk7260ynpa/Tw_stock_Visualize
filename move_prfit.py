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
    WHERE Date BETWEEN '2025-01-01' AND '2025-07-01' 
    AND SecurityCode = '3032'
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
movestoploss = 0.05

prod = "3032"

position = 0
trade = pd.DataFrame()
for i in range(data.shape[0]-1):
    c_time = data.index[i]
    c_high = data.loc[c_time, 'high']
    c_close = data.loc[c_time, 'close']
    c_ceil = data.loc[c_time, 'ceil']

    n_time = data.index[i+1]
    n_open = data.loc[n_time, 'open']

    if position == 0:
        if c_close > c_ceil:
            position = 1
            order_i = i
            order_time = n_time
            order_price = n_open
            order_unit = 1
            stoploss = order_price * (1 - movestoploss)

    elif position == 1:
        stoploss = max(stoploss, c_close * (1 - movestoploss))
        if c_close < stoploss:
            position = 0
            cover_time = n_time
            cover_price = n_open
            trade = pd.concat([trade, pd.DataFrame([[
                prod, 'Buy', order_time, order_price,
                cover_time, cover_price, order_unit
            ]])], ignore_index=True)

addp = []
addp.append(mpf.make_addplot(data['ceil']))

Performance(trade, prodtype='Stock')
ChartTrade(data, addp=addp, v_enable=False)