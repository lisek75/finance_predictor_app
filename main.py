import subprocess
import sys

import streamlit as st
from datetime import date
import re
from utils.data_utils import load_data, get_ticker_info
from utils.validation_utils import validate_ticker, mean_absolute_percentage_error
import models.prophet_model as prophet_model
from plotly import graph_objs as go

# Define the start and end dates for data collection
START = "2010-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

# The Streamlit app header
st.set_page_config(page_title="Finance Predictor App", page_icon="💰")
st.title("💰 Finance Predictor App")
st.write(
    """
    Predict assets like stocks, currencies, world indices, cryptocurrencies, and futures 
    using the Facebook Prophet model. A full list of these assets can be found [here](https://finance.yahoo.com/trending-tickers).
    """
)
st.divider()

# User input for the ticker symbol
user_input = st.text_input(
    r"$\textsf{\normalsize Enter\ the\ ticker\ for\ prediction: }$",
    label_visibility="visible",
    disabled=False,
    placeholder="e.g. AAPL, BTC=F, EURUSD=X",
).upper()

# Main process after the user inputs a valid ticker
if user_input:
    tickers = re.split(r'\s+', user_input.strip())
    
    if len(tickers) != 1:
        st.error("❌ Please provide exactly one ticker symbol. You can find a full list of tickers [here](https://finance.yahoo.com/trending-tickers). 🧐")
    else:
        ticker = tickers[0]
        if validate_ticker(ticker):
            selected_stock = ticker
            ticker_info = get_ticker_info(selected_stock)
            st.write(f"{ticker_info} ({selected_stock})")

            n_years = st.slider(r"$\textsf{\normalsize Years\ of\ prediction:}$", 1, 4)
            period = n_years * 365     

            # Display a loading spinner while data is being loaded
            with st.spinner('📈 Loading data... Hold tight! 🚀'):
                data = load_data(selected_stock, START, TODAY)

            st.header("Historical Market Data", divider='grey')

            # Plot the raw historical data
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='stock_close'))
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Close Price"
            )
            st.plotly_chart(fig)

            # Fit the Prophet model and make predictions
            with st.spinner('🔮 Fitting the crystal ball... 🧙‍♂️'):
                m, forecast = prophet_model.fit_prophet_model(data, period)

            # Perform cross-validation and calculate performance metrics
            with st.spinner('🤹‍♂️ Juggling some numbers... 🤔'):
                df_cv = prophet_model.cross_validate_model(m)
            global_mape = mean_absolute_percentage_error(df_cv['y'], df_cv['yhat'])
            m_accuracy = 100 - global_mape

            # Plot the forecasted data with accuracy in the title
            st.header(f"Forecast with {m_accuracy:.2f}% Accuracy", divider='grey')
            forecast_fig = prophet_model.plot_forecast(m, forecast)
            st.plotly_chart(forecast_fig)

        else:
            st.error("❌ Please provide a valid ticker. You can find a full list of tickers [here](https://finance.yahoo.com/trending-tickers). 🧐")
