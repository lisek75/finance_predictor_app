import yfinance as yf
import numpy as np

# Validate if the ticker symbol exists
def validate_ticker(ticker):
    if ticker:
        try:
            data = yf.download(ticker, period="1d")
            if not data.empty:
                return True
        except:
            pass
    return False

# Calculate the Mean Absolute Percentage Error (MAPE)
def mean_absolute_percentage_error(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100
