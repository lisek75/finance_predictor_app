from ..data import plot_data, get_ticker_info
import streamlit as st

def explore_section(data, ticker):
    st.write("#####")
    stock_info_df, price_info_df, business_info_df = get_ticker_info(ticker)
    st.dataframe(stock_info_df.set_index(stock_info_df.columns[0]), width=800)
    st.dataframe(price_info_df.set_index(price_info_df.columns[0]), width=800)
    st.dataframe(business_info_df.set_index(business_info_df.columns[0]), width=800)
    st.write("#####")
    plot_data(data)