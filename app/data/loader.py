import yfinance as yf
import streamlit as st
import pandas as pd
from datetime import date
import re

# Define constants for start and end dates
START = "2018-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

# Function to get the ticker input from the user.
def get_user_ticker():
    return st.text_input(
        r"$\textsf{\normalsize Enter\ a\ ticker\ }$",
        label_visibility="visible",
        disabled=st.session_state.running,
        placeholder="e.g. AAPL, BTC=F, EURUSD=X"
    ).upper()


# Validate and process the user's ticker input.
def validate_input(user_ticker_input):

    if user_ticker_input:
        # Step 1: Ensure only one ticker is provided
        tickers = re.split(r'\s+', user_ticker_input.strip())
        if len(tickers) != 1:
            st.error("❌ Please provide only one ticker. You can find a full list of tickers [here](https://finance.yahoo.com/trending-tickers). 🧐")
            return None

        ticker = tickers[0].upper()

        # Step 2: Validate the ticker by fetching 1 day of data
        try:
            validation_data = yf.download(ticker, period="1d")
            if validation_data.empty:
                st.error("❌ Invalid ticker provided. Please try again.")
                return None
        except Exception as e:
            st.error(f"❌ Error occurred during validation: {e}")
            return None

        # Return the valid ticker if all checks pass
        return ticker

# Load and display full historical data for the valid ticker
@st.cache_data(show_spinner=False)
def load_data(ticker):
    try:
        with st.spinner('📈 Loading data... Hold tight! 🚀'):
            # Fetch full historical data (no need to check data validity again)
            data = yf.download(ticker, START, TODAY)
            data.reset_index(inplace=True)
            return data
    except Exception as e:
        st.error(f"❌ Error occurred while fetching data: {e}")
        return None


# Retrieve ticker long name
def get_ticker_name(ticker):
    try:
        info = yf.Ticker(ticker).info
        return info.get("longName", ticker)
    except Exception:
        return ticker
    
