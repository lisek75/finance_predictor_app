import pandas as pd
from pmdarima import auto_arima
from statsmodels.tsa.arima.model import ARIMA
from sklearn.model_selection import TimeSeriesSplit
import plotly.graph_objects as go
import streamlit as st

def fit_arima_model(data, period):
    """
    Fits an ARIMA model to the historical 'Close' prices and forecasts future values.

    Args:
        data (pd.DataFrame): Historical data containing 'Date' and 'Close' columns.
        period (int): Number of periods (days) to forecast into the future.

    Returns:
        m_arima (AutoARIMA): Fitted ARIMA model.
        forecast_df (pd.DataFrame): DataFrame containing forecasted values and corresponding dates.
    """

    # Automatically find the best ARIMA order using AutoARIMA
    m_arima = auto_arima(
                    data['Close'],
                    seasonal=True, 
                    m=7,                                # Weekly seasonality for financial data
                    max_p=4, max_d=1, max_q=3,          # ARIMA order constraints
                    max_P=2, max_D=1, max_Q=1,          # Seasonal ARIMA order constraints
                    stepwise=True,
                    trace=True,                         # Show model fitting process
                    error_action='ignore',              # Ignore fitting errors for certain parameter combinations
                    suppress_warnings=True,             # Suppress irrelevant warnings
                    n_jobs=1                           # Utilize all CPU cores for faster computation
                )
    print(m_arima.summary())

    # Forecast for the specified future periods
    future_forecast = m_arima.predict(n_periods=period)

    # Generate future dates for the forecast period
    forecast_dates = pd.date_range(start=data['Date'].iloc[-1] + pd.Timedelta(days=1), periods=period, freq='D')

    # Create a DataFrame to store forecasted values along with dates
    forecast_df = pd.DataFrame({
        'Date': forecast_dates,
        'Forecast': future_forecast
    })

    return m_arima, forecast_df

def cross_validation_arima(data, m_arima):
    """
    Performs rolling cross-validation for the ARIMA model to evaluate prediction performance.

    Args:
        data (pd.DataFrame): Historical data containing 'Close' column.
        m_arima (AutoARIMA): Fitted ARIMA model.

    Returns:
        results_df (pd.DataFrame): DataFrame with actual and predicted values during cross-validation.
    """
    
    data = data['Close']  # Extract close price series
    
    # Initialize TimeSeriesSplit for cross-validation (rolling forward)
    tscv = TimeSeriesSplit(n_splits=5)
 
    # List to store cross-validation results
    results = []

    # Perform rolling cross-validation on splits
    for train_index, test_index in tscv.split(data):
        train, test = data.iloc[train_index], data.iloc[test_index]

        # Forecast for the test set (one-step ahead)
        predictions = m_arima.predict(n_periods=len(test))

        # Store actual vs predicted values
        for actual, predicted in zip(test.values.flatten(), predictions):
            results.append({'Actual': actual, 'Predicted': predicted})

    # Convert the result list to a DataFrame
    results_df = pd.DataFrame(results)
    
    return results_df

def plot_arima_forecast(data, forecast):
    """
    Plots the ARIMA forecast along with historical data using Plotly.

    Args:
        data (pd.DataFrame): Historical data with 'Date' and 'Close' columns.
        forecast (pd.DataFrame): Forecasted values with 'Date' and 'Forecast' columns.

    Returns:
        fig (go.Figure): Plotly figure object with the forecast visualization.
    """

    try:
        # Common style dictionary for fonts
        common_font_style = dict(size=14, color='#ffffff')

        # Create a Plotly figure object
        fig = go.Figure()

        # Plot historical data ('Actual' line)
        fig.add_trace(go.Scatter(
            x=data['Date'],
            y=data['Close'],
            mode='lines',
            name='Actual',
            marker=dict(color='#87CEEB', size=3),
            hovertemplate='Actual: %{y:.2f}<extra></extra>',
        ))

        # Plot forecasted data ('Predicted' line)
        fig.add_trace(go.Scatter(
            x=forecast['Date'],
            y=forecast['Forecast'],
            mode='lines',
            name='Predicted',
            marker=dict(color='#FF0000', size=3),
            hovertemplate='Predicted: %{y:.2f}<extra></extra>' ,
        ))

        # Customize chart layout
        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Close Price ($)',
            margin=dict(t=20, b=0, l=0, r=0),
            font=common_font_style,  # Apply the common font to the whole chart
            hovermode='x',
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1,
                xanchor='center',
                x=0.5,
                font=common_font_style  # Use the same common font style for the legend
            )
        )

        return fig
    except Exception as e:
        st.error(f"Error plotting forecast: {e}")
        return None
