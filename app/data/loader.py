import yfinance as yf
import streamlit as st
import pandas as pd
import re

def get_user_ticker():
    """
    Prompt the user to enter a valid ticker symbol (e.g., AAPL, BTC=F, EURUSD=X).
    
    Returns:
        str: The entered ticker symbol in uppercase.
    """
    
    # Get the current ticker input
    new_ticker = st.sidebar.text_input(
        r"$\textsf{\normalsize Enter\ a\ ticker:\ }$",
        label_visibility="visible",
        disabled=st.session_state.running,
        placeholder="e.g. AAPL, BTC=F, EURUSD=X",
    ).upper()

    st.sidebar.button("Go", disabled=st.session_state.running)

    if 'previous_ticker' in st.session_state and st.session_state.previous_ticker != new_ticker:
        # Reset data and predictions if the ticker has changed
        st.session_state.output_predict = None
        st.session_state.output_warning = None
        st.session_state.output_generate = None
        st.session_state.selected_section = None
        st.session_state.running = False

    # Store the new ticker in session state
    st.session_state.previous_ticker = new_ticker
    # Back to the homepage
    st.session_state.page = "Homepage"

    return new_ticker

def validate_input(ticker_input):
    """
    Validate the user-inputted ticker symbol by checking that only one is entered and 
    attempting to download a piece of data for it.
    
    Args:
        user_ticker_input (str): The ticker symbol entered by the user.

    Returns:
        str: Valid ticker symbol if the validation passes, None otherwise.
    """

    if ticker_input:
        # Step 1: Ensure only one ticker is provided
        tickers = re.split(r'\s+', ticker_input.strip())
        if len(tickers) != 1:
            st.sidebar.error("❌ Please provide only one ticker.")
            return None

        ticker = tickers[0].upper()
        ticker_type = get_ticker_type(ticker)

        # Step 2: Validate the ticker by fetching 1 day or 1 month of data
        try:
            if ticker_type in ["FUTURE", "OPTION"]:
                st.sidebar.error("❌ Futures and options are not supported because they lack sufficient long-term data for forecasting. Please enter a stock, cryptocurrency, or other asset.")
                return None
            if ticker_type == "MUTUALFUND":
                validation_data = yf.download(ticker, period="1mo")
            else:
                validation_data = yf.download(ticker, period="1d")
            if validation_data.empty:
                st.sidebar.error("❌ Invalid ticker provided.")
                return None
        except Exception as e:
            st.sidebar.error(f"❌ Error occurred during validation: {e}")
            return None
        # Return the valid ticker if all checks pass
        return ticker

def get_ticker_type(ticker):
    """
    Fetch the ticker type (e.g., stock, ETF, etc.) from Yahoo Finance.

    Args:
        ticker (str): The ticker symbol for which to get the type.

    Returns:
        str: Ticker type (e.g., 'EQUITY', 'ETF'), or None if there is an error.
    """
    try:
        ticker_info = yf.Ticker(ticker).info

        # Check if the info is not empty
        if not ticker_info:
            st.warning("⚠️ The data is unavailable right now. Please try again later.")
            return None

        # Get the ticker type (e.g., EQUITY, ETF)
        ticker_type = ticker_info.get('quoteType', 'Unknown')
        return ticker_type
    except KeyError:
        # Handle if 'quoteType' is not found in the response
        st.warning("⚠️ Unable to retrieve ticker type. Please try again later.")
        return None
    except Exception as e:
        # Handle other exceptions, including connection errors
        st.warning(f"❌ Unable to access Yahoo Finance API for ticker {ticker}. Please try again later.")
        return None


@st.cache_data(show_spinner=False)
def load_data(ticker):
    """
    Load historical data for the given ticker symbol from Yahoo Finance.

    Args:
        ticker (str): The ticker symbol for which data is to be fetched.

    Returns:
        pd.DataFrame: DataFrame containing historical data for the ticker.
    """
    end = pd.to_datetime("today").date()
    start = (end - pd.DateOffset(years=5)).date()
    
    try:
        with st.spinner('📈 Loading data... Hold tight! 🚀'):
            # Fetch full historical data
            data = yf.download(ticker, start=start, end=end)
            data.reset_index(inplace=True)
            return data
    except Exception as e:
        st.sidebar.error(f"❌ Error occurred while fetching data: {e}")
        return None

def get_ticker_name(ticker):
    """
    Get the long name of the given ticker (e.g., company name).

    Args:
        ticker (str): The ticker symbol.

    Returns:
        str: The long name of the company or the ticker itself if not available.
    """
    try:
        info = yf.Ticker(ticker).info
        long_name = info.get("longName", ticker)
        ticker_type = get_ticker_type(ticker)  # Call the function to get the ticker type
        return f"{long_name} ({ticker_type})"
    except Exception:
        return f"{ticker} (Unknown)"

def get_ticker_info(ticker):
    """
    Determine the type of the ticker and call the appropriate function to fetch detailed info.

    Args:
        ticker (str): The ticker symbol.

    Returns:
        tuple: DataFrames containing relevant info based on ticker type.
    """
    ticker_type = get_ticker_type(ticker)
    if ticker_type == "EQUITY":
        return get_stock_info(ticker)
    else:
        return None, None, None

