import streamlit as st

def display_data(historical_data, forecast_data, data_type):
    """
    Displays the DataFrame `forecast_data` or any other type based on the selected data type.
    If the data type is 'forecast', only the forecast data starting from the last date of `historical_data` is shown.
    
    Parameters:
    - historical_data: The historical data used to train the model, contains actual values up to the present.
    - forecast_data: The forecast data containing predicted values and additional components.
    - data_type: The type of data to display ('forecast', 'historical', or others).
    """

    # Create a checkbox to toggle display of data
    show_data = st.checkbox(f"Display {data_type} data")

    # If the checkbox is selected
    if show_data:
        # Handle forecast data specifically
        if data_type == "forecast":
            # Get the last date in the historical data
            last_date = historical_data['Date'].max()

            # Filter the forecast data to only include dates after the last historical date
            filtered_forecast_data = forecast_data[forecast_data['ds'] > last_date]

            # Rename columns for a user-friendly display
            filtered_forecast_data = filtered_forecast_data.rename(columns={
                'ds': 'Date',
                'trend': 'Predicted Value',
                'yhat_lower': 'Prediction Lower Bound',
                'yhat_upper': 'Prediction Upper Bound',
                'additive_terms': 'Additive Terms'
            })

            # Select only the relevant columns for the forecast display
            filtered_forecast_data = filtered_forecast_data[['Date', 'Predicted Value', 'Prediction Lower Bound', 'Prediction Upper Bound', 'Additive Terms']]

            # Display the filtered forecast data
            st.write(filtered_forecast_data.reset_index(drop=True))

        # For all other data types, simply display the provided DataFrame 
        else:
            st.write(forecast_data.reset_index(drop=True))