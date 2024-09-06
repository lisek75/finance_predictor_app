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

    st.write("#####")

    # Fetch stock, price, and business information for the given ticker
    stock_info_df, price_info_df, business_info_df = get_ticker_info(ticker)

    # Display the stock information DataFrame
    st.dataframe(stock_info_df.set_index(stock_info_df.columns[0]), width=800)

    # Display the price information DataFrame
    st.dataframe(price_info_df.set_index(price_info_df.columns[0]), width=800)

    # Display the business information DataFrame
    st.dataframe(business_info_df.set_index(business_info_df.columns[0]), width=800)

    st.write("#####")

    # Show historical data using a custom function
    display_data(data, data, "historical")

    st.write("#####")

    # Plot historical data for the ticker
    plot_data(data)