def get_stock_info(ticker):
    """
    Fetch detailed stock, price, and business information for the provided ticker symbol.

    Args:
        ticker (str): The ticker symbol to fetch data for.

    Returns:
        tuple: Three DataFrames containing stock, price, and business metrics respectively.
    """
    try:
        ticker_obj = yf.Ticker(ticker)
        stock_info = ticker_obj.info

        # Stock Info DataFrame
        stock_data = {
            "Stock Info": ["Company Name", "Country", "Sector", "Industry", "Market Cap", "Enterprise Value", "Beta", "Shares Outstanding", "Revenue (TTM)", "Employees"],
            "Value": [
                str(stock_info.get("longName", "N/A")),
                str(stock_info.get("country", "N/A")),
                str(stock_info.get("sector", "N/A")),
                str(stock_info.get("industry", "N/A")),
                f"${round(stock_info.get('marketCap', 0) / 1e9, 1)}T" if stock_info.get("marketCap") else "N/A",
                f"${round(stock_info.get('enterpriseValue', 0) / 1e9, 1)}T" if stock_info.get("enterpriseValue") else "N/A",
                str(stock_info.get('beta', 'N/A')),
                str(stock_info.get('sharesOutstanding', 'N/A')),
                f"${round(stock_info.get('totalRevenue', 0) / 1e9, 2)}B" if stock_info.get('totalRevenue') else "N/A",  # Revenue in billions
                str(stock_info.get("fullTimeEmployees", "N/A"))
            ]
        }
        stock_info_df = pd.DataFrame(stock_data)

        # Price Info DataFrame
        price_data = {
            "Price Info": ["Current Price", "Previous Close", "Day High", "Day Low", "52 Week High", "52 Week Low", "Volume (10-Day Avg)", "P/S Ratio"],
            "Value": [
                f"${stock_info.get('currentPrice', 'N/A')}" if stock_info.get('currentPrice') is not None else "N/A",
                f"${stock_info.get('previousClose', 'N/A')}" if stock_info.get('previousClose') is not None else "N/A",
                f"${stock_info.get('dayHigh', 'N/A')}" if stock_info.get('dayHigh') is not None else "N/A",
                f"${stock_info.get('dayLow', 'N/A')}" if stock_info.get('dayLow') is not None else "N/A",
                f"${stock_info.get('fiftyTwoWeekHigh', 'N/A')}" if stock_info.get('fiftyTwoWeekHigh') is not None else "N/A",
                f"${stock_info.get('fiftyTwoWeekLow', 'N/A')}" if stock_info.get('fiftyTwoWeekLow') is not None else "N/A",
                str(stock_info.get('averageVolume10days', 'N/A')) if stock_info.get('averageVolume10days') is not None else "N/A",
                str(round(stock_info.get('priceToSalesTrailing12Months', 0), 2)) if stock_info.get('priceToSalesTrailing12Months') is not None else "N/A"
            ]
        }
        price_info_df = pd.DataFrame(price_data)

        # Business Metrics DataFrame
        business_data = {
            "Business Metrics": ["EPS (FWD)", "P/E (FWD)", "PEG Ratio", "Div Rate (FWD)", "Div Yield (FWD)", "EBITDA", "Free Cash Flow", "Return on Equity (ROE)", "Gross Profit Margin", "Recommendation"],
            "Value": [
                str(stock_info.get('forwardEps', 'N/A')) if stock_info.get('forwardEps') is not None else "N/A",
                str(stock_info.get('forwardPE', 'N/A')) if stock_info.get('forwardPE') is not None else "N/A",
                str(stock_info.get('pegRatio', 'N/A')) if stock_info.get('pegRatio') is not None else "N/A",
                f"${stock_info.get('dividendRate', 'N/A')}" if stock_info.get('dividendRate') is not None else "N/A",
                f"{round(stock_info.get('dividendYield', 0) * 100, 2)}%" if stock_info.get('dividendYield') is not None else "N/A",
                f"${round(stock_info.get('ebitda', 0) / 1e9, 2)}B" if stock_info.get('ebitda') is not None else "N/A",
                f"${round(stock_info.get('freeCashflow', 0) / 1e9, 2)}B" if stock_info.get('freeCashflow') is not None else "N/A",  # FCF in billions
                f"{round(stock_info.get('returnOnEquity', 0) * 100, 2)}%" if stock_info.get('returnOnEquity') is not None else "N/A",
                f"{round(stock_info.get('grossMargins', 0) * 100, 2)}%" if stock_info.get('grossMargins') is not None else "N/A",
                str(stock_info.get('recommendationKey', 'N/A').capitalize()) if stock_info.get('recommendationKey') else "N/A"
            ]
        }
        business_info_df = pd.DataFrame(business_data)

        # Display the stock information DataFrame
        with st.expander(f"Stock Information for {ticker}", expanded=False):
            st.write("######")
            st.dataframe(stock_info_df.set_index(stock_info_df.columns[0]), width=800)

        # Display the price information DataFrame
        with st.expander(f"Price Information for {ticker}", expanded=False):
            st.write("######")
            st.dataframe(price_info_df.set_index(price_info_df.columns[0]), width=800)

        # Display the business information DataFrame
        with st.expander(f"Business Information for {ticker}", expanded=False):
            st.write("######")
            st.dataframe(business_info_df.set_index(business_info_df.columns[0]), width=800)

        # Return the three DataFrames if needed elsewhere
        return stock_info_df, price_info_df, business_info_df

    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return None, None, None
