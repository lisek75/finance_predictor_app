import yfinance as yf
import pandas as pd
import streamlit as st

# Load data from Yahoo Finance
@st.cache_data
def load_data(ticker, start, end):
    data = yf.download(ticker, start, end)
    data.reset_index(inplace=True)
    return data

# Get the ticker information
def get_ticker_info(ticker):
    try:
        info = yf.Ticker(ticker).info
        return info.get("longName", ticker)
    except:
        return ticker
