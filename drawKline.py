import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import text
import mplfinance as mpf

from routers import MySQLRouter

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

df = pd.DataFrame(results)

df['Date'] = pd.to_datetime(df['Date'])
columns_to_convert = ['TradeVolume', 'OpeningPrice', 'HighestPrice', 'LowestPrice', 'ClosingPrice']
df[columns_to_convert] = df[columns_to_convert].astype(float)

df.rename({"Date": "date",
           "TradeVolume": "volume", 
           "OpeningPrice": "open",
           "HighestPrice": "high",
           "LowestPrice": "low",
           "ClosingPrice": "close"}, axis=1, inplace=True)

df.set_index('date', inplace=True)

plt.figure(figsize=(16, 9), dpi=100)
plt.tight_layout()
mpf.plot(df, type='candle', style='yahoo',
         title='2330 Daily Price',
         ylabel='Price (TWD)',
         volume=True,
         mav=(5, 10, 20),
         figratio=(16, 9),
         figscale=1.2,
         savefig='2330_daily_price.png',
         tight_layout=True,
         show_nontrading=True)