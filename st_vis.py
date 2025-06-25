import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import text
import mplfinance as mpf

from routers import MySQLRouter


# Streamlit input fields
stock_symbol = st.text_input("Enter Stock Symbol:", "")
start_date = st.date_input("Select Start Date:")
end_date = st.date_input("Select End Date:")