import yfinance as yf
import streamlit as st
from datetime import date
import re

# Define constants for start and end dates
START = "2018-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

# Processes user input to extract a single ticker symbol
def process_user_input(user_ticker_input):
    if user_ticker_input:
        tickers = re.split(r'\s+', user_ticker_input.strip())
        if len(tickers) != 1:
            st.error("❌ Please provide only one ticker. You can find a full list of tickers [here](https://finance.yahoo.com/trending-tickers). 🧐")
            return None
        return tickers[0].upper()
    return None

# Loads historical data for the given ticker symbol
@st.cache_data(show_spinner=False)
def fetch_data(ticker, start, end):
    data = yf.download(ticker, start, end)
    data.reset_index(inplace=True)
    return data

# Retrieve ticker information, such as the long name.
def get_ticker_info(ticker):
    try:
        info = yf.Ticker(ticker).info
        return info.get("longName", ticker)
    except Exception:
        return ticker

# Validate the ticker symbol, retrieve its information, and load its data.
def validate_and_load_data(ticker):
    try:
        # Validate ticker by attempting to download one day's data
        validation_data = yf.download(ticker, period="1d")
        if validation_data.empty:
            st.error("❌ Please provide a valid ticker. You can find a full list of tickers [here](https://finance.yahoo.com/trending-tickers). 🧐")
            return None, None

        # Retrieve ticker information and full data
        with st.spinner('📈 Loading data... Hold tight! 🚀'):
            ticker_info = get_ticker_info(ticker)
            data = fetch_data(ticker, START, TODAY)
            return ticker_info, data
    except Exception as e:
        st.error(f"❌ Error occurred: {e}")
        return None, None
