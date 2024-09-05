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


def get_ticker_info(ticker):
    try:
        ticker_obj = yf.Ticker(ticker)
        stock_info = ticker_obj.info

        # Stock Info DataFrame
        stock_data = {
            "Stock Info": ["Company Name", "Country", "Sector", "Industry", "Market Cap", "Enterprise Value", "Beta", "Shares Outstanding", "Revenue (TTM)", "Employees"],
            "Value": [
                stock_info.get("longName", "N/A"),
                stock_info.get("country", "N/A"),
                stock_info.get("sector", "N/A"),
                stock_info.get("industry", "N/A"),
                f"${round(stock_info.get('marketCap', 0) / 1e9, 1)}T" if stock_info.get("marketCap") else "N/A",
                f"${round(stock_info.get('enterpriseValue', 0) / 1e9, 1)}T" if stock_info.get("enterpriseValue") else "N/A",
                stock_info.get('beta', 'N/A'),
                stock_info.get('sharesOutstanding', 'N/A'),
                f"${round(stock_info.get('totalRevenue', 0) / 1e9, 2)}B" if stock_info.get('totalRevenue') else "N/A",  # Revenue in billions
                stock_info.get("fullTimeEmployees", "N/A")
            ]
        }
        stock_info_df = pd.DataFrame(stock_data)

        # Price Info DataFrame
        price_data = {
            "Price Info": ["Current Price", "Previous Close", "Day High", "Day Low", "52 Week High", "52 Week Low", "Volume (10-Day Avg)", "P/S Ratio"],
            "Value": [
                f"${stock_info.get('currentPrice', 'N/A')}",
                f"${stock_info.get('previousClose', 'N/A')}",
                f"${stock_info.get('dayHigh', 'N/A')}",
                f"${stock_info.get('dayLow', 'N/A')}",
                f"${stock_info.get('fiftyTwoWeekHigh', 'N/A')}",
                f"${stock_info.get('fiftyTwoWeekLow', 'N/A')}",
                stock_info.get('averageVolume10days', 'N/A'),
                round(stock_info.get('priceToSalesTrailing12Months', 'N/A'), 2) if stock_info.get('priceToSalesTrailing12Months') else "N/A"
            ]
        }
        price_info_df = pd.DataFrame(price_data)

        # Business Metrics DataFrame
        business_data = {
            "Business Metrics": ["EPS (FWD)", "P/E (FWD)", "PEG Ratio", "Div Rate (FWD)", "Div Yield (FWD)", "EBITDA", "Free Cash Flow", "Return on Equity (ROE)", "Gross Profit Margin", "Recommendation"],
            "Value": [
                stock_info.get('forwardEps', 'N/A'),
                stock_info.get('forwardPE', 'N/A'),
                stock_info.get('pegRatio', 'N/A'),
                f"${stock_info.get('dividendRate', 'N/A')}" if stock_info.get('dividendRate') else "N/A",
                f"{round(stock_info.get('dividendYield', 0) * 100, 2)}%" if stock_info.get('dividendYield') else "N/A",
                f"${round(stock_info.get('ebitda', 0) / 1e9, 2)}B" if stock_info.get('ebitda') else "N/A",
                f"${round(stock_info.get('freeCashflow', 0) / 1e9, 2)}B" if stock_info.get('freeCashflow') else "N/A",  # FCF in billions
                f"{round(stock_info.get('returnOnEquity', 0) * 100, 2)}%" if stock_info.get('returnOnEquity') else "N/A",
                f"{round(stock_info.get('grossMargins', 0) * 100, 2)}%" if stock_info.get('grossMargins') else "N/A",
                stock_info.get('recommendationKey', 'N/A').capitalize()
            ]
        }
        business_info_df = pd.DataFrame(business_data)

        # Return the three DataFrames
        return stock_info_df, price_info_df, business_info_df

    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None, None, None
