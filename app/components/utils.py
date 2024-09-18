import streamlit as st

def display_data(historical_data, forecast_data, data_type, model_type):
    """
    Displays the DataFrame `forecast_data` or any other type based on the selected data type.

    Parameters:
    - historical_data: The historical data used to train the model, contains actual values up to the present.
    - forecast_data: The forecast data containing predicted values and additional components.
    - data_type: The type of data to display ('forecast', 'historical', or others).
    - model_type: The type of forecasting model ('prophet' or 'arima').
    """

    if data_type == "forecast":
        # Get the last date in the historical data
        last_date = historical_data['Date'].max()

        if model_type == "Prophet":
            # Rename columns for a user-friendly display
            forecast_data = forecast_data.rename(columns={
                'ds': 'Date',
                'yhat': 'Predicted Close Price ($)'
            })[['Date', 'Predicted Close Price ($)']]

        elif model_type == "ARIMA":
            # Rename columns for a user-friendly display
            forecast_data = forecast_data.rename(columns={
                'Forecast': 'Predicted Close Price ($)'
            })[['Date', 'Predicted Close Price ($)']]

        # Format the Date column to remove time
        forecast_data['Date'] = forecast_data['Date'].dt.strftime('%Y-%m-%d')

        # Display the filtered forecast data
        st.dataframe(forecast_data.reset_index(drop=True))

    # For all other data types, simply display the provided DataFrame 
    else:

        # Format the Date column to only show date (remove time)
        historical_data['Date'] = historical_data['Date'].dt.strftime('%Y-%m-%d')

        st.write(forecast_data.reset_index(drop=True))