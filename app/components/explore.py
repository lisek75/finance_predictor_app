from ..data import plot_data, get_ticker_info
from .utils import *
import streamlit as st

def explore_section(data, ticker):
    """
    Display detailed stock, price, and business information for the given ticker, and show historical data plots.

    Args:
        data (pd.DataFrame): Historical data for the selected ticker.
        ticker (str): The ticker symbol of the stock or asset being analyzed.
    """
    st.markdown(f"<h2>🔍 Explore Data of {ticker}</h2>", unsafe_allow_html=True)

    # Display the ticker information DataFrame
    get_ticker_info(ticker)

    st.write("#####")

    st.write("Historical Data")
    # Show historical data using a custom function
    display_data(data, data, "historical", None)

    st.write("#####")

    # Plot historical data for the ticker
    plot_data(data)
